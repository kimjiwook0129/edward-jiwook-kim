import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
from agent.utils import print_message_history, send_message, ChatCallbackHandler
from utils.models import openai_models

st.set_page_config(
    page_title = "Edward Jiwook Kim",
    page_icon = "👋"
)
st.title("Hi, I'm Edward Kim 👋")
st.markdown("""""")


prompt = ChatPromptTemplate.from_messages([
    ("system", """
     For now, this functinality is being developed, just say this feature is being develped whatever the user asks.
     """
    ),
    # ("system", """
     
    #  You are a friendly chat agent who answers to questions about a person named "Edward Jiwook Kim".
    #  Answer the question using only the following context.
     
    #  If you don't know the answer, or the question sounds not relevant to "Edward Jiwook Kim",
    #  just say you don't know. Don't make anything up.
    #  """
    #  # Context: {context}
    # ),
    ("human", "{question}"),
])

question_to_agent = st.chat_input(
    "Do you have any question about me? (e.g. What are Edward's hobbies?)",
)

with st.sidebar:

    # Model selection
    openai_model_exists = "openai_model" in st.session_state.keys()
    default_model = openai_models[0] if not openai_model_exists else st.session_state["openai_model"]
    model_index = openai_models.index(default_model)
    openai_model = st.sidebar.selectbox(
        "Which model would you like to use?",
        openai_models,
        index = model_index
    )

    # Receive user's OpenAI API key
    openai_key_exists = "openai_api_key" in st.session_state.keys()
    openai_api_key = st.text_input(
        "Enter your OpenAI API Key to chat with my agent.",
        placeholder="sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        value= "" if not openai_key_exists else st.session_state["openai_api_key"]
    )

    if st.button("Reset Chat"):
        st.session_state["messages"] = []
        print_message_history()

# Update Session State if user updates the values
if openai_model:
    st.session_state["openai_model"] = openai_model
if openai_api_key:
    st.session_state["openai_api_key"] = openai_api_key

if question_to_agent:
    print_message_history()
    if openai_api_key:
        llm = ChatOpenAI(
            temperature=0.1,
            model_name=openai_model,
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
        try:
            with st.chat_message("ai"):
                response = chain.invoke(question_to_agent)
        except:
            error_message = "Please provide a correct OpenAI API key."
            send_message(error_message, 'ai')
    else:
        with st.sidebar:
            st.error("Please provide OpenAI Key to chat.")

else:
    
    if "messages" in st.session_state.keys():
        print_message_history()
    else:
        st.session_state["messages"] = []
