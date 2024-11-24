from neo4j import GraphDatabase 
from queries import create_package, create_conflicts_with_relation, create_depend_on_relation, label_as_leaf, label_as_library
import os

def get_package_template():
    return {
            'URL': '',
            'Name': '',
            'Version':'',
            'Packager': '',
            'Description': '',
            'Architecture': '',
            'Installed Size': '', 'conflictors': [],
            'dependencies': [],
            'isLibrary': False,
        }

PASS = os.environ["NEO4J_PASS"]
URI = "bolt://localhost:7687"
AUTH = ("neo4j", PASS)

def apply_name_constraint():
    try: 
        driver = GraphDatabase.driver(URI, auth=AUTH)
        driver.verify_connectivity()
        driver.execute_query("""
             CREATE CONSTRAINT FOR (p:Package) REQUIRE p.name IS UNIQUE;
         """)
    except Exception as e: 
        print(f"error : {e}")


stored = []
def store_package(package):

    if package["Name"] in stored: 
        return
    stored.append(package["Name"])
    
    try: 
        driver = GraphDatabase.driver(URI, auth=AUTH)
        driver.verify_connectivity()

        with driver.session(database="neo4j") as session: 
            session.execute_write(create_package, package)

            if package["isLibrary"]: 
                session.execute_write(label_as_library, package)

            for dep in package["dependencies"]: 
                if dep == "None": 
                    session.execute_write(label_as_leaf, package)
                    continue
                session.execute_write(create_depend_on_relation, package["Name"], dep)

        for conflict in package["conflictors"]: 
            if conflict == "None": 
                break;
            session.execute_write(create_conflicts_with_relation,
                                  package["Name"],
                                  conflict)
    except Exception as e : 
        print(f"something went wrong!! : {e}")
