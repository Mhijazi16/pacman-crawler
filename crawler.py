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
