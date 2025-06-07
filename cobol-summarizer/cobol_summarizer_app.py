import os
import requests
import openai
import anthropic

# --- Collect API keys ---
openai_key = input("Enter your OpenAI API key (or leave blank to skip): ").strip()
anthropic_key = input("Enter your Anthropic API key (or leave blank to skip): ").strip()
openrouter_key = input("Enter your OpenRouter API key (or leave blank to skip): ").strip()

# --- Select COBOL file ---
file_path = input("\n📄 Enter the path to your COBOL file: ").strip()
if not os.path.isfile(file_path):
    print(f" Error: File '{file_path}' not found.")
    exit()

with open(file_path, 'r') as f:
    cobol_code = f.read()

# --- Choose model source ---
print("\n Choose a model to summarize COBOL:")
print("1. OpenAI (GPT-4 / GPT-3.5)")
print("2. Anthropic Claude")
print("3. OpenRouter (e.g., Mixtral, GPT-4, Claude, etc.)")
choice = input("Enter 1, 2, or 3: ").strip()

# --- Prepare business-oriented prompt ---
prompt = (
    "You are a business analyst reviewing legacy COBOL code. "
    "Summarize what this program does from a functional and business perspective. "
    "Avoid technical jargon, variables, or COBOL syntax. "
    "Explain the purpose, business rules, and real-world outcome in plain English.\n\n"
    f"COBOL Code:\n{cobol_code}\n\n"
    "Business Summary:"
)

print(f"\n Summarizing using option {choice}...\n")
summary = ""
try:
    if choice == "1":
        if not openai_key:
            raise ValueError("OpenAI API key not provided.")
        client = openai.OpenAI(api_key=openai_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        summary = response.choices[0].message.content

    elif choice == "2":
        if not anthropic_key:
            raise ValueError("Anthropic API key not provided.")
        client = anthropic.Anthropic(api_key=anthropic_key)
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        summary = response.content[0].text

    elif choice == "3":
        if not openrouter_key:
            raise ValueError("OpenRouter API key not provided.")
        
        headers = {
            "Authorization": f"Bearer {openrouter_key}",
            "Content-Type": "application/json"
        }

        # You can customize the model here (e.g., gpt-4, mistral, claude)
        model = "mistralai/mixtral-8x7b-instruct"

        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        data = response.json()

        if "choices" in data:
            summary = data["choices"][0]["message"]["content"]
        else:
            raise ValueError(f"OpenRouter error: {data}")

    else:
        print(" Invalid selection.")
        exit()

except Exception as e:
    print(f"Error during summarization: {e}")
    exit()

# --- Output result ---
print("\n=== COBOL Summary ===\n")
print(summary)
