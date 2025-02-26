# Complete Tutorial: Contributing Synthetic Training Data

This tutorial will guide you through the entire process of contributing synthetic training data to this repository, from setting up your environment to submitting a pull request with your generated examples.

## Table of Contents

1. [Setting Up Your Environment](#setting-up-your-environment)
2. [Acquiring Data from CommonCrawl](#acquiring-data-from-commoncrawl)
3. [Generating Synthetic Training Examples](#generating-synthetic-training-examples)
4. [Customizing the Generation Process](#customizing-the-generation-process)
5. [Validating Your Generated Data](#validating-your-generated-data)
6. [Submitting Your Contribution](#submitting-your-contribution)

## Setting Up Your Environment

### Prerequisites

Before starting, make sure you have:

- Python 3.6 or higher installed
- Git installed
- Ollama installed (see [Ollama installation guide](https://github.com/ollama/ollama#installation))
- At least one language model loaded in Ollama (e.g., llama3, deepseek, etc.)

### Step 1: Clone the Repository

```bash
git clone https://github.com/MikeyBeez/Ollama_Experiments.git
cd Ollama_Experiments
```

### Step 2: Create a Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Your Environment

```bash
cp .env.sample .env
```

Open the `.env` file in your editor and configure it:

```
# Ollama Configuration
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3  # Or another model you have installed

# API Parameters
TEMPERATURE=0.7
TOP_P=0.9
MAX_TOKENS=2048

# Data Generation Settings
EXAMPLES_PER_BATCH=5
OUTPUT_DIR=./data

# Ethical Categories
ETHICAL_CATEGORIES=privacy,fairness,autonomy,harm,deception,general_ethics

# Logging
LOG_LEVEL=INFO
```

### Step 5: Create a Branch for Your Contribution

```bash
git checkout -b add-my-training-examples
```

## Acquiring Data from CommonCrawl

CommonCrawl is a free repository of web crawl data that provides a great source of diverse text from the web.

### Step 1: Understanding CommonCrawl

CommonCrawl data is stored in WARC (Web ARChive) files, which are large archives of web content. Our tools simplify the process of downloading and extracting useful content from these files.

### Step 2: Download a Sample of CommonCrawl Data

```bash
python download_cc_sample.py --size 100  # Download ~100MB of data
```

This will:
- Download WARC files from CommonCrawl
- Extract text content from web pages
- Filter for relevant content
- Save the processed data to `data/jsonl` directory

### Step 3: Verify the Downloaded Data

```bash
# List the downloaded files
ls -la data/jsonl/

# View a sample of the extracted content
head -n 50 data/jsonl/CC-MAIN-*.jsonl | jq
```

## Generating Synthetic Training Examples

Now that you have raw text data, you can generate synthetic training examples.

### Step 1: Understanding the Ethical Reasoning Format

Our default example uses ethical reasoning as the objective function. Each example follows this structure:

```json
{
  "passage": "Text describing an ethically relevant situation",
  "category": "privacy|fairness|autonomy|harm|deception",
  "reasoning": "<|begin_of_thought|>\nDetailed ethical analysis...\n<|end_of_thought|>\n\n<|begin_of_solution|>\nEthical conclusion and recommendations...\n<|end_of_solution|>"
}
```

### Step 2: Generate Examples

```bash
# Generate 20 ethical reasoning examples
python generate_ethical_data.py --count 20 --output data/my_ethical_examples.json
```

### Step 3: Test with a Single Example

For quicker iteration, you can generate just one example:

```bash
python generate_single_example.py --output data/test_example.json
```

## Customizing the Generation Process

You can customize the generation process to create different types of examples or improve the quality.

### Step 1: Modifying the Prompt Template

Examine the prompt template in `generate_ethical_data.py` and customize it for your needs:

```python
# Example of a prompt template section in the code
prompt = f"""
Given the following situation:
"{text}"

Analyze this situation from an ethical perspective related to {category}.
...
"""
```

### Step 2: Changing Categories or Classifications

Edit the `ETHICAL_CATEGORIES` in your `.env` file or pass them directly via command-line arguments:

```bash
python generate_ethical_data.py --categories privacy,fairness,autonomy --count 10
```

### Step 3: Adjusting Generation Parameters

Change parameters like temperature and max tokens in your `.env` file or via command-line:

```bash
python generate_ethical_data.py --temperature 0.8 --max_tokens 3000 --count 10
```

## Validating Your Generated Data

Before contributing, validate your generated examples to ensure they're high-quality.

### Step 1: Test Examples with the Agent

```bash
# Run the ethical agent with your examples
python ethical_agent.py --examples data/my_ethical_examples.json
```

### Step 2: Manually Review Examples

Open your generated JSON file and review the examples to ensure they:
- Have meaningful and diverse content
- Follow the correct format structure
- Contain thoughtful and useful analysis
- Don't contain problematic or harmful content

### Step 3: Fix or Filter Out Low-Quality Examples

Edit your JSON file to remove or fix any examples that don't meet your quality standards.

## Submitting Your Contribution

Once you have generated and validated your training examples, you can contribute them back to the repository.

### Step 1: Commit Your New Data Files

```bash
git add data/my_ethical_examples.json
git commit -m "Add new ethical reasoning examples focusing on [your focus area]"
```

### Step 2: Push Your Branch to GitHub

First, fork the repository on GitHub, then:

```bash
git remote add fork https://github.com/[YOUR_USERNAME]/Ollama_Experiments.git
git push -u fork add-my-training-examples
```

### Step 3: Create a Pull Request

1. Go to the original repository: https://github.com/MikeyBeez/Ollama_Experiments
2. Click "Pull Requests" and then "New Pull Request"
3. Click "compare across forks"
4. Select your fork and branch
5. Fill out the PR template with information about your contribution:
   - What type of examples did you create?
   - How many examples are included?
   - What methodology did you use?
   - Any special considerations or insights?

### Step 4: Respond to Feedback

The maintainers may provide feedback or ask for changes before accepting your contribution. Be ready to:
- Address any formatting issues
- Improve the quality of examples if needed
- Answer questions about your generation process

## Creating Your Own Objective Function

If you want to create a different type of training data beyond ethical reasoning:

### Step 1: Define Your Objective

Decide what capability you want to teach models:
- Mathematical reasoning
- Legal analysis
- Creative writing
- Scientific explanation
- etc.

### Step 2: Design Your Data Format

Create a structured format that encourages the desired reasoning pattern, similar to our thought/solution format.

### Step 3: Create a Generation Script

Copy and modify one of our existing scripts:

```bash
cp generate_ethical_data.py generate_my_objective_data.py
```

Then edit it to implement your objective function and prompt template.

### Step 4: Document Your Approach

Create documentation explaining:
- Your objective function
- The data format
- How to generate examples
- How to validate results

## Conclusion

Congratulations! By following this tutorial, you've learned how to:
1. Set up the environment for working with this repository
2. Download and process data from CommonCrawl
3. Generate synthetic training examples
4. Customize the generation process
5. Validate your examples
6. Contribute your examples back to the repository

Your contribution helps build a valuable resource for the entire AI community. Thank you for participating in this collaborative effort!

## Troubleshooting

### Common Issues

#### Ollama Connection Issues

If you encounter errors connecting to Ollama:
```
ERROR: Could not connect to Ollama server at http://localhost:11434
```

Solutions:
- Ensure Ollama is running: `ollama serve`
- Check if your Ollama host is correct in the `.env` file
- Try using a different port if you're running Ollama on a custom port

#### Model Not Found

If you get an error that the model doesn't exist:
```
ERROR: Model [model_name] not found
```

Solutions:
- List available models: `ollama list`
- Pull the model you want to use: `ollama pull llama3`
- Update your `.env` file to use an available model

#### Memory Issues

If you encounter memory errors during generation:
```
ERROR: CUDA out of memory
```

Solutions:
- Reduce batch size in the `.env` file
- Use a smaller model
- Process fewer examples at once: `--count 5`

#### JSON Parsing Errors

If you see JSON parsing errors in your generated examples:
```
ERROR: Invalid JSON in generated example
```

Solutions:
- Adjust temperature to a lower value (e.g., 0.5)
- Use a different model that produces more consistent output
- Check and fix the format manually in problematic examples