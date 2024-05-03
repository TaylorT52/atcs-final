import ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.llms import OpenAI
from langchain_community.llms import Ollama
import configparser
from crewai import Agent, Task, Crew, Process

class Analyzer():
    def __init__(self):
        self.hasty_generalizations = ["In society", "In the modern day", "Since the beginning of time", "Some may argue"]
        self.model = Ollama(model = "llama2")
        self.goal = "Return the exact sentences with 'importance of, significance of, value of, valuable, useful, necessary, necessity of, important, it's important, crucial' or similar errors in this text that tell readers 'that' something matters and not 'what' matters. Exclude sentences that contain 'because' or are statements of fact."

    def process_data(self, text):
        responder = Agent(
            role = "English teacher assistant",
            goal = self.goal,
            backstory = "Given a student's essay, a teacher needs help marking up the errors in the student's essay. ",
            verbose = True,
            allow_delegation = False,
            llm = self.model
        )
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