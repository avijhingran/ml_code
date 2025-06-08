import os
from src.openrouter_client import call_openrouter

# Agentic: Run a specific instruction on a file
def analyze_file(file_path, instruction, model="openchat/openchat-7b"):
    with open(file_path, 'r', errors='ignore') as f:
        content = f.read()

    prompt = f"{instruction}:\n\n{content}"
    return call_openrouter(prompt, model=model)


# Pipeline version (same as before, still supported)
def analyze_file_full(file_path, model="openchat/openchat-7b"):
    with open(file_path, 'r', errors='ignore') as f:
        content = f.read()

    return {
        "filename": os.path.basename(file_path),
        "summary": call_openrouter(f"Summarize this COBOL or JCL program:\n\n{content}", model),
        "variables": call_openrouter(f"Extract variables with types, roles, and meaning:\n\n{content}", model),
        "calls": call_openrouter(f"List other programs called and how:\n\n{content}", model),
        "mermaid": call_openrouter(f"Generate Mermaid flowchart in graph TD format:\n\n{content}", model)
    }


# For backward compatibility with main.py
def analyze_all_files(base_path, model="openchat/openchat-7b"):
    results = []
    for root, _, files in os.walk(base_path):
        for fname in files:
            if fname.endswith((".cob", ".jcl", ".sql", ".txt")):
                result = analyze_file_full(os.path.join(root, fname), model=model)
                results.append(result)
    return results
