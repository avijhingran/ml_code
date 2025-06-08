import os
from src.openrouter_client import call_openrouter

def analyze_file(file_path):
    with open(file_path, 'r', errors='ignore') as f:
        content = f.read()

    return {
        "filename": os.path.basename(file_path),
        "summary": call_openrouter(f"Summarize this COBOL or JCL program:\n\n{content}"),
        "variables": call_openrouter(f"Extract variables with types, roles, and meaning:\n\n{content}"),
        "calls": call_openrouter(f"List other programs called and how:\n\n{content}"),
        "mermaid": call_openrouter(f"Generate Mermaid flowchart in graph TD format:\n\n{content}")
    }

def analyze_all_files(base_path):
    results = []
    for root, _, files in os.walk(base_path):
        for fname in files:
            if fname.endswith((".cob", ".jcl", ".sql", ".txt")):
                result = analyze_file(os.path.join(root, fname))
                results.append(result)
    return results
