import streamlit as st
import os
import uuid
import time
from langchain_community.llms import Ollama
from backend import *


# Constants
INACTIVITY_TIMEOUT = 30

def create_unique_folder():
    unique_id = str(uuid.uuid4())
    folder_path = f"temp_folder_{unique_id}"
    os.makedirs(folder_path, exist_ok=True)
    print(f"create folder: {folder_path}")
    return folder_path

def delete_folder(folder_path):
    if os.path.exists(folder_path):
        os.remove(folder_path)
        print(f"Deleted folder: {folder_path}")
        

if 'folder_path' not in st.session_state:
    st.session_state.folder_path = create_unique_folder()


#folder for dbase
def create_unique_file():
    unique_id = str(uuid.uuid4())
    file_path = f"temp_file_{unique_id}"
    os.makedirs(file_path, exist_ok=True)
    print(f"created file: {file_path}")
    return file_path

def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Deleted folder: {file_path}")

if 'file_path' not in st.session_state:
    st.session_state.file_path = create_unique_file()

if 'last_interaction' not in st.session_state:
    st.session_state.last_interaction = time.time()


def main():

    # Page setting
    st.set_page_config(page_title="PDF-Chatbot",page_icon="📖")
    st.header(":blue[PDF RAG]")
    st.subheader("Upload PDF to chat")

    # Sidebar
    with st.sidebar:
        st.title("Upload Your PDF here")
        pdf_file = st.file_uploader("Choose a PDF file", type="pdf")
        if st.button("Submit"):
            if pdf_file is not None:
                with st.spinner("In progress"):
                    with open(os.path.join(st.session_state.file_path,pdf_file.name), "wb") as f:
                        f.write(pdf_file.getbuffer())
                        upload_pdf(st.session_state.file_path+'\\'+pdf_file.name,st.session_state.folder_path)
                    st.write("File uploaded successfully")
            
    # Chat
    query = st.text_input("What's on your mind?")
    on = st.toggle("Chat with PDF")
    if on:
        response = ask_pdf(query,st.session_state.folder_path)
    else:
        response = ask_ai(query)
    if query:
        st.write(response)

    # Update last activity time
    st.session_state.last_interaction = time.time()

def check_inactivity():
    current_time = time.time()
    if (current_time - st.session_state.last_interaction) > INACTIVITY_TIMEOUT:
        delete_folder(st.session_state.folder_path)
        delete_file(st.session_state.file_path)
        st.session_state.folder_path = None
        st.session_state.file_path = None
        st.warning("Session expired due to inactivity. Resources have been deleted.")
        st.stop()




if __name__ == '__main__':
    main()
    check_inactivity()


