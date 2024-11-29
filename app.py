import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json
import os

# This function creates an instance of a generative model called 'gemini-pro'. It then uses this model to generate content based on the input provided and returns the generated response text.

os.environ['GOOGLE_API_KEY'] = 'GOOGLE_API_KEY'
load_dotenv() ## load all our environment variables
GOOGLE_API_KEY = 'GOOGLE_API_KEY'
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_repsonse(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#This function reads a PDF file, extracts text from each page, and concatenates it into a single string. It uses the pdf.Pdf Reader class to access the pages and extract text.
# 3. Prompt Template

input_prompt="""
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving thr resumes. Assign the percentage Matching based 
on Jd and
the missing keywords with high accuracy
resume:{text}
description:{jd}
I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
"""
# This string defines a prompt template for the generative model. It instructs the model to act as an experienced ATS and evaluate a resume against a job description. The model is expected to return a JSON-like string indicating the percentage match, missing keywords, and a profile summary.

## 4. Streamlit app: The Streamlit app interface includes a title and instructions for users. Users can input the job description (jd) and upload their resume as a PDF file (uploaded_file). The submit button triggers the processing.
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

submit = st.button("Submit")
# 5. Processing and Output
# When the submit button is pressed, and a file is uploaded, the text is extracted from the uploaded resume PDF using input_pdf_text. 
# Then, the get_gemini_repsonse function generates a response based on the input prompt and extracted text.
# The response, which contains the evaluation and suggestions, is displayed in the app as a subheader.
if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_repsonse(input_prompt)
        st.subheader(response)
