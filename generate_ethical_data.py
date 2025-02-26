#!/usr/bin/env python
"""
Generate ethical reasoning training data from CommonCrawl samples.
This script analyzes downloaded CommonCrawl data to identify content with
potential ethical implications, then generates training examples with
detailed ethical reasoning.

Usage:
    python generate_ethical_data.py [--input INPUT_DIR] [--output OUTPUT_FILE] [--count COUNT]
"""

import os
import json
import glob
import argparse
import random
import re
import requests
from tqdm import tqdm

# Constants
DEFAULT_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "jsonl")
DEFAULT_OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "ethical_training.jsonl")
DEFAULT_COUNT = 20
OLLAMA_API = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "deepseek-r1"

# Ethical categories and keywords
ETHICAL_CATEGORIES = {
    "fairness": [
        "discrimination", "bias", "prejudice", "equality", "unfair", "unjust", "privilege",
        "favoritism", "equitable", "impartial"
    ],
    "harm": [
        "hurt", "damage", "injury", "pain", "suffering", "abuse", "mistreat", "exploit",
        "harm", "unsafe", "danger", "violent"
    ],
    "autonomy": [
        "freedom", "choice", "consent", "coercion", "manipulation", "force", "control",
        "privacy", "liberty", "self-determination", "agency"
    ],
    "deception": [
        "lie", "deceive", "mislead", "trick", "fraud", "false", "fake", "dishonest",
        "cheat", "scam", "misinformation", "disinformation"
    ],
    "justice": [
        "fair", "rights", "deserve", "punishment", "reward", "compensation", "retribution",
        "law", "legal", "illegal", "crime", "equitable"
    ]
}

# Combined keywords for initial filtering
ALL_ETHICAL_KEYWORDS = []
for keywords in ETHICAL_CATEGORIES.values():
    ALL_ETHICAL_KEYWORDS.extend(keywords)

# Remove duplicates
ALL_ETHICAL_KEYWORDS = list(set(ALL_ETHICAL_KEYWORDS))

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Generate ethical reasoning training data")
    parser.add_argument("--input", type=str, default=DEFAULT_DATA_DIR,
                        help=f"Directory containing JSONL files (default: {DEFAULT_DATA_DIR})")
    parser.add_argument("--output", type=str, default=DEFAULT_OUTPUT_FILE,
                        help=f"Output file for training data (default: {DEFAULT_OUTPUT_FILE})")
    parser.add_argument("--count", type=int, default=DEFAULT_COUNT,
                        help=f"Number of examples to generate (default: {DEFAULT_COUNT})")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL,
                        help=f"Ollama model to use (default: {DEFAULT_MODEL})")
    return parser.parse_args()

def ensure_dir(file_path):
    """Create directory for file if it doesn't exist"""
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def load_cc_data(input_dir):
    """Load CommonCrawl data from JSONL files"""
    all_data = []
    jsonl_files = glob.glob(os.path.join(input_dir, "*.jsonl"))
    
    if not jsonl_files:
        print(f"No JSONL files found in {input_dir}")
        return []
    
    for file_path in jsonl_files:
        print(f"Loading data from {file_path}...")
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    record = json.loads(line.strip())
                    all_data.append(record)
                except json.JSONDecodeError:
                    continue
    
    print(f"Loaded {len(all_data)} documents from {len(jsonl_files)} files")
    return all_data

def extract_ethical_content(documents, keywords=ALL_ETHICAL_KEYWORDS, max_length=1000):
    """Extract passages that contain ethical keywords"""
    ethical_passages = []
    
    for doc in tqdm(documents, desc="Scanning for ethical content"):
        text = doc.get('text', '')
        
        # Skip very short texts
        if len(text) < 100:
            continue
        
        # Check for ethical keywords
        matches = []
        for keyword in keywords:
            pattern = r'\b' + re.escape(keyword) + r'\b'
            for match in re.finditer(pattern, text.lower()):
                # Get context around the match
                start = max(0, match.start() - 200)
                end = min(len(text), match.end() + 200)
                matches.append((match.start(), text[start:end]))
        
        # If matches found, add to ethical passages
        if matches:
            # Sort by position in text
            matches.sort(key=lambda x: x[0])
            
            # Take up to 3 matches from this document
            for _, passage in matches[:3]:
                if len(passage) > max_length:
                    passage = passage[:max_length] + "..."
                ethical_passages.append({
                    'passage': passage,
                    'url': doc.get('url', ''),
                    'domain': doc.get('domain', '')
                })
    
    print(f"Found {len(ethical_passages)} passages with ethical content")
    return ethical_passages

def categorize_ethical_content(passages):
    """Determine primary ethical category for each passage"""
    categorized = []
    
    for passage in tqdm(passages, desc="Categorizing content"):
        text = passage['passage'].lower()
        
        # Count matches for each category
        category_counts = {}
        for category, keywords in ETHICAL_CATEGORIES.items():
            count = 0
            for keyword in keywords:
                pattern = r'\b' + re.escape(keyword) + r'\b'
                count += len(re.findall(pattern, text))
            category_counts[category] = count
        
        # Choose primary category (highest count)
        if sum(category_counts.values()) > 0:
            primary_category = max(category_counts.items(), key=lambda x: x[1])[0]
            passage['category'] = primary_category
            categorized.append(passage)
    
    return categorized

