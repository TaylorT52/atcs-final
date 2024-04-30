import ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.llms import OpenAI
<<<<<<< HEAD
from langchain_community.llms import Ollama
import configparser
from crewai import Agent, Task, Crew, Process
=======
import configparser
>>>>>>> 4194af53 (works using open ai!)

class Analyzer():
    def __init__(self):
        self.hasty_generalizations = ["In society", "In the modern day", "Since the beginning of time", "Some may argue"]
<<<<<<< HEAD
        self.model = Ollama(model = "llama2")
        self.goal = "Identify sentences where there are errors in student essays from provided common student errors and return them. Return the exact sentences with 'importance of, significance of, value of, valuable, useful, necessary, necessity of, important, it's important, crucial' or similar errors in this text that tell readers 'that' something matters and not 'what' matters. Exclude sentences that contain 'because'"
=======
        self.api_key = self.load_api_key()

    def load_api_key(self):
        config = configparser.ConfigParser()
        config.read('config.ini') 
        return config['API']['APIKey']
>>>>>>> 4194af53 (works using open ai!)

    def process_data(self, text):
        responder = Agent(
            role = "English teacher assistant",
            goal = self.goal,
            backstory = "Given a student's essay, a teacher needs help marking up the errors in the student's essay. ",
            verbose = True,
            allow_delegation = False,
            llm = self.model
        )
<<<<<<< HEAD
        identify_errors = Task(
            description = f"Identify the errors in the following essay: '{text}'",
            agent = responder,
            expected_output = "A list of each sentence where this an error."
        )
        crew = Crew(
            agents = [responder],
            tasks = [identify_errors],
            verbose = 2,
            process = Process.sequential
        )

        output = crew.kickoff()
        return output

    # #TODO: need api key??? 
    # def load_api_key(self):
    #     config = configparser.ConfigParser()
    #     config.read('config.ini') 
    #     return config['API']['APIKey']

    # def process_data(self, text):
    #     print("processing data...")
    #     text_splitter = RecursiveCharacterTextSplitter(
    #         chunk_size=100,
    #         chunk_overlap=20,
    #         length_function=len,
    #         is_separator_regex=False
    #     )
    #     data = text_splitter.create_documents([text])
    #     all_splits = text_splitter.split_documents(data)
    #     oembed = OllamaEmbeddings(model="nomic-embed-text")
    #     vectorstore = Chroma.from_documents(documents=all_splits, embedding=oembed)
    #     #TODO: fix questions
    #     question="Return the exact sentences with 'importance of, significance of, value of, valuable, useful, necessary, necessity of, important, it's important, crucial' or similar errors in this text that tell readers 'that' something matters and not 'what' matters." + text
    #     print(question)
    #     #TODO: need runnable nomic-embed-text to not use openapi
    #     qachain=RetrievalQA.from_chain_type(llm=OpenAI(api_key=self.api_key), retriever=vectorstore.as_retriever())
    #     ans = qachain.invoke({"query": question})
    #     result = ans["result"]
    #     print(result)
    #     return result

=======
        data = text_splitter.create_documents([text])
        all_splits = text_splitter.split_documents(data)
        oembed = OllamaEmbeddings(model="nomic-embed-text")
        vectorstore = Chroma.from_documents(documents=all_splits, embedding=oembed)
        question="Return the entire input text with double asterisks around the phrase [we begin to wonder]"
        qachain=RetrievalQA.from_chain_type(llm=OpenAI(api_key=self.api_key), retriever=vectorstore.as_retriever())
        ans = qachain.invoke({"query": question})
        print(ans["result"])
>>>>>>> 4194af53 (works using open ai!)
