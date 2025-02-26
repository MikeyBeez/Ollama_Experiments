#!/usr/bin/env python
"""
Generate a single ethical reasoning example using pre-defined content
"""

import os
import json
import argparse
import requests

# Constants
OLLAMA_API = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "deepseek-r1"

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Generate a single ethical reasoning example")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL,
                      help=f"Ollama model to use (default: {DEFAULT_MODEL})")
    parser.add_argument("--output", type=str, default="ethical_example.json",
                      help="Output file path (default: ethical_example.json)")
    return parser.parse_args()

def ensure_dir(file_path):
    """Create directory for file if it doesn't exist"""
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

def generate_ethical_reasoning(passage, category, model=DEFAULT_MODEL, timeout=60):
    """Generate ethical reasoning for a passage using Ollama API"""
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
        print(f"Sending request to Ollama API with model: {model}")
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

def main():
    args = parse_args()
    
    # Predefined ethical scenarios - shorter and simpler for testing
    scenarios = [
        {
            "passage": "Companies track online activities to deliver personalized ads.",
            "category": "privacy"
        },
        {
            "passage": "AI systems make hiring decisions without human oversight.",
            "category": "fairness"
        },
        {
            "passage": "Video games use random rewards to encourage continued spending.",
            "category": "harm"
        },
        {
            "passage": "Websites collect user data without clear consent.",
            "category": "autonomy"
        },
        {
            "passage": "Social media platforms filter content based on user preferences.",
            "category": "deception"
        }
    ]
    
    # Use a specific scenario directly without user input
    selected_scenario = scenarios[3]  # Autonomy
    print(f"Using scenario ({selected_scenario['category']}):\n{selected_scenario['passage']}\n")
    
    # Generate reasoning with longer timeout
    reasoning = generate_ethical_reasoning(
        selected_scenario['passage'], 
        selected_scenario['category'],
        args.model,
        timeout=120
    )
    
    # Print result
    print("\n----- Generated Ethical Reasoning -----\n")
    print(reasoning)
    print("\n--------------------------------------\n")
    
    # Save to file
    output_file = args.output
    ensure_dir(output_file)
    
    example = {
        "passage": selected_scenario['passage'],
        "category": selected_scenario['category'],
        "reasoning": reasoning
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(example, f, indent=2)
    
    print(f"Saved output to {output_file}")

if __name__ == "__main__":
    main()