from setuptools import find_packages,setup

setup(
    name='mcqgenerator',
    version='0.0.1',
    author='fakhera',
    author_email='[EMAIL_ADDRESS]',
    install_requires=["openai","langchain","langchain-openai","langchain-google-genai","langchain-community","streamlit","PyPDF2","pandas"],
    packages=find_packages()
)