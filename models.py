from neo4j import GraphDatabase 
from queries import create_package, get_dependencies, get_dependency_by_degree, get_package, topological_sort 
from queries import create_conflicts_with_relation
from queries import create_depend_on_relation
from queries import label_as_leaf
from queries import label_as_library
from queries import project_graph
import os

def get_package_template():
    return { 'URL': '', 'Name': '', 'Version':'',
            'Packager': '',
            'Description': '',
            'Architecture': '',
            'Installed Size': '', 'conflictors': [],
            'dependencies': [],
            'isLibrary': False,
            # 'ManualIndex': [float],
            # 'Manual': str,
        }

PASS = os.environ["NEO4J_PASS"]
URI = "bolt://localhost:7687"
AUTH = ("neo4j", PASS)
driver = GraphDatabase.driver(URI, auth=AUTH)
driver.verify_connectivity()

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
        print(f"warning : {e}")

def get_topological_sort(name):
    """"
    This tool is used to know the righ topological order
    for installing the package and its dependencies
    this is used to reslove dependency conflicts
    Args: 
        name: str
    """
    try: 
        order = ""
        with driver.session(database="neo4j") as session: 
            session.execute_write(project_graph, name)
            order = session.execute_read(topological_sort,name)
        return order
    except Exception as e : 
        print(f"something went wrong!! : {e}")

def get_dependency_by_distance(name, step): 
    """
    this tool is used to get the dependencies of 
    a software package that are N steps away from it 
    takes in name of the package and step 
    Args: 
        name: str
        step: int
    """
    with driver.session() as s: 
        result = s.execute_read(get_dependency_by_degree,name,step)
        return result

def get_all_dependencies(name): 
    """
    this tool takes returns all the dependencies
    of the package 
    Args: 
        name: str
    """
    with driver.session() as s: 
        result = s.execute_read(get_dependencies,name)
        return result

def get_package_info(name: str): 
    """
        This tool is used for getting information 
        about a software package
        Args: 
            name: str
        Returns: 
            info about the package
    """
    with driver.session() as s: 
        result = s.execute_read(get_package,name)
        print(result)
        return result

