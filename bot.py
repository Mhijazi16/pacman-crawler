from langchain_ollama.chat_models import ChatOllama
from langgraph.prebuilt import create_react_agent
from models import free_database, get_all_dependencies, get_package_info, get_dependency_by_distance, get_topological_sort, get_conflicting_packages
from crawler import crawl


tools = [crawl,
         get_conflicting_packages,
         get_package_info,
         get_dependency_by_distance,
         get_all_dependencies,
         get_topological_sort,
         free_database]

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

