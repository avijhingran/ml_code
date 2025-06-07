import streamlit as st
import openai
import anthropic

# --- Setup API keys ---
openai.api_key = "your_openai_api_key"
anthropic_client = anthropic.Anthropic(api_key="your_anthropic_api_key")

# --- Streamlit UI ---
st.set_page_config(page_title="COBOL Summarizer", layout="centered")
st.title("📄 COBOL Code Summarizer")
st.write("Upload a COBOL file to get a summary of its functionality.")

# File upload
uploaded_file = st.file_uploader("Choose a COBOL file", type=["cbl", "cob", "txt"])

# Model selection
model_choice = st.selectbox("Choose a model to summarize with:", ["OpenAI GPT-4", "Anthropic Claude"])

# When file is uploaded and button clicked
if uploaded_file is not None:
    cobol_code = uploaded_file.read().decode("utf-8")

    if st.button("Generate Summary"):
        with st.spinner("Summarizing..."):

            try:
                if model_choice == "OpenAI GPT-4":
                    response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=[
                            {"role": "user", "content": f"Summarize this COBOL code:\n{cobol_code}"}
                        ],
                        temperature=0.3
                    )
                    summary = response["choices"][0]["message"]["content"]

                else:  # Anthropic Claude
                    response = anthropic_client.messages.create(
                        model="claude-3-opus-20240229",
                        max_tokens=500,
                        messages=[
                            {"role": "user", "content": f"Summarize this COBOL code:\n{cobol_code}"}
                        ]
                    )
                    summary = response.content[0].text

                st.success("Summary generated successfully!")
                st.text_area("Summary Output", value=summary, height=300)

            except Exception as e:
                st.error(f"Error: {e}")
