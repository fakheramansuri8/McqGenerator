import os
import json
import traceback
import pandas as pd
from utils import read_file,get_table_data
from logger import logging

# importing necessary packages from langchain
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.runnables import RunnablePassthrough

def get_mcq_chain(llm):
    """
    Creates a LangChain sequence for generating and evaluating MCQs using LCEL.
    """
    
    # MCQ Generation Prompt
    quiz_template = """
    Text:{text}
    You are an expert MCQ maker. Given the above text, it is your job to \
    create a quiz of {number} multiple choice questions for {subject} students in {tone} tone. 
    Make sure the questions are not repeated and check all the questions to be conforming the text as well.
    Make sure to format your response like RESPONSE_JSON below and use it as a guide. \
    Ensure to make {number} MCQs
    ### RESPONSE_JSON
    {response_json}
    """
    
    quiz_generation_prompt = PromptTemplate(
        input_variables=["text", "number", "subject", "tone", "response_json"],
        template=quiz_template)

    # Quiz chain (Generation)
    quiz_chain = quiz_generation_prompt | llm | StrOutputParser()

    # Quiz evaluation Prompt
    evaluation_template = """
    You are an expert English grammarian and writer. Given a Multiple Choice Quiz for {subject} students.
    You need to evaluate the complexity of the question and give a complete analysis of the quiz if the students
    will be able to understand the questions and answer them. Only use at max 50 words for complexity analysis. 
    if the quiz is not at par with the cognitive and analytical abilities of the students,
    update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
    Quiz_MCQs:
    {quiz}

    Check from an expert English Writer of the above quiz:
    """

    quiz_evaluation_prompt = PromptTemplate(input_variables=["subject", "quiz"], template=evaluation_template)

    # Evaluation chain
    evaluation_chain = quiz_evaluation_prompt | llm | StrOutputParser()

    # Overall chain logic via a function (since SequentialChain is legacy)
    def invoke_chains(inputs):
        # 1. Generate Quiz
        quiz_response = quiz_chain.invoke(inputs)
        # 2. Evaluate Quiz
        eval_inputs = {"subject": inputs["subject"], "quiz": quiz_response}
        review_response = evaluation_chain.invoke(eval_inputs)
        
        return {
            "quiz": quiz_response,
            "review": review_response
        }

    return invoke_chains


