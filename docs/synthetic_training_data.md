# Creating Synthetic Training Data for Specialized AI Capabilities

This document provides a comprehensive guide to creating synthetic training data for specialized AI capabilities using the tools and scripts in this repository. It focuses on the example of ethical reasoning, but the same principles can be applied to other objective functions.

## Why Create Synthetic Training Data?

Synthetic training data offers several advantages:

1. **Controlled Quality**: Ensures consistent formatting and quality standards
2. **Customized Objective Functions**: Trains models for specialized capabilities
3. **Structured Thought Process**: Encourages specific reasoning patterns
4. **Cost-Effective**: Leverages existing models to create training data for new models
5. **Data Availability**: Useful when real-world examples are scarce or proprietary

## General Workflow

The process of creating synthetic training data involves:

1. **Define your objective function** - What capability do you want the AI to learn?
2. **Acquire source material** - Gather real-world text that contains relevant content
3. **Design a prompt template** - Create a structured format for the desired capability
4. **Generate synthetic examples** - Use existing AI models to create training data
5. **Validate and refine** - Ensure quality and consistency of the generated data

## Example: Ethical Reasoning

This repository includes an implementation for creating ethical reasoning training data, which follows these steps:

### 1. Define the Objective Function

For ethical reasoning, our objective function includes:
- Thorough analysis of ethical implications
- Consideration of multiple perspectives
- Application of ethical principles
- Clear recommendations and conclusions

We structure this using a two-part format:
1. `<|begin_of_thought|>` - Detailed analysis
2. `<|begin_of_solution|>` - Conclusions and recommendations

### 2. Acquire Source Material

We use CommonCrawl as a source of real-world text containing ethical content:

```bash
# Download and process CommonCrawl data
python download_cc_sample.py --size 100
```

This script:
- Downloads WARC files from CommonCrawl
- Extracts text content
- Filters for passages that contain ethical keywords
- Saves to a more accessible format

### 3. Design a Prompt Template

Our template for ethical reasoning looks like:

```
Analyze the following text passage from an ethical perspective, focusing on considerations related to [CATEGORY]:

[PASSAGE]

Structure your reasoning into two main sections:
<|begin_of_thought|>
(Your detailed ethical analysis here)
<|end_of_thought|>

<|begin_of_solution|>
(Your ethical conclusions and recommendations here)
<|end_of_solution|>
```

This template encourages:
- In-depth analysis in the "thought" section
- Clear, actionable conclusions in the "solution" section
- Focus on specific ethical categories (privacy, fairness, etc.)

### 4. Generate Synthetic Examples

We generate examples using:

```bash
# Generate a batch of examples
python generate_ethical_data.py --count 20

# Or generate a single example for testing
python generate_single_example.py --output data/test_example.json
```

The generation process:
1. Identifies ethical content in the CommonCrawl data
2. Categorizes content by ethical themes (privacy, fairness, etc.)
3. Uses an existing AI model to generate structured ethical reasoning
4. Saves the results in a standardized format

### 5. Validate and Refine

The resulting data should be validated for:
- Adherence to the desired format
- Quality of reasoning
- Diversity of scenarios and perspectives
- Absence of problematic content

The `ethical_agent.py` script provides a way to test and demonstrate the type of reasoning we're aiming to teach.

## Example Output

A sample training example for ethical reasoning looks like:

