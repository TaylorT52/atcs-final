#authors @ taylor tam & cody kletter
#actual model, runs inference on input essay

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

    def process_data(self, text):
        print(self.promptgen.generate_goal())
        print("\n")
        print(self.promptgen.generate_task() + text)

        responder = Agent(
            role = "English teacher assistant",
            goal = self.promptgen.generate_goal(),
            backstory = "Given a student's essay, a teacher needs help marking up the errors in the student's essay.",
            verbose = True,
            allow_delegation = False,
            llm = self.model
        )
        identify_errors = Task(
            description = self.promptgen.generate_task() + text,
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

