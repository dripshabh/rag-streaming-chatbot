
import streamlit as st
from dotenv import load_dotenv
import os
from rag import rag_chain_of_thought_response
import anthropic
import chromadb
load_dotenv()

st.title("Medical Policy Q&A Chatbot")

client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

def initialize_session_state():
    if "model" not in st.session_state:
        st.session_state["model"] = "claude-sonnet-4-5"
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chroma_client" not in st.session_state:
        st.session_state.chroma_client = chromadb.PersistentClient(path="chroma_db")

def handle_user_input():
    if prompt := st.chat_input("Ask a question about the medical policy..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Get the streaming response generator
            response_stream = rag_chain_of_thought_response(prompt, st.session_state.chroma_client, client)
            
            # Use Streamlit's write_stream for automatic streaming display
            # This will display chunks as they arrive
            full_response = st.write_stream(response_stream)
            
            # Store the complete response
            st.session_state.messages.append({"role": "assistant", "content": full_response})

def display_messages():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
def main(): 
    initialize_session_state()
    display_messages()
    handle_user_input()

if __name__ == "__main__":
    main()