#!/usr/bin/env python
"""
CommonCrawl Sample Downloader

This script downloads a small sample of data from CommonCrawl and preprocesses it
for use in ethical AI training. It focuses on filtering content that might contain
potential human biases for analysis.

Usage:
    python download_cc_sample.py [--size SIZE] [--output OUTPUT_DIR]

Requirements:
    - requests
    - warcio
    - beautifulsoup4
    - tqdm
"""

import os
import sys
import gzip
import json
import argparse
import random
import hashlib
from urllib.parse import urlparse
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import re
import io
from warcio.archiveiterator import ArchiveIterator
from concurrent.futures import ThreadPoolExecutor

# Constants
DEFAULT_DOWNLOAD_SIZE = 100  # MB
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
INDEX_URL = "https://index.commoncrawl.org/"
CC_BUCKET = "https://data.commoncrawl.org/"

# Potential bias keywords to look for
BIAS_KEYWORDS = [
    "gender", "race", "ethnicity", "religion", "politics", "income", 
    "class", "age", "disability", "sexuality", "controversial",
    "opinion", "belief", "stereotype", "discrimination", "prejudice",
    "bias", "unfair", "inequality", "privilege", "minority", "majority"
]

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Download a sample of CommonCrawl data")
    parser.add_argument("--size", type=int, default=DEFAULT_DOWNLOAD_SIZE,
                        help=f"Size of data to download in MB (default: {DEFAULT_DOWNLOAD_SIZE})")
    parser.add_argument("--output", type=str, default=OUTPUT_DIR,
                        help=f"Output directory (default: {OUTPUT_DIR})")
    parser.add_argument("--filter-mode", choices=["bias", "all"], default="bias",
                        help="Whether to filter for bias-related content only")
    return parser.parse_args()

def ensure_dir(directory):
    """Create directory if it doesn't exist"""
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def get_latest_crawl_id():
    """Get the ID of the latest CommonCrawl dataset"""
    try:
        response = requests.get(INDEX_URL)
        response.raise_for_status()
        # Extract the latest crawl ID from the response
        latest_id = re.search(r'CC-MAIN-\d{4}-\d{2}', response.text).group(0)
        return latest_id
    except Exception as e:
        print(f"Error getting latest crawl ID: {e}")
        print("Using fallback crawl ID: CC-MAIN-2023-23")
        return "CC-MAIN-2023-23"  # Fallback to a known crawl

def get_warc_paths(crawl_id, num_files=2):
    """Get paths to WARC files from the specified crawl"""
    index_path = f"{CC_BUCKET}crawl-data/{crawl_id}/warc.paths.gz"
    try:
        response = requests.get(index_path, stream=True)
        response.raise_for_status()
        
        # Decompress and read the paths file
        with gzip.GzipFile(fileobj=io.BytesIO(response.content)) as f:
            paths = [line.decode('utf-8').strip() for line in f]
        
        # Randomly select a subset of paths
        selected_paths = random.sample(paths, min(num_files, len(paths)))
        return selected_paths
    except Exception as e:
        print(f"Error getting WARC paths: {e}")
        # Fallback to known WARC files
        return [
            "crawl-data/CC-MAIN-2023-23/segments/1685224643388.28/warc/CC-MAIN-20230528083433-20230528113433-00000.warc.gz",
            "crawl-data/CC-MAIN-2023-23/segments/1685224643388.28/warc/CC-MAIN-20230528083433-20230528113433-00001.warc.gz"
        ]

def download_warc_file(warc_path, output_dir, max_size_mb=50):
    """Download a portion of a WARC file"""
    url = f"{CC_BUCKET}{warc_path}"
    output_file = os.path.join(output_dir, os.path.basename(warc_path))
    
    try:
        # Stream the file and save a portion of it
        print(f"Downloading from {url}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        content_size = int(response.headers.get('content-length', 0))
        max_bytes = max_size_mb * 1024 * 1024
        bytes_to_read = min(content_size, max_bytes)
        
        progress_bar = tqdm(total=bytes_to_read, unit='B', unit_scale=True, desc=os.path.basename(warc_path))
        
        with open(output_file, 'wb') as f:
            bytes_read = 0
            for chunk in response.iter_content(chunk_size=8192):
                if bytes_read >= bytes_to_read:
                    break
                if chunk:
                    bytes_remaining = bytes_to_read - bytes_read
                    if len(chunk) > bytes_remaining:
                        chunk = chunk[:bytes_remaining]
                    f.write(chunk)
                    bytes_read += len(chunk)
                    progress_bar.update(len(chunk))
        
        progress_bar.close()
        return output_file
    except Exception as e:
        print(f"Error downloading WARC file: {e}")
        return None

def extract_text_from_html(html_content):
    """Extract readable text from HTML content"""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "header", "footer", "nav"]):
            script.extract()
        
        # Get text
        text = soup.get_text(separator='\n')
        
        # Clean the text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""

