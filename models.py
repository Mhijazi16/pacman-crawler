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
