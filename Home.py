import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
from agent.utils import print_message_history, send_message, ChatCallbackHandler

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
     
     
     """
     # Context: {context}
    ),
    ("human", "{question}"),
])

question_to_agent = st.chat_input(
    "Do you have any question about me? (e.g. What are Edward's hobbies?)"
)

with st.sidebar:
    
    openai_api_key = st.text_input(
        "Enter your OpenAI API Key to chat with my agent.",
        placeholder="sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    )

# Message history keep deleting when api key changes or deleted
    # -> should remain the same

if question_to_agent:
    print_message_history()
    if openai_api_key:
        llm = ChatOpenAI(
            temperature=0.1,
            model_name="gpt-3.5-turbo-1106",
            streaming=True,
            api_key=openai_api_key,
            callbacks =[ChatCallbackHandler()]
        )
            

        # Write doc related to Edward
        # Put embeddings in .cache FAISS vectorstore

        send_message(question_to_agent, 'human')

        chain = {
            # "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough()
        } | prompt | llm

        with st.chat_message("ai"):
            response = chain.invoke(question_to_agent)
    else:
        with st.sidebar:
            st.error("Please provide OpenAI Key to chat.")

else:
    
    if "messages" in st.session_state.keys():
        print_message_history()
    else:
        st.session_state["messages"] = []