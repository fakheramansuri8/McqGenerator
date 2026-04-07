import os
import PyPDF2
import json
import traceback

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader=PyPDF2.PdfReader(file)
            text=""
            for page in pdf_reader.pages:
                text+=page.extract_text()
            return text
            
        except Exception as e:
            raise Exception("error reading the PDF file")
        
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    
    else:
        raise Exception(
            "unsupported file format only pdf and text file supported"
            )

def get_table_data(quiz_str):
    try:
        # 1. Clean the string from potential markdown fences (common in AI outputs)
        if "```json" in quiz_str:
            quiz_str = quiz_str.split("```json")[1].split("```")[0].strip()
        elif "```" in quiz_str:
            quiz_str = quiz_str.split("```")[1].strip()
        
        # 2. Find the JSON boundaries if there is extra text
        start_idx = quiz_str.find('{')
        end_idx = quiz_str.rfind('}') + 1
        if start_idx != -1 and end_idx != 0:
            quiz_str = quiz_str[start_idx:end_idx]

        # 3. Convert the quiz from a str to dict
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []
        
        # iterate over the quiz dictionary and extract the required information
        for key, value in quiz_dict.items():
            mcq = value["mcq"]
            options = " || ".join(
                [
                    f"{option}-> {option_value}" for option, option_value in value["options"].items()
                ]
            )
            
            correct = value["correct"]
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})
        
        return quiz_table_data
        
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        # Return empty list instead of False to prevent DataFrame errors
        return []



