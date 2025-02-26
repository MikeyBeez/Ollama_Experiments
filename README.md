# Ollama Experiments: Collaborative Synthetic Training Data

This repository provides tools and infrastructure for creating, sharing, and utilizing high-quality synthetic training data for fine-tuning language models through Ollama. Our primary focus is building a community-driven collection of specialized training examples for capabilities like ethical reasoning, with a structured methodology that anyone can follow.

## Project Mission

Our goal is to:

1. **Enable community-driven data creation**: Provide tools that let anyone generate valuable synthetic training data
2. **Build a shared resource**: Collect diverse, high-quality examples that benefit the entire AI community
3. **Standardize data formats**: Create consistent, well-structured training examples for specialized capabilities
4. **Foster collaboration**: Make it easy to contribute new data and methodologies

## Repository Contents

1. **Simple Agent Chat Interface**: Tools for interacting with Ollama models
2. **CommonCrawl Data Extraction**: Utilities to download and process data from CommonCrawl
3. **Synthetic Training Data Generation**: Scripts to create structured training examples 
4. **Ethical Reasoning Agent**: Implementation demonstrating specialized capabilities

## Requirements

- Python 3.6+
- Ollama installed and running locally (or remotely)
- Language models loaded in Ollama (e.g., deepseek-r1, llama3, etc.)
- MikeyBeez/Ollama_Agents (for some components - see installation instructions below)

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

4. Set up Ollama_Agents:
   ```bash
   # Clone the Ollama_Agents repository
   git clone https://github.com/MikeyBeez/Ollama_Agents.git ../Ollama_Agents
   
   # Add to your Python path (you may want to add this to your .bashrc or .zshrc)
   export PYTHONPATH="../Ollama_Agents:$PYTHONPATH"
   
   # Install its dependencies
   pip install -r ../Ollama_Agents/requirements.txt
   ```

5. Configure the environment:
   ```bash
   cp .env.sample .env
   # Edit the .env file to set your preferred model and Ollama host
   ```

## Complete Tutorial

For a step-by-step walkthrough of the entire process from setup to contributing, see our [Complete Tutorial](docs/complete_tutorial.md).

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

## Contributing to the Repository

We welcome and encourage contributions of synthetic training data and improvements to the generation methodology. Here's how you can contribute:

### Contributing Training Data

1. **Generate synthetic examples** using the tools provided in this repository
2. **Validate your examples** for quality and effectiveness
3. **Submit a pull request** with your new data in the appropriate format
4. **Document your contribution** including any special considerations or insights

### Contribution Guidelines

- Make sure your examples follow the structured format described in this README
- Include metadata about how the examples were generated
- Ensure your examples don't contain personally identifiable information (PII)
- Test your examples with the provided agent implementations

### Ideas for Contributions

- Datasets for new capabilities beyond ethical reasoning
- Improvements to the generation methodology
- New prompt templates that produce better results
- Tools for validating or filtering generated examples

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

## Community and Support

### Asking for Help

If you encounter issues or have questions:
- Open an issue in this repository
- Provide detailed information about your environment and problem
- Share any error messages or unexpected behavior

### Sharing Your Work

We encourage you to share how you've used this framework:
- If you've created interesting examples, submit them through a pull request
- If you've extended the framework for a new capability, consider contributing your code
- Share your success stories in the discussions section

## Using the Data

All data in this repository is available under the MIT License. You are free to:
- Use it for research purposes
- Include it in your own projects
- Build upon it for your own applications

We only ask that you:
- Cite this repository if you use it in academic work
- Consider contributing back improvements or extensions

## License

[MIT License](LICENSE)