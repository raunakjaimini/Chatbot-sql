from dotenv import load_dotenv
load_dotenv()  # Load all the environment variables

import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# Configure GenAI Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Model and provide queries as response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

# Function to retrieve query from the database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

# Define Your Prompt
prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT 
    where CLASS="Data Science"; 
    also the sql code should not have ``` in beginning or end and sql word in output
    """
]

# Streamlit App
st.set_page_config(page_title="Chat-Mate SQL Query Retriever", page_icon="🌟", layout="centered")
st.markdown(
    """
    <style>
    body {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    .css-18e3th9 {
        padding: 2rem;
    }
    .css-1d391kg {
        background-color: #444444;
        border-radius: 10px;
        padding: 20px;
    }
    .css-1d391kg h1 {
        color: #FFD700;
    }
    .css-1d391kg h2 {
        color: #FFFFFF;
    }
    .css-1d391kg input {
        background-color: #333333;
        color: #FFD700;
        border: 2px solid #FFD700;
        border-radius: 5px;
    }
    .css-1d391kg button {
        background-color: #FFD700;
        color: #333333;
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
    }
    .css-1d391kg button:hover {
        background-color: #FFA500;
    }
    .css-1d391kg .stButton {
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.header("Chat-Mate SQL Query Retriever 🌟")

question = st.text_input("Ask your question:", key="input")

submit = st.button("Retrieve SQL Query")

if submit:
    with st.spinner("Generating SQL query..."):
        response = get_gemini_response(question, prompt)
        st.success(f"Generated SQL Query: `{response}`")
    
    with st.spinner("Fetching data from the database..."):
        try:
            results = read_sql_query(response, "student.db")
            if results:
                st.subheader("Results:")
                for row in results:
                    st.write(row)
            else:
                st.warning("No data found.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
