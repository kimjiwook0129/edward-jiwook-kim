import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

st.set_page_config(
    page_title = "Edward Jiwook Kim",
    page_icon = "👋"
)

st.title("Hi, I'm Edward Kim 👋")
st.markdown("""""")

prompt = ChatPromptTemplate.from_messages([
    ("system", """
     You are a friendly chat agent who answers to questions about a person named "Edward Jiwook Kim".
     Answer the question using only the following context.
     
     If you don't know the answer, or the question sounds not relevant to "Edward Jiwook Kim",
     just say you don't know. Don't make anything up.
     
     Context: {context}
     """
    ),
    ("human", "{question}"),
])

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
        llm = ChatOpenAI(
            temperature=0.1,
            streaming=True,
        )

        # Write doc related to Edward
        # Put embeddings in .cache FAISS vectorstore
        # 
    else:
        with st.sidebar:
            st.error("Please provide OpenAI Key to chat.")