import os
import traceback
from src.analyzer import analyze_file
from src.doc_writer import save_report

def agentic_analyze(file_path, model="openchat/openchat-7b"):
    """
    Agentic loop to analyze a single file using planning + execution.
    Returns result dict or error note.
    """
    plan = [
        "Summarize the program",
        "Identify variables and types",
        "Find other programs called",
        "Generate a mermaid flowchart"
    ]
    file_name = os.path.basename(file_path)
    results = {}

    for step in plan:
        try:
            print(f"Thinking: {step} for {file_name}")
            result = analyze_file(file_path, step, model=model)
            results[step] = result
        except Exception as e:
            print(f"Error in step '{step}' for {file_name}: {e}")
            traceback.print_exc()
            results[step] = "Error during execution"

    return results


def run_agent_loop(project_dir, output_dir="output", model="openchat/openchat-7b"):
    """
    Runs the agent loop over all source code files in project_dir.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    summaries = []
    for root, _, files in os.walk(project_dir):
        for fname in files:
            if fname.endswith((".cob", ".jcl", ".sql", ".txt")):
                full_path = os.path.join(root, fname)
                print(f"Analyzing {fname}...")
                result = agentic_analyze(full_path, model=model)
                summaries.append((fname, result))
                save_report(fname, result, output_dir)

    print(f"Agentic analysis complete. Reports saved to '{output_dir}/'")
