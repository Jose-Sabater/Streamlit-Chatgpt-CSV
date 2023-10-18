import streamlit as st
import pandas as pd
from llm import LLMGenie

database_selection = ["Snowflake"]
filename = None
response = None

st.set_page_config(
    page_title="Genai AI",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state for questions and answers
if "questions" not in st.session_state:
    st.session_state.questions = []
if "answers" not in st.session_state:
    st.session_state.answers = []


st.title("Genai Chat Demo")
st.write(
    "This is a demo of the Genai Chatbot. Please enter your question below and click on 'Submit' to get an answer."
)
st.write("## File upload")
st.write(
    """
    Instructions:  
    - First row must be a header row  
    - Use comma as a separator"""
)

uploaded_file = st.file_uploader(
    "Upload your file here (max 200mb)", type=["xlsx", "csv"]
)

if uploaded_file is not None:
    filename = uploaded_file.name
    try:
        df = pd.read_csv(uploaded_file)
        st.selectbox("(Optional) Select your main column", df.columns)
        data_description = st.text_input(
            "(Optional) Describe your data: ", placeholder="Brief description"
        )

    except Exception as e:
        st.write("Please upload a csv or xlsx file")

if filename:
    database_selection.append(filename)

selection = st.multiselect(
    "Select up to 2 datasources to answer questions from",
    database_selection,
    max_selections=2,
)

model_name = st.text_input(
    "What model would you like to use?",
    placeholder="gpt-3.5-turbo",
    value="gpt-3.5-turbo",
)

question = st.text_input("Write your question below", placeholder="Type here")

# Add a submit button for the question
if st.button("Submit Question"):
    if uploaded_file:
        genie = LLMGenie(question, df, model_name)
        response = genie.answer_question()

if response:
    st.write(response)

# Display history of questions and answers
st.write("## History")
for q, a in zip(st.session_state.questions, st.session_state.answers):
    st.write(f"Q: {q}")
    st.write(f"A: {a}")
# TODO
# IF data larger than x amount of columns, build SQLite