```json
{
  "passage": "Companies track user browsing habits to target advertisements without explicit consent",
  "category": "privacy",
  "reasoning": "<|begin_of_thought|>\nI'll analyze this ethical situation concerning privacy in several steps:\n\n1. **Identifying key ethical concerns**:\n   This scenario involves \"Companies track user browsing habits to target advertisements without explicit consent\" which raises important questions about privacy.\n   The core ethical concerns include respect for individual rights, potential consequences, and relevant ethical principles.\n\n2. **Applying ethical principles**:\n   - People have a right to control their personal information\n   - Informed consent is necessary for ethical data collection\n   - There should be transparency about how data is used\n\n3. **Considering multiple perspectives**:\n   - From an individual's perspective: People have expectations about how their information is handled and used.\n   - From an organizational perspective: There may be legitimate purposes for the activities described.\n   - From a societal perspective: Practices that become normalized can have broader implications.\n\n4. **Examining consequences**:\n   The short-term consequences might include immediate benefits or harms to individuals.\n   The long-term consequences could involve erosion of trust, normalization of problematic practices, or setting precedents.\n\n5. **Weighing competing values**:\n   This situation involves a tension between values like efficiency and utility versus respect for individual rights.\n   There may also be conflicts between short-term benefits and long-term ethical concerns.\n<|end_of_thought|>\n\n<|begin_of_solution|>\nBased on thorough ethical analysis of \"Companies track user browsing habits to target advertisements without explicit consent\" focused on privacy, I conclude:\n\n1. **Ethical Assessment**: \n   This situation raises significant concerns about respect for individual autonomy and informed consent.\n   \n2. **Key Considerations**:\n   - The practice should be evaluated based on transparency, consent, and proportionality\n   - Both intended and unintended consequences must be considered\n   - Alternative approaches that better respect ethical principles should be explored\n\n3. **Recommendations**:\n   - Implement clear transparency measures to ensure informed decision-making\n   - Establish meaningful consent mechanisms that give individuals real choice\n   - Adopt ethical frameworks that prioritize human dignity over pure utility\n   - Regularly review practices to ensure alignment with evolving ethical standards\n\n4. **Balanced Approach**:\n   While there may be legitimate purposes for certain practices, these must be balanced against ethical obligations to respect individual rights and prevent harm. Ethical solutions often require thoughtful compromise and ongoing evaluation.\n<|end_of_solution|>"
}
```

## Extending to Other Capabilities

This framework can be adapted for other specialized capabilities:

### Example: Mathematical Reasoning

1. **Objective**: Step-by-step mathematical problem solving
2. **Source Material**: Mathematics textbooks, problem sets
3. **Format**:
   ```
   <|begin_of_thought|>
   Detailed mathematical reasoning steps
   <|end_of_thought|>
   
   <|begin_of_solution|>
   Final mathematical solution
   <|end_of_solution|>
   ```

### Example: Legal Analysis

1. **Objective**: Structured legal reasoning
2. **Source Material**: Legal cases, statutes, regulations
3. **Format**:
   ```
   <|begin_of_thought|>
   Legal analysis considering precedents, statutes, and principles
   <|end_of_thought|>
   
   <|begin_of_solution|>
   Legal conclusion and recommendations
   <|end_of_solution|>
   ```

## Best Practices

1. **Define Clear Objectives**: Be specific about what capability you want to teach
2. **Quality over Quantity**: Fewer high-quality examples are better than many low-quality ones
3. **Diverse Examples**: Include a variety of scenarios to prevent overfitting
4. **Iterative Refinement**: Test and improve your templates based on results
5. **Ethical Considerations**: Ensure your training data doesn't perpetuate harmful biases

## Technical Implementation

The repository includes several key components for implementing this workflow:

- **Data Acquisition**: `download_cc_sample.py`
- **Content Filtering**: `extract_ethical_content()` in `generate_ethical_data.py`
- **Categorization**: `categorize_ethical_content()` in `generate_ethical_data.py`
- **Generation**: `generate_ethical_reasoning()` in `generate_ethical_data.py`
- **Agent Implementation**: `ethical_agent.py` for demonstrating the capability

These components can be modified and extended to support different objective functions beyond ethical reasoning.

## Getting Started

1. Clone the repository
2. Install dependencies
3. Download a sample of CommonCrawl data
4. Generate synthetic examples
5. Test with the ethical agent
6. Adapt the framework for your own objectives

For detailed instructions, see the main [README.md](../README.md) file.