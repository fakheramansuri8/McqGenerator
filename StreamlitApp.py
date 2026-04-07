import os
import json
import traceback
import pandas as pd
from utils import read_file,get_table_data
import streamlit as st
from langchain_community.callbacks import get_openai_callback
from MCQGenerator import get_mcq_chain
from logger import logging
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

# loading json file
import os
import json

# Define the absolute path for Response.json relative to this file
RESPONSE_FILE_PATH = os.path.join(os.path.dirname(__file__), 'Response.json')

with open(RESPONSE_FILE_PATH, 'r') as file:
    RESPONSE_JSON = json.load(file)

# configuration for page layout
st.set_page_config(page_title="AI MCQ Creator", page_icon="📝", layout="wide")

# Custom CSS for modern design
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .sidebar .sidebar-content {
        background-image: linear-gradient(#2e7bcf,#2e7bcf);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR CONFIGURATION ---
st.sidebar.title("🛠️ Model Configuration")

provider = st.sidebar.selectbox(
    "Choose Provider",
    ["OpenAI", "Google Gemini", "Local/Custom (OpenAI Compatible)"]
)

if provider == "OpenAI":
    api_key = st.sidebar.text_input("OpenAI API Key", type="password")
    model_name = st.sidebar.text_input("Model Name", value="gpt-3.5-turbo", help="e.g., gpt-4, gpt-4-turbo")
    base_url = None
elif provider == "Google Gemini":
    api_key = st.sidebar.text_input("Gemini API Key", type="password")
    model_name = st.sidebar.text_input("Model Name", value="gemini-1.5-flash", help="e.g., gemini-1.5-pro")
    base_url = None
else:
    api_key = st.sidebar.text_input("API Key (if needed)", type="password")
    model_name = st.sidebar.text_input("Model Name", placeholder="e.g., llama3")
    base_url = st.sidebar.text_input("Base URL", placeholder="e.g., http://localhost:1234/v1")

# Set a fixed default temperature for consistency
temperature = 0.3

# --- MAIN UI ---
st.markdown("<h1 style='text-align: center; color: #2c3e50;'>✨ MCQs Creator Application</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7f8c8d;'>Generate high-quality multiple choice questions powered by LangChain 🦜⛓️</p>", unsafe_allow_html=True)

# Main Form
with st.form("user_inputs"):
    st.subheader("📋 Quiz Settings")
    
    uploaded_file = st.file_uploader("📤 Upload a PDF or Text file", type=['pdf', 'txt'])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        mcq_count = st.number_input("🔢 No. of MCQs", min_value=3, max_value=50, value=5)
    with col2:
        subject = st.text_input("📚 Subject", max_chars=20, placeholder="Python")
    with col3:
        tone = st.text_input("🎯 Complexity", max_chars=20, placeholder="Simple")
    
    button = st.form_submit_button("🚀 Create MCQs")

# Workflow processing (OUTSIDE the form)
if button:
    if not api_key:
        st.sidebar.error("🔑 Please provide an API Key.")
    elif uploaded_file is not None and mcq_count and subject and tone:
        try:
            # 1. Initialize the LLM based on user selection
            if provider == "OpenAI":
                llm = ChatOpenAI(openai_api_key=api_key, model_name=model_name, temperature=temperature)
            elif provider == "Google Gemini":
                llm = ChatGoogleGenerativeAI(google_api_key=api_key, model=model_name, temperature=temperature)
            else:
                llm = ChatOpenAI(openai_api_key=api_key, model_name=model_name, temperature=temperature, openai_api_base=base_url)

            # 2. Get the Chain
            generate_evaluate_chain = get_mcq_chain(llm)

            # 3. Process
            with st.spinner("🧠 Generating your quiz with AI... Please wait."):
                text = read_file(uploaded_file)
                
                # Token callback only supports OpenAI
                if provider in ["OpenAI", "Local/Custom (OpenAI Compatible)"]:
                    with get_openai_callback() as cb:
                        response = generate_evaluate_chain(
                            {
                                "text": text,
                                "number": mcq_count,
                                "subject": subject,
                                "tone": tone,
                                "response_json": json.dumps(RESPONSE_JSON)
                            }
                        )
                    st.info(f"💡 **Usage Stats:** Tokens: {cb.total_tokens} | Cost: ${cb.total_cost:.4f}")
                else:
                    response = generate_evaluate_chain(
                        {
                            "text": text,
                            "number": mcq_count,
                            "subject": subject,
                            "tone": tone,
                            "response_json": json.dumps(RESPONSE_JSON)
                        }
                    )

                # 4. Display Results
                st.success("✅ MCQ Generation Complete!")
                if isinstance(response, dict):
                    quiz = response.get("quiz", None)
                    if quiz:
                        table_data = get_table_data(quiz)
                        if table_data: # Check if list is not empty
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            
                            tab1, tab2 = st.tabs(["📊 Generated Quiz", "📝 AI Analysis"])
                            with tab1:
                                st.table(df)
                                csv = df.to_csv(index=True).encode('utf-8')
                                st.download_button("📥 Download Quiz as CSV", data=csv, file_name=f"{subject}_MCQs.csv", mime="text/csv")
                            
                            with tab2:
                                st.markdown(f"### Review\n{response['review']}")
                        else: 
                            st.error("❌ The AI's response couldn't be parsed into a table. Please try again.")
                            st.text_area("Raw AI Output", value=quiz)
                    else: st.error("❌ No quiz data generated.")
                else: st.write(response)

        except Exception as e:
            st.error(f"⚠️ An error occurred: {str(e)}")
            with st.expander("Show Traceback"):
                st.write(traceback.format_exc())
    else:
        st.warning("⚠️ Please upload a file and fill in all fields.")





