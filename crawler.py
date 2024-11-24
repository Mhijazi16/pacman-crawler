import os
from models import get_package_template, store_package, apply_name_constraint

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

    return package

seen = []
def crawl(name: str): 

    if name in seen: 
        return 

    seen.append(name)
    package = fill_package(name)

    # for debuging
    # print(package)
    # input("============")
    for dependency in package['dependencies']: 
        if dependency == "None": 
            store_package(package)
            return 
        crawl(dependency)
    store_package(package)
    print(package["Name"], package['dependencies'])

# only execute this once
# apply_name_constraint()

crawl("neofetch")
