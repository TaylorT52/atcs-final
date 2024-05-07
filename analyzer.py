import ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.llms import OpenAI
from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew, Process
import promptgen

class Analyzer():
    def __init__(self):
        self.model = Ollama(model = "llama2")
        self.keywords = "'importance of', 'significance of', 'value of', 'valuable', 'useful', 'necessary', 'necessity of', 'important', 'it's important', 'crucial'"
        self.goal = f"Return exact sentences containing the phrases. Don't extrapolate meaning, just identify phrases: {self.keywords}."
        #f"Return exact sentences that state the existence of value without specifying what is important, containing the following phrases {self.keywords}. Don't extrapolate meaning."

    def process_data(self, text):
        my_goal = "Identify sentences where there are errors in student essays from only the provided list of errors and return them. Return the exact entire sentences with 'importance of, significance of, value of, valuable, useful," + "  necessary, necessity of, important, it's important, crucial' in the text."+ " Return the exact sentences with any of the following hasty generalizations: " + "'Since the beginning of time', 'in society', 'in our world', 'throughout history', or any other similar hasty generalization." + " You do not need to fix the sentences or provide a conclusion text. Only return sentences with the provided errors. If there are no errors in the text, you may return nothing."
        responder = Agent(
            role = "English teacher assistant",
            goal = self.goal,
            backstory = "Given a student's essay, a teacher needs help marking up the errors in the student's essay. ",
            verbose = True,
            allow_delegation = False,
            llm = self.model
        )
        identify_errors = Task(
            description = f"Return the exact sentences which contain the phrases {self.keywords} from the text: '{text}'. The sentence must delcare the existence or necessity of importance, without detailing the object or subject of importance.",
            #f"Return the exact sentences that declare the existence or necessity of importance, without detailing the object or subject of that importance. The sentences MUST contain the following phrases {self.keywords} in the given text: {text}",
            agent = responder,
            expected_output = "Only a list of each exact sentence where this an error, followed by a brief explanation of why the sentence was returned."
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

