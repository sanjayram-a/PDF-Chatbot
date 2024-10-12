# PDF-Chatbot Project Documentation

## Overview

This project is a PDF-based chatbot application built using Streamlit, Langchain, and Ollama. It allows users to upload a PDF document, and then ask questions about the content of the document. The application uses a vector database (Chroma) to store embeddings of the PDF text, enabling efficient retrieval of relevant information for answering user queries.

## Deployment

The application can be deployed using Streamlit.  To run the application locally, navigate to the project directory in your terminal and run:
streamlit run app.py


## Features

* *PDF Upload:* Users can upload PDF files for querying.
* *Question Answering:*  The application answers questions based on the uploaded PDF content.
* *AI-powered fallback:* If the question cannot be answered from the PDF, it falls back to a general AI model.
* *Session Management:*  The application manages sessions to handle multiple users and clean up temporary files after inactivity.

### Dependencies

The project uses the following Python libraries:

chromadb==0.5.5
Flask==3.0.3
langchain==0.3.0
langchain-community==0.3.0
langchain-core==0.3.0
langchain-ollama==0.2.0
langchain-text-splitters==0.3.0
ollama==0.3.3
streamlit==1.39

These can be installed using pip install -r requirements.txt.


### Architecture

The application consists of two main Python files:

* **app.py:** This file contains the Streamlit application logic. It handles user interaction, file uploads, and displays the chatbot interface.  It uses the functions defined in backend.py to process the PDF and answer questions.

* **backend.py:** This file contains the core logic for processing the PDF, creating embeddings, and answering questions. It uses Langchain to load the PDF, split it into chunks, create embeddings using Ollama embeddings, and store them in a Chroma vector database.  It uses Ollama for both the question answering based on the PDF and for a general AI fallback.

The application uses Ollama for both the large language model (LLM) and the embedding model.  The specific models used are "gemma2:2b" for the LLM and "nomic-embed-text" for embeddings.

### Data Handling

The application creates temporary folders and files to store uploaded PDFs and the Chroma vector database. These are automatically deleted after a period of inactivity.

### Workflow

1. *User uploads a PDF:* The PDF is saved to a temporary folder.
2. *PDF is processed:* The PDF is loaded, split into chunks, and embeddings are generated.
3. *Embeddings are stored:* The embeddings are stored in a Chroma vector database.
4. *User asks a question:* The question is processed, and relevant information is retrieved from the vector database.
5. *Answer is generated:* The LLM generates an answer based on the retrieved information.
6. *Answer is displayed:* The answer is displayed to the user.


## Future Improvements

* Implement more robust error handling.
* Add support for other document formats.
* Improve the user interface.
