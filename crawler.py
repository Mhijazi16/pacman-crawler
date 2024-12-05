import os
from langchain_ollama.embeddings import OllamaEmbeddings
from models import get_package_template, store_package, apply_name_constraint

embeddings_allowed = False

if embeddings_allowed: 
    llm = OllamaEmbeddings(model="nomic-embed-text")

    def embed_data(data):
        return llm.embed_query(data)

def fill_package(name: str):
    package = get_package_template()
    headers = ["Installed Size","Version","Packager","Description","Architecture","URL"]
    data = os.popen(f"pacman -Qi {name}").read()
    lines = data.strip().split('\n')

    for line in lines: 
        if ":" not in line: 
            continue

        key, value = line.split(":",1)
        key = key.strip()
        value = value.strip()

        if key in headers:  
            package[key] = value
        elif key == "Name":
            if "lib" in value or value.startswith("lib"): 
                package['isLibrary'] = True
            package[key] = value
        elif key == "Depends On":
            dependencies = value.split('  ')
            for dep in dependencies:
                if ">" in dep:
                    result = dep.split('>',1)[0]
                    package['dependencies'].append(result)
                else: 
                    package['dependencies'].append(dep)
        elif key == "Conflicts With": 
            package['conflictors'].append(value)

        if embeddings_allowed: 
            man = os.popen(f"man {name}").read() 
            if "No manual entry" in man: 
                man = package["Description"]
                package["Manual"] = embed_data(man)
            else: 
                package["Manual"] = embed_data(package["Description"] + man)

    return package

seen = []
def crawl(name: str): 

    if name in seen: 
        return 

    seen.append(name)
    package = fill_package(name)

    for dependency in package['dependencies']: 
        if dependency == "None": 
            store_package(package)
            return 
        crawl(dependency)
    store_package(package)
    print(package["Name"], package['dependencies'])

# only execute this once
# apply_name_constraint()

crawl("htop")
