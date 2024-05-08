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
        self.model = Ollama(model = "llama3")
        self.promptgen = promptgen
        self.tvw = "'importance of', 'significance of', 'value of', 'valuable', 'useful', 'necessary', 'necessity of', 'important', 'it's important', 'crucial'"
        self.hasty_generalizations = "'since the beginning of time', 'in society', 'in our world', 'throughout history'"
        self.goal = f"Identify sentences where there are errors in student essays from only the following errors and return them. Return exact full sentences that contain any of the phrases {self.tvw} that tell readers 'that' something matters and not 'what' matters. Also, return only exact full sentences containing the phrases: {self.hasty_generalizations} that make an overly general statement about something. Only return sentences with the provided errors and do not modify original sentences in the text. If there are no errors in the text, you may return nothing." 
        if len(self.promptgen.bad_sentences) != 0:
            self.goal = self.goal + f" Example: {self.promptgen.bad_sentences[0]} is an incorrectly identified error because {self.promptgen.feedback_list[0]}"
        #f"Return exact sentences that state the existence of value without specifying what is important, containing the following phrases {self.keywords}. Don't extrapolate meaning."

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
            description = f"Return only the exact sentences which contain any of the provided errors in the following text: {text}",
            #f"Return the exact sentences that declare the existence or necessity of importance, without detailing the object or subject of that importance. The sentences MUST contain the following phrases {self.keywords} in the given text: {text}",
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

