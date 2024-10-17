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

def get_package():
    return {
            'Name': '',
            'Packager': '',
            'URL': '',
            'Description': '',
            'Size': '',
            'conflictors': [],
            'dependencies': []
        }

def fill_package(name: str):

    package = get_package()
    headers = ["Name","Size","Packager","Description","URL"]
    data = os.popen(f"pacman -Qi {name}").read()
    lines = data.strip().split('\n')

    for line in lines: 
        key, value = line.split(":",1)
        key = key.strip()
        value = value.strip()

        if key in headers:  
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

print(fill_package("glibc"))
