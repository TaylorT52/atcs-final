import ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA


class Analyzer():
    def __init__(self):
        self.hasty_generalizations = ["In society", "In the modern day", "Since the beginning of time", "Some may argue"]

    def process_data(self, text):
        print("processing data...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=100,
            chunk_overlap=20,
            length_function=len,
            is_separator_regex=False
        )
        data = text_splitter.create_documents([text])
        all_splits = text_splitter.split_documents(data)
        oembed = OllamaEmbeddings(model="nomic-embed-text")
        vectorstore = Chroma.from_documents(documents=all_splits, embedding=oembed)
        question="What is Porath's purpose?"
        print("done")
        # qachain=RetrievalQA.from_chain_type(ollama, retriever=vectorstore.as_retriever())
        # qachain.invoke({"query": question})