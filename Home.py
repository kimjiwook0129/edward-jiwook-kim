import streamlit as st
from langchain.prompts import PromptTemplate
from datetime import datetime

st.set_page_config(
    page_title = "Edward Jiwook Kim",
    page_icon = "👋"
)

st.title("Hi, I'm Edward Kim 👋")
st.markdown("""""")

question_to_agent = st.text_input(
    "Do you have any question about me?",
    placeholder="What does Edward do during his free time?"
)

with st.sidebar:
    openai_api_key = st.text_input(
        "Enter your OpenAI API Key to chat with my agent.",
        placeholder="sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    )

if question_to_agent:
    if openai_api_key:
        st.markdown("Allowed to chat!")
    else:
        with st.sidebar:
            st.error("Please provide OpenAI Key to chat.")