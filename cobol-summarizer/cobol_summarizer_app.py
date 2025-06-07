import os
import anthropic
import openai

# --- Set your API keys ---
# For OpenAI (new SDK format)
client = openai.OpenAI(api_key="your-openai-api-key")

# For Anthropic
anthropic_client = anthropic.Anthropic(api_key="your-anthropic-api-key")

# --- Ask for file location ---
file_path = input("Enter the path to your COBOL file: ").strip()

# --- Check if file exists ---
if not os.path.isfile(file_path):
    print(f" Error: File '{file_path}' not found.")
    exit()

# --- Read the COBOL file ---
with open(file_path, 'r') as f:
    cobol_code = f.read()

# --- Ask user for model selection ---
print("\nChoose a model to summarize COBOL:")
print("1. OpenAI GPT-4")
print("2. Anthropic Claude")
choice = input("Enter 1 or 2: ").strip()

if choice == "1":
    model_used = "openai"
elif choice == "2":
    model_used = "anthropic"
else:
    print("Invalid choice. Defaulting to OpenAI GPT-4.")
    model_used = "openai"

# --- Generate summary ---
print(f"\nSummarizing using {model_used.upper()}...\n")

if model_used == "openai":
    response = client.chat.completions.create(
        model="gpt-4",
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

# --- Output summary ---
print("=== COBOL Summary ===\n")
print(summary)