def generate_ethical_reasoning(passage, category, model=DEFAULT_MODEL, timeout=60):
    """Generate ethical reasoning for a passage using Ollama API"""
    # Truncate passage if it's too long
    if len(passage) > 1500:
        passage = passage[:1500] + "..."
    
    system_prompt = f"""You are an ethical reasoning assistant trained to analyze text passages and provide detailed ethical reasoning. 
For the given text passage, identify ethical considerations related to {category} and develop a step-by-step ethical reasoning process.
Analyze the implications thoroughly and consider multiple perspectives.

Structure your reasoning into two main sections with the following format:
<|begin_of_thought|>
(Your step-by-step ethical analysis here, analyzing the ethical implications in detail)
<|end_of_thought|>

<|begin_of_solution|>
(Your final ethical assessment and recommendation, summarizing the key points from your analysis)
<|end_of_solution|>

Keep your response concise but insightful, focusing on the most important ethical considerations."""

    user_prompt = f"""Analyze the following text passage from an ethical perspective, focusing especially on considerations related to {category}:

{passage}

Provide ethical reasoning following the format I specified."""

    try:
        response = requests.post(
            OLLAMA_API,
            json={
                "model": model,
                "system": system_prompt,
                "prompt": user_prompt,
                "stream": False
            },
            timeout=timeout
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "")
        else:
            return f"Error generating ethical reasoning: {response.status_code}"
    except requests.exceptions.Timeout:
        return "Request timed out while generating ethical reasoning"
    except Exception as e:
        return f"Exception during generation: {str(e)}"

def generate_training_data(passages, count, model=DEFAULT_MODEL):
    """Generate training examples with ethical reasoning"""
    # Ensure we have enough passages
    if len(passages) < count:
        print(f"Warning: Only {len(passages)} passages available, less than requested {count}")
        count = min(len(passages), count)
    
    # Select a diverse set of passages
    selected_passages = []
    categories = list(ETHICAL_CATEGORIES.keys())
    
    # Try to get an even distribution across categories
    for category in categories:
        category_passages = [p for p in passages if p.get('category') == category]
        per_category = max(1, count // len(categories))
        
        if len(category_passages) > 0:
            selected_passages.extend(random.sample(
                category_passages, 
                min(per_category, len(category_passages))
            ))
    
    # If we still need more passages, add randomly
    if len(selected_passages) < count:
        remaining = [p for p in passages if p not in selected_passages]
        if remaining:
            selected_passages.extend(random.sample(
                remaining,
                min(count - len(selected_passages), len(remaining))
            ))
    
    # Limit to requested count
    selected_passages = selected_passages[:count]
    
    # Generate ethical reasoning for each passage
    training_data = []
    
    print(f"Generating ethical reasoning for {len(selected_passages)} passages")
    for i, passage in enumerate(selected_passages):
        category = passage.get('category', 'general ethics')
        
        # Progress display
        print(f"Processing example {i+1}/{len(selected_passages)}: {category}")
        
        # Generate reasoning with timeout protection
        try:
            reasoning = generate_ethical_reasoning(passage['passage'], category, model, timeout=90)
            
            # Create training example
            example = {
                "passage": passage['passage'],
                "category": category,
                "url": passage.get('url', ''),
                "domain": passage.get('domain', ''),
                "reasoning": reasoning
            }
            
            training_data.append(example)
            
            # Save example immediately to avoid losing work if script crashes
            with open(f"data/ethical_examples_{i+1}.json", 'w', encoding='utf-8') as f:
                json.dump(example, f, indent=2)
                
        except Exception as e:
            print(f"Error processing example {i+1}: {str(e)}")
            continue
    
    return training_data

def save_training_data(training_data, output_file):
    """Save training data to a JSONL file"""
    ensure_dir(output_file)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for example in training_data:
            f.write(json.dumps(example) + '\n')
    
    print(f"Saved {len(training_data)} training examples to {output_file}")

def main():
    args = parse_args()
    
    # Check if Ollama API is available
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code != 200:
            print("Warning: Ollama API doesn't seem to be available. Generation may fail.")
    except Exception:
        print("Warning: Ollama API doesn't seem to be available. Generation may fail.")
    
    # Load data
    documents = load_cc_data(args.input)
    
    if not documents:
        print("No documents found. Please run the download script first.")
        return
    
    # Process data
    print(f"Extracting ethical content from {len(documents)} documents...")
    ethical_passages = extract_ethical_content(documents)
    
    print(f"Categorizing {len(ethical_passages)} ethical passages...")
    categorized_passages = categorize_ethical_content(ethical_passages)
    
    print(f"Generating {args.count} training examples...")
    training_data = generate_training_data(categorized_passages, args.count, args.model)
    
    # Save training data
    save_training_data(training_data, args.output)
    
    print("Done!")

if __name__ == "__main__":
    main()