from langchain_community.llms import Ollama

if __name__ == "__main__":
    llm = Ollama(model="llama3")
    llm.invoke("Why is the sky blue?")