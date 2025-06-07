import os
import anthropic
import openai
import getpass

# --- Secure API key input ---
openai_key = getpass.getpass("🔐 Enter your OpenAI API key (starts with sk-...): ")
anthropic_key = getpass.getpass("🔐 Enter your Anthropic API key: ")

# --- Initialize OpenAI + Anthropic clients ---
client = openai.OpenAI(api_key=openai_key)
anthropic_client = anthropic.Anthropic(api_key=anthropic_key)

# --- Ask for COBOL file path ---
file_path = input("\n📄 Enter the path to your COBOL file: ").strip()

# --- Check if file exists ---
if not os.path.isfile(file_path):
    print(f"❌ Error: File '{file_path}' not found.")
    exit()

# --- Read COBOL file ---
with open(file_path, 'r') as f:
    cobol_code = f.read()

# --- Ask user for model selection ---
print("\n🤖 Choose a model to summarize COBOL:")
print("1. OpenAI gpt-3.5-turbo")
print("2. Anthropic Claude")
choice = input("Enter 1 or 2: ").strip()

if choice == "1":
    model_used = "openai"
elif choice == "2":
    model_used = "anthropic"
else:
    print("⚠️ Invalid choice. Defaulting to OpenAI gpt-3.5-turbo.")
    model_used = "openai"

# --- Summarize the COBOL code ---
print(f"\n📝 Summarizing using {model_used.upper()}...\n")

if model_used == "openai":
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"Summarize this COBOL code:\n{cobol_code}"}
        ],
        temperature=0.3
    )
    summary = response.choices[0].message.content

else:
    response = anthropic_client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=500,
        messages=[
            {"role": "user", "content": f"Summarize this COBOL code:\n{cobol_code}"}
        ]
    )
    summary = response.content[0].text

# --- Output the summary ---
print("=== ✅ COBOL Summary ===\n")
print(summary)
