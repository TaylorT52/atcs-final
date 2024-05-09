import ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew, Process
import promptgen

class Analyzer():
    def __init__(self, promptgen):
        self.model = Ollama(model = "llama2")
        self.promptgen = promptgen
        self.goal = self.promptgen.generate_goal()

    def process_data(self, text):
        responder = Agent(
            role = "English teacher assistant",
            goal = self.goal,
            backstory = "Given a student's essay, a teacher needs help marking up the errors in the student's essay.",
            verbose = True,
            allow_delegation = False,
            llm = self.model
        )
        identify_errors = Task(
            description = f"Return the exact sentences that declare the existence or necessity of importance, without detailing the object or subject of that importance. The sentences MUST contain the following phrases {self.tvw} in the given text: {text}",
            agent = responder,
            expected_output = "Only a list of each full exact sentence where this an error, and then a brief explanation of why the sentence was returned as an error."
        )
        crew = Crew(
            agents = [responder],
            tasks = [identify_errors],
            verbose = 2,
            process = Process.sequential
        )

        output = crew.kickoff()
        return output