def contains_bias_keywords(text):
    """Check if text contains any bias-related keywords"""
    text_lower = text.lower()
    return any(keyword.lower() in text_lower for keyword in BIAS_KEYWORDS)

def process_warc_file(warc_file, output_dir, filter_mode="bias", max_records=1000):
    """Process a WARC file and extract relevant content"""
    output_file = os.path.join(output_dir, os.path.basename(warc_file).replace('.warc.gz', '.jsonl'))
    
    record_count = 0
    saved_count = 0
    
    try:
        with open(output_file, 'w') as out:
            with open(warc_file, 'rb') as stream:
                for record in tqdm(ArchiveIterator(stream), desc="Processing records", total=max_records):
                    if record_count >= max_records:
                        break
                    
                    record_count += 1
                    
                    if record.rec_type == 'response' and record.http_headers and record.http_headers.get_header('Content-Type', '').startswith('text/html'):
                        try:
                            url = record.rec_headers.get_header('WARC-Target-URI')
                            domain = urlparse(url).netloc
                            payload = record.content_stream().read()
                            
                            if payload:
                                content = None
                                
                                # Try to decode with different encodings
                                for encoding in ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']:
                                    try:
                                        content = payload.decode(encoding)
                                        break
                                    except UnicodeDecodeError:
                                        continue
                                
                                if content:
                                    text = extract_text_from_html(content)
                                    
                                    # Skip if we're filtering for bias keywords and none are found
                                    if filter_mode == "bias" and not contains_bias_keywords(text):
                                        continue
                                    
                                    # Create a record and save it
                                    document = {
                                        'url': url,
                                        'domain': domain,
                                        'id': hashlib.md5(url.encode()).hexdigest(),
                                        'text': text[:10000]  # Limit text size
                                    }
                                    
                                    out.write(json.dumps(document) + '\n')
                                    saved_count += 1
                        except Exception as e:
                            tqdm.write(f"Error processing record: {e}")
    except Exception as e:
        print(f"Error processing WARC file: {e}")
    
    print(f"Processed {record_count} records, saved {saved_count} documents to {output_file}")
    return output_file

def main():
    args = parse_args()
    
    # Create output directory
    output_dir = ensure_dir(args.output)
    warc_dir = ensure_dir(os.path.join(output_dir, "warc"))
    jsonl_dir = ensure_dir(os.path.join(output_dir, "jsonl"))
    
    print(f"Downloading {args.size} MB of CommonCrawl data")
    print(f"Output directory: {output_dir}")
    
    # Get the latest crawl ID
    crawl_id = get_latest_crawl_id()
    print(f"Using crawl ID: {crawl_id}")
    
    # Calculate how many files to download
    files_to_download = max(1, args.size // 50)
    
    # Get WARC paths
    warc_paths = get_warc_paths(crawl_id, files_to_download)
    
    # Download WARC files
    warc_files = []
    for path in warc_paths:
        warc_file = download_warc_file(path, warc_dir, max_size_mb=min(50, args.size))
        if warc_file:
            warc_files.append(warc_file)
    
    # Process WARC files
    jsonl_files = []
    for warc_file in warc_files:
        jsonl_file = process_warc_file(warc_file, jsonl_dir, filter_mode=args.filter_mode)
        if jsonl_file:
            jsonl_files.append(jsonl_file)
    
    # Print summary
    total_size = sum(os.path.getsize(file) for file in warc_files + jsonl_files) / (1024 * 1024)
    print(f"Download and processing complete. Total size: {total_size:.2f} MB")
    print(f"Downloaded {len(warc_files)} WARC files and generated {len(jsonl_files)} JSONL files")
    print(f"WARC files directory: {warc_dir}")
    print(f"JSONL files directory: {jsonl_dir}")

if __name__ == "__main__":
    main()