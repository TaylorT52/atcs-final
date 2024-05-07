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
        responder = Agent(
            role = "English teacher",
            goal = self.goal,
            backstory = "Given a student's essay, a teacher needs help identifying sentences containing specific phrases.",
            verbose = True,
            allow_delegation = False,
            llm = self.model
        )
        identify_errors = Task(
            description = f"Return the exact sentences which contain the phrases {self.keywords} from the text: '{text}'. The sentence must delcare the existence or necessity of importance, without detailing the object or subject of importance.",
            #f"Return the exact sentences that declare the existence or necessity of importance, without detailing the object or subject of that importance. The sentences MUST contain the following phrases {self.keywords} in the given text: {text}",
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