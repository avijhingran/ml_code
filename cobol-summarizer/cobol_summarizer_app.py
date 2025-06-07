import openai
import anthropic
from google.colab import files

# Upload a COBOL file
uploaded = files.upload()
filename = list(uploaded.keys())[0]

with open(filename, 'r') as f:
    cobol_code = f.read()

# Set your API keys
openai.api_key = "your-openai-key"
anthropic_client = anthropic.Anthropic(api_key="your-anthropic-key")

# Use OpenAI to summarize
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": f"Summarize this COBOL code:\n{cobol_code}"}
    ]
)
print("Summary:\n", response["choices"][0]["message"]["content"])
