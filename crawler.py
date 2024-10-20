import os
from typing import TypedDict, List

class Package(TypedDict): 
    Name: str 
    Packager: str
    URL: str
    Description: str
    Size: str
    conflictors: List[str]
    dependencies: List[str] 
    isLibrary: bool

def get_package():
    return {
            'URL': '',
            'Name': '',
            'Version':'',
            'Packager': '',
            'Description': '',
            'Architecture': '',
            'Installed Size': '',
            'conflictors': [],
            'dependencies': [],
            'isLibrary': False,
        }

def fill_package(name: str):

    package = get_package()
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
            if "lib" in value: 
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

    return package

seen = []
packages = [] 
def crawl(name: str): 

    if name in seen: 
        return 

    seen.append(name)
    package = fill_package(name)
    packages.append(package)

    # for debuging
    # print(package)
    # input("============")

    for dependency in package['dependencies']: 
        if dependency == "None": 
            return 
        crawl(dependency)


crawl("htop")
for package in packages: 
    print(package)
    print("=============")
    input()
