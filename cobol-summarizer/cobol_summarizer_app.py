import os
import getpass
import openai
import anthropic
import requests

# === 🔐 Securely prompt for API keys ===
openai_key = getpass.getpass("🔐 Enter your OpenAI API key (or press Enter to skip): ")
anthropic_key = getpass.getpass("🔐 Enter your Anthropic API key (or press Enter to skip): ")
hf_token = getpass.getpass("🔐 Enter your Hugging Face API key (or press Enter to skip): ")

# === 🧠 Initialize API clients ===
client = openai.OpenAI(api_key=openai_key) if openai_key else None
anthropic_client = anthropic.Anthropic(api_key=anthropic_key) if anthropic_key else None

# === 📄 Get COBOL file path ===
file_path = input("\n📂 Enter the path to your COBOL file (e.g., my_sample.cbl): ").strip()

if not os.path.isfile(file_path):
    print(f"❌ Error: File '{file_path}' not found.")
    exit()

with open(file_path, 'r') as f:
    cobol_code = f.read()

# === 🤖 Choose model ===
print("\nChoose a model to summarize COBOL:")
print("1. OpenAI GPT-4 / GPT-3.5")
print("2. Anthropic Claude")
print("3. Hugging Face Mistral-7B-Instruct")
choice = input("Enter 1, 2 or 3: ").strip()

# === 📝 Create the prompt ===
prompt = f"Summarize the following COBOL code in plain English:\n\n{cobol_code}\n\nSummary:"

# === 🔁 Call the selected model ===
print(f"\n📡 Generating summary using option {choice}...\n")

summary = ""

try:
    if choice == "1":
        if not openai_key:
            raise ValueError("OpenAI API key not provided.")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Change to gpt-4 if your account has access
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        summary = response.choices[0].message.content

    elif choice == "2":
        if not anthropic_key:
            raise ValueError("Anthropic API key not provided.")
        response = anthropic_client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        summary = response.content[0].text

    elif choice == "3":
        if not hf_token:
            raise ValueError("Hugging Face API key not provided.")
        API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct"
        headers = {
            "Authorization": f"Bearer {hf_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 400,
                "temperature": 0.7,
                "return_full_text": False
            }
        }
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code != 200:
            raise Exception(f"Hugging Face API error: {response.status_code} {response.text}")
        result = response.json()
        summary = result[0]["generated_text"] if isinstance(result, list) else result.get("generated_text", "")

    else:
        print("⚠️ Invalid choice. Please enter 1, 2, or 3.")
        exit()

except Exception as e:
    print(f"❌ Error during summarization: {e}")
    exit()

# === ✅ Output the result ===
print("\n=== COBOL Summary ===\n")
print(summary)
