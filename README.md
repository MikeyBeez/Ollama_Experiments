# Simple Ollama Agent

This is a simple demo of an agent that uses the Ollama API to chat with language models.

## Requirements

- Python 3.6+
- Ollama installed and running locally (or remotely)
- A language model loaded in Ollama (e.g., deepseek-r1)

## Setup

1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install requests
   ```

3. Configure the environment:
   - Edit the `.env` file to set your preferred model and Ollama host

## Usage

Run the demo script:
```bash
python simple_agent.py
```

This will run a simple conversation with the agent using the specified model.

## Customization

- To use a different model, update the `OLLAMA_MODEL` in the `.env` file
- To add more functionality, extend the `AgentAPI` class with additional methods
- To customize the demo conversation, modify the `demo_messages` list in the `main()` function

## Available Models

To see what models are available on your Ollama instance, run:
```bash
ollama list
```

## Project Structure

- `simple_agent.py` - Main script with the agent implementation
- `.env` - Environment configuration
- `api_document.md` - Documentation of the full Ollama_Agents API (reference only)