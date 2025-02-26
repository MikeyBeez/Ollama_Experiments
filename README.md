# Ollama Experiments

This repository contains tools and scripts for experimenting with Ollama models, with a particular focus on generating synthetic training data for specialized objective functions like ethical reasoning.

## Overview

The repository includes:

1. **Simple Agent Chat Interface**: A basic interface for interacting with Ollama models
2. **CommonCrawl Data Extraction**: Tools to download and extract data from CommonCrawl
3. **Synthetic Training Data Generation**: Scripts to generate specialized training data for objectives like ethical reasoning
4. **Ethical Reasoning Agent**: Implementation of an agent specialized in ethical analysis and reasoning

## Requirements

- Python 3.6+
- Ollama installed and running locally (or remotely)
- Language models loaded in Ollama (e.g., deepseek-r1, llama3, etc.)

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/MikeyBeez/Ollama_Experiments.git
   cd Ollama_Experiments
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the environment:
   ```bash
   cp .env.sample .env
   # Edit the .env file to set your preferred model and Ollama host
   ```

## Creating Synthetic Training Data

This repository demonstrates creating synthetic training data for AI models with specific objective functions, such as ethical reasoning. Here's the general workflow:

### 1. Acquiring Source Data from CommonCrawl

CommonCrawl is a vast repository of web crawl data that provides a rich source of human-generated content for training data.

```bash
# Download a sample from CommonCrawl
python download_cc_sample.py --size 100  # Download ~100MB of data
```

The script will:
- Download WARC files from CommonCrawl
- Extract and process the data into a more usable format
- Save the processed data to the `data/jsonl` directory

### 2. Generating Synthetic Training Data

Once you have source data, you can generate synthetic training examples:

```bash
# Generate ethical reasoning training data
python generate_ethical_data.py --count 20  # Generate 20 examples
```

For quicker testing of the synthetic data generation:

```bash
# Test with a single example
python generate_single_example.py --output data/test_example.json
```

### 3. Using the Ethical Reasoning Agent

The repository includes an implementation of an ethical reasoning agent that can analyze scenarios and provide structured ethical analyses:

```bash
# Run with preset scenarios
python ethical_agent.py

# Analyze a specific scenario
python ethical_agent.py --scenario "Companies track user data without consent" --category privacy

# Interactive mode
python ethical_agent.py --interactive
```

## Training Data Formats

The synthetic training data is structured to train models with specialized capabilities:

### Ethical Reasoning Format

```json
{
  "passage": "Text describing an ethically relevant situation",
  "category": "privacy|fairness|autonomy|harm|deception",
  "reasoning": "<|begin_of_thought|>\nDetailed ethical analysis...\n<|end_of_thought|>\n\n<|begin_of_solution|>\nEthical conclusion and recommendations...\n<|end_of_solution|>"
}
```

This format encourages models to:
1. Perform thorough analysis in the "thought" section
2. Provide clear conclusions in the "solution" section

## Extending for Other Objective Functions

This framework can be adapted for other specialized AI capabilities:

1. **Create a data extraction script** to obtain relevant source material
2. **Define the objective function** (what capability you want the AI to learn)
3. **Design a prompt template** that elicits the desired reasoning pattern
4. **Generate synthetic examples** using existing models
5. **Create a specialized agent** that demonstrates the capability

## Components

- `simple_agent.py` - Basic agent interface for Ollama models
- `download_cc_sample.py` - Tool for downloading data from CommonCrawl
- `generate_ethical_data.py` - Generate ethical reasoning training data
- `ethical_agent.py` - Specialized agent for ethical reasoning
- `test_ollama.py` - Diagnostic tool for Ollama API
- `generate_single_example.py` - Generate a single training example
- `.env.sample` - Example environment configuration

## Available Models

To see what models are available on your Ollama instance, run:
```bash
ollama list
```

## License

[MIT License](LICENSE)