# PDF Reference Counter with DSPy

This project provides a Python script that counts the number of references to a specific author within a PDF document. It is a practical demonstration of Hybrid LLM Coding, where the script combines the declarative power of the DSPy framework to handle unstructured data with traditional Python code for deterministic tasks.

## Core Concepts
- Hybrid LLM Coding: This approach combines the strengths of large language models (LLMs) and traditional code. The LLM is used for "fuzzy" tasks that require natural language understanding (like parsing messy citation formats), while Python code is used for "rigid" tasks that require precise logic (like counting, file handling, and section identification).
- [DSPy](https://dspy.ai/): The DSPy framework is used to program the LLM calls. It allows us to define clear input and output "signatures" for our tasks, making the LLM a reliable, predictable component of the overall pipeline.

## Getting StartedPrerequisitesYou need to have Python installed, along with the following libraries:
```
pip install dspy-ai langchain-community pypdf
```

You also need to have a local LLM server running via Ollama.
 1. Install Ollama: Follow the instructions on the [Ollama website](https://ollama.com/download/windows).
 2. Pull the LLM Model: This script is configured to use Llama 3.1. Open a terminal and run:
 ```
 ollama pull llama3.1:latest
```
 3. Start Ollama: Ensure the Ollama server is running in the background.
 
## Usage
1. Save the code provided below as a Python file (e.g., count_references.py)
2. Place the PDF file you want to analyze in the same directory and name it Paper.pdf.
3. Run the script from your terminal:
```
python count_references.py
```

 ### Customization
 You can easily modify the script for your specific needs by changing the variables at the bottom of the file:
 - pdf_file_path: Change this to the path of your PDF document.
 - author_to_find: Change this to the name of the author you want to count references for.


### More Info
Some useful information about Prompt Engineering and DSPY, with a focus on mapping data.
- https://www.dbreunig.com/2025/06/10/let-the-model-write-the-prompt.html
- https://www.youtube.com/watch?v=I9ZtkgYZnOw&t
