import json
import subprocess
import os

def call_openrouter(prompt, model="mistralai/mistral-7b-instruct"):
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }
    headers = {
        "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
        "Content-Type": "application/json"
    }
    cmd = [
        "curl", "-s", "-X", "POST", "https://openrouter.ai/api/v1/chat/completions",
        "-H", f"Authorization: Bearer {headers['Authorization']}",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(data)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return json.loads(result.stdout)["choices"][0]["message"]["content"]
    except Exception:
        return "Error parsing OpenRouter response"
