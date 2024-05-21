# McqGenerator
## Overview

The Automated MCQ Generator streamlines the creation of multiple-choice questions using advanced NLP techniques. Utilizing OpenAI's GPT-3.5 Turbo and LangChain, this project automates MCQ generation, making it ideal for educators and students in e-learning environments.

## Features

- **Automated MCQ Generation**: Create MCQs from input text using cutting-edge language models.
- **Customization**: Adjust parameters like subject, difficulty, and question type.
- **User-Friendly Interface**: Streamlit-based web app for easy interaction.
- **Scalability**: Handles large datasets, suitable for educational institutions.

## Technologies Used

- **Languages**: Python
- **Libraries**: OpenAI, LangChain, Streamlit, PyPDF2, Scikit-learn, TensorFlow
- **Models**: OpenAI GPT-3.5 Turbo

## Installation

2. **Create and Activate a Virtual Environment**:
   ```bash
   python -m venv env
   # Windows
   .\env\Scripts\activate
   # macOS/Linux
   source env/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up OpenAI API Key**:
   - Obtain your API key from [OpenAI](https://www.openai.com/api/).
   - Create a `.env` file:
     ```plaintext
     OPENAI_API_KEY=your_openai_api_key
     ```

## Usage

1. **Run the Streamlit App**:
   ```bash
   streamlit run app.py
   ```

## Project Structure

- **streamlitApp.py**: Main Streamlit application.
- **mcqgenrator.py**: Logic for generating MCQs.
- **requirements.txt**: Project dependencies.
- **README.md**: Project documentation.

