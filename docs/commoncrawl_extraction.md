# Extracting Data from CommonCrawl

This guide provides detailed information on accessing and extracting data from CommonCrawl for use in AI training and other applications.

## What is CommonCrawl?

[CommonCrawl](https://commoncrawl.org/) is a non-profit organization that builds and maintains an open repository of web crawl data that can be accessed and analyzed by anyone. The CommonCrawl corpus contains petabytes of data collected over years of web crawling, making it one of the largest publicly available datasets of web content.

## Why Use CommonCrawl for AI Training?

CommonCrawl provides several advantages:

1. **Scale**: Contains billions of web pages providing diverse training examples
2. **Accessibility**: Free and publicly available data
3. **Real-world Content**: Contains actual human-written text from across the internet
4. **Historical Data**: Access to web content over time
5. **Diverse Languages**: Content in many languages and on many topics

## Understanding CommonCrawl Data Formats

CommonCrawl provides data in three primary formats:

1. **WARC (Web ARChive)**: The raw web data including HTTP request and response information
2. **WAT**: Metadata extracted from the WARC files
3. **WET**: Plain text content extracted from the WARC files

For most AI training purposes, you'll likely want to work with either:
- **WARC files** if you need the complete HTML and HTTP metadata
- **WET files** if you only need the extracted plain text

## Accessing CommonCrawl Data

CommonCrawl data is hosted on Amazon S3 and can be accessed via HTTP or directly through AWS S3 if you're in the AWS ecosystem.

### URL Structure

The base URL for CommonCrawl data is:
```
https://data.commoncrawl.org/
```

Individual crawl datasets are organized by date, for example:
```
https://data.commoncrawl.org/crawl-data/CC-MAIN-2023-23/
```

### Index Files

To find specific files, you can use the CommonCrawl index:
```
https://index.commoncrawl.org/
```

## Our Approach: Simplified Extraction

This repository includes a simplified approach to extract a manageable portion of CommonCrawl data:

### 1. Download and Process Script

The `download_cc_sample.py` script automates the process of:
- Downloading a portion of WARC files
- Extracting content
- Filtering for relevant text
- Saving in a more convenient format

```bash
# Download approximately 100MB of CommonCrawl data
python download_cc_sample.py --size 100

# Specify output directory
python download_cc_sample.py --output /path/to/output

# Filter for specific content (default is to filter for bias-related content)
python download_cc_sample.py --filter-mode all  # Don't filter content
```

### 2. Implementation Details

The script uses the following approach:

1. **Identify a Crawl**: Either use the latest crawl or a specified one
2. **Download WARC Files**: Download a portion of the crawl's WARC files
3. **Process Records**: Extract and decode the records from the WARC files
4. **Filter Content**: Keep only records matching filter criteria
5. **Save as JSONL**: Store processed records in JSONL format for easy use

### 3. JSONL Output Format

The processed data is saved in JSONL (JSON Lines) format with the following structure:

```json
{
  "url": "https://example.com/page",
  "domain": "example.com",
  "id": "md5hash",
  "text": "The extracted text content from the web page..."
}
```

This format makes it easy to:
- Process one record at a time
- Filter by domain or URL
- Perform text analysis on the content

## Example: Downloading a Specific Amount of Data

```python
# Download approximately 500MB of data
python download_cc_sample.py --size 500

# Download a smaller sample for testing
python download_cc_sample.py --size 50
```

## Example: Filtering for Specific Content

The default behavior is to filter for content related to ethical considerations (bias, fairness, etc.), but you can customize the filtering:

```python
# In download_cc_sample.py, you can modify the BIAS_KEYWORDS list:
BIAS_KEYWORDS = [
    "gender", "race", "ethnicity", "religion", "politics", "income", 
    # Add your own keywords here...
]
```

Or create a new filter mechanism by modifying the `contains_bias_keywords()` function.

## Advanced: Direct CommonCrawl Access

For more advanced use cases, you can access CommonCrawl data directly:

### Using the AWS CLI

```bash
# List files in a CommonCrawl segment
aws s3 ls --no-sign-request s3://commoncrawl/crawl-data/CC-MAIN-2023-23/segments/1685224643388.28/warc/

# Download a specific file
aws s3 cp --no-sign-request s3://commoncrawl/crawl-data/CC-MAIN-2023-23/segments/1685224643388.28/warc/CC-MAIN-20230528083433-20230528113433-00000.warc.gz local-file.warc.gz
```

### Using Python Directly

```python
import requests
import gzip
import io
from warcio.archiveiterator import ArchiveIterator

# Download a WARC file
url = "https://data.commoncrawl.org/crawl-data/CC-MAIN-2023-23/segments/1685224643388.28/warc/CC-MAIN-20230528083433-20230528113433-00000.warc.gz"
response = requests.get(url, stream=True)

# Process WARC records
with gzip.GzipFile(fileobj=io.BytesIO(response.content)) as f:
    for record in ArchiveIterator(f):
        if record.rec_type == 'response':
            content = record.content_stream().read()
            # Process content...
```

### Using the CommonCrawl Index API

For more targeted extraction, you can use the CommonCrawl Index API:

```python
import requests
import json

index_url = "https://index.commoncrawl.org/CC-MAIN-2023-23-index"
query = {"url": "commoncrawl.org"}
response = requests.get(index_url, params=query)

if response.status_code == 200:
    for line in response.text.strip().split('\n'):
        record = json.loads(line)
        warc_filename = record['filename']
        # Now download the specific WARC file containing this page
```

## Memory and Performance Considerations

Working with CommonCrawl data can be resource-intensive:

1. **Memory Efficient Processing**: The scripts in this repository use streaming approaches to avoid loading entire files into memory
2. **Sampling**: Start with small samples (10-100MB) before scaling up
3. **Filtering Early**: Filter content as early as possible in the pipeline
4. **Parallel Processing**: For large-scale extraction, consider parallel downloading and processing

## Next Steps

After extracting data from CommonCrawl:

1. **Further Filtering**: Apply more sophisticated filters or classifiers to select content
2. **Preprocessing**: Clean and normalize text for AI training
3. **Tokenization**: Convert text into tokens suitable for your model
4. **Training Data Creation**: Use the extracted content to create synthetic training examples

For more information on creating synthetic training data from the extracted content, see [Creating Synthetic Training Data](synthetic_training_data.md).