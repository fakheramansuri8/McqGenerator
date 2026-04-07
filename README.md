---
title: MCQ Generator 📝✨
emoji: 🦜
colorFrom: blue
colorTo: green
sdk: streamlit
app_file: StreamlitApp.py
pinned: false
---

# MCQs Creator Application 📝✨

A professional, production-ready Multiple Choice Question (MCQ) generator powered by **LangChain (LCEL)** and **Streamlit**. Supporting various LLM providers with a fully dynamic, UI-driven configuration.

## ✨ Features
- **Multi-Model Support**: Use OpenAI (GPT-4/3.5), Google Gemini (Pro/Flash), or any local OpenAI-compatible model (Llama 3, etc.).
- **Dynamic UI Configuration**: Input your API keys and select models directly in the app. No `.env` files required!
- **LCEL Architecture**: High-reliability MCQ generation using LangChain Expression Language.
- **Smart Analysis**: Automatic English grammar and complexity evaluation of generated quizzes.
- **Modern UI**: Sleek, wide layout with real-time spinners and status indicators.
- **Export Options**: Download your generated MCQs as professional CSV files.

## 🛠️ Tech Stack
- **Core**: Python 3.10+
- **Agentic Logic**: LangChain (LCEL)
- **Interface**: Streamlit
- **LLM Providers**: OpenAI, Google Google-GenAI, Local via LM Studio/Ollama

## 📂 Project Structure
```text
mcqgenerator/
├── MCQGenerator.py     # Core MCQ generation logic (LCEL)
├── StreamlitApp.py      # Main UI and application entry point
├── utils.py            # PDF/Text processing and JSON parsing
├── logger.py            # Application logging
├── Response.json        # Standard MCQ response format template
├── requirements.txt     # Python dependencies
└── README.md            # Documentation
```

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/fakheramansuri8/McqGenerator
```

### 2. Installation
It is highly recommended to use a virtual environment to manage dependencies:
```bash
# Create venv
python3 -m venv venv

# Activate venv
source venv/bin/activate  # MacOS/Linux
# .\venv\Scripts\activate # Windows

# Install requirements
pip install -r requirements.txt
```

### 3. Run the Application
The application handles all API keys and model settings via the UI sidebar.
```bash
streamlit run StreamlitApp.py
```

## 📝 How to Use
1.  **Sidebar Config**: Provide your **API Key** and type in the **Model Name** you wish to use.
2.  **Upload Content**: Upload a PDF or Text file containing the information you want to test.
3.  **Quiz Settings**: Choose the number of MCQs, the subject, and the target complexity.
4.  **Generate**: Click "Create MCQs" and wait for the results!
5.  **Review & Export**: View the generated table, read the AI's analysis, and download the CSV.

## ⚠️ Security Note
Your API keys are processed only within your browser session and are never stored on a server. However, always exercise caution when inputting credentials!
