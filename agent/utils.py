import streamlit as st
from langchain.callbacks.base import BaseCallbackHandler

def save_message(message, role):
    if not "messages" in st.session_state.keys():
        st.session_state["messages"] = []
    st.session_state["messages"].append({"message": message, "role": role})

def send_message(message, role, save = True):
    with st.chat_message(role):
        st.markdown(message)
    if save:
        save_message(message, role)

def print_message_history():
    for message in st.session_state["messages"]:
        send_message(
            message["message"],
            message['role'],
            False,
        )


class ChatCallbackHandler(BaseCallbackHandler):

    message = ""
    
    def on_llm_start(self, *args, **kwargs):
        self.message_box = st.empty()
        
    def on_llm_end(self, *args, **kwargs):
        save_message(self.message, "ai")

    def on_llm_new_token(self, token, *args, **kwargs):
        self.message += token
        self.message_box.markdown(self.message)

        