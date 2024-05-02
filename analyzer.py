import ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.llms import OpenAI
import configparser

class Analyzer():
    def __init__(self):
        self.hasty_generalizations = ["In society", "In the modern day", "Since the beginning of time", "Some may argue"]
        self.api_key = self.load_api_key()

    #TODO: need api key??? 
    def load_api_key(self):
        config = configparser.ConfigParser()
        config.read('config.ini') 
        return config['API']['APIKey']

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
        #TODO: fix questions
        question="Return the exact sentences with 'importance of, significance of, value of, valuable, useful, necessary, necessity of, important, it's important, crucial' or similar errors in this text that tell readers 'that' something matters and not 'what' matters." + text
        print(question)
        #TODO: need runnable nomic-embed-text to not use openapi
        qachain=RetrievalQA.from_chain_type(llm=OpenAI(api_key=self.api_key), retriever=vectorstore.as_retriever())
        ans = qachain.invoke({"query": question})
        result = ans["result"]
        print(result)
        return result

