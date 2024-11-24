from neo4j import GraphDatabase 
import os

def get_package_template():
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

PASS = os.environ["NEO4J_PASS"]
URI = "bolt://localhost:7687"
AUTH = ("neo4j", PASS)
