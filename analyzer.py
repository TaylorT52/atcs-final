import ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew, Process
import promptgen
import configparser
from langchain_community.llms import OpenAI

class Analyzer():
    def __init__(self, promptgen):
        self.api_key = self.load_api_key()
        self.tvw = "'importance of', 'significance of', 'value of', 'valuable', 'useful', 'necessary', 'necessity of', 'important', 'it's important', 'crucial'"

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
        question=f"Return a dashed list of exact sentences from the text from only the following errors and return them. After the sentence, explain why you chose it. Return exact full sentences that contain any of the phrases {self.tvw} that tell readers 'that' something matters and not 'what' matters. Only return sentences with the provided errors and do not modify original sentences in the text. If there are no errors in the text, you may return nothing. Text: {text}" 
        print(question)
        qachain=RetrievalQA.from_chain_type(llm=OpenAI(api_key=self.api_key), retriever=vectorstore.as_retriever())
        ans = qachain.invoke({"query": question})
        result = ans["result"]
        print(result)
        return result