from langchain_ollama.chat_models import ChatOllama
from langgraph.prebuilt import create_react_agent
from models import query_graph
from crawler import crawl


tools = [query_graph, crawl]
model = ChatOllama(model="llama3.1", temperature=0).bind_tools(tools)
agent = create_react_agent(model=model, tools=tools)
print("Hello I'm an Interactive Package Manager \nEnter your prompt down here ")

while True: 
    prompt = input("📦>> ")
    for step in agent.stream({'messages': prompt}, stream_mode="values"): 
        message = step["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

