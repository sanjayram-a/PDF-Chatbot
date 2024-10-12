from langchain_community.llms import Ollama
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import PDFPlumberLoader
from langchain.chains import RetrievalQA
from langchain_core.prompts import ChatPromptTemplate




cached_llm = Ollama(model="gemma2:2b")
embedding = OllamaEmbeddings(model="nomic-embed-text")


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1024, chunk_overlap=100, length_function=len, is_separator_regex=False
)

def ask_ai(query):
    response = cached_llm.invoke(query)
    return response

def ask_pdf(query,folder_path):
    vector_store = Chroma(persist_directory=folder_path, embedding_function=embedding)
    retriever = vector_store.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(llm=cached_llm, retriever=retriever, chain_type="stuff")
    prompt_formatted = prompt.format(query=query)
    response = qa_chain.invoke(prompt_formatted)
    return response["result"]

def upload_pdf(file,folder_path):
    loader = PDFPlumberLoader(file)
    docs = loader.load_and_split()
    chunks = text_splitter.split_documents(docs)
    vector_store = Chroma.from_documents(
        documents=chunks, embedding=embedding, persist_directory=folder_path
    )

prompt_template = """You are a helpful assistant. Based on the context, answer the following question in at least 250 words:
1) Only answer from the given context
2) If you don’t know, just say there is no context
3) Refer to books and documents as context
4) While printing the answer, replace context with book
5) If the context had a question, try to solve it on your own
6) While answering, give headings and subheadings
7) Give an example if available
Question: {query}"""

prompt = ChatPromptTemplate.from_template(prompt_template)




if __name__ == '__main__':
    ask_pdf()
    ask_ai()