def print_purple(query):
    PURPLE = '\033[95m'
    RESET = '\033[0m'
    print(f"{PURPLE}{query}{RESET}")

def create_package(tx, package):
    query = """
        MERGE (p:Package{
            name: $name, url: $url, version: $version, owner: $owner, 
            description: $description, arch: $arch, size: $size})
        RETURN p.name AS name
    """
    print_purple(query)
    result = tx.run(query,
                    name=package["Name"], 
                    version=package["Version"],
                    url=package["URL"],
                    owner=package["Packager"],
                    arch=package["Architecture"],
                    size=package["Installed Size"],
                    description=package["Description"])
    return result

def label_as_library(tx, package):
    query = """MERGE (p:Package{name: $name}) SET p:Library"""
    print_purple(query)
    result = tx.run(query, name=package["Name"])
    return result

def label_as_leaf(tx, package):
    query = """MERGE (p:Package{name: $name}) SET p:Leaf"""
    print_purple(query)
    result = tx.run(query, name=package["Name"])
    return result

def create_depend_on_relation(tx, name, dep):
    query = """
        MERGE (p:Package {name: $name})
        MERGE (p2:Package {name: $dep_name})
        SET p2:DEPENDENCY
        MERGE (p)-[d:DEPENDS_ON]->(p2)
    """
    print_purple(query)
    result = tx.run(query, name=name, dep_name=dep)
    return result

def create_conflicts_with_relation(tx, name, conflict):
    query = """
        MERGE (p:Package {name: $name})
        MERGE (p2:Package {name: $conflictor})
        MERGE (p)-[:CONFLICTS_WITH]->(p2)
        MERGE (p)<-[:CONFLICTS_WITH]-(p2)
    """
    print_purple(query)
    result = tx.run(query, name=name, conflictor=conflict)
    return result

def project_graph(tx, package_name):
    drop_query = "CALL gds.graph.drop($name, false)"
    print_purple(drop_query)
    tx.run(drop_query, name=package_name)

    project_query = """
        MATCH (:Package{name: $name})-[rels:DEPENDS_ON*]->(leaf)
        WHERE NOT (leaf)-[:DEPENDS_ON]->()
        UNWIND rels AS r
        WITH DISTINCT r
        RETURN gds.graph.project($name, STARTNODE(r), ENDNODE(r))
    """
    print_purple(project_query)
    tx.run(project_query, name=package_name)

def topological_sort(tx, name):
    query = """
        CALL gds.dag.topologicalSort.stream($name, {computeMaxDistanceFromSource: true})
        YIELD nodeId, maxDistanceFromSource
        WITH gds.util.asNode(nodeId) as node,
               maxDistanceFromSource AS hops
        RETURN node.name as name
        ORDER BY hops DESC
    """
    print_purple(query)
    result = tx.run(query, name=name)

    order = f"this is the order that you should install dependencies for {name}"
    for i, record in enumerate(result): 
        order += f"\n{i}) {record['name']}"
    return order

def get_dependency_by_degree(tx, package_name, degree):
    query = f"""
        MATCH (node:Package)-[:DEPENDS_ON*..{degree}]->(other) 
        WHERE node.name = $name
        RETURN other.name as name
    """
    print_purple(query)
    result = tx.run(query, name=package_name)

    records = [record['name'] for record in result]
    return records

def get_dependencies(tx, name):
    query = """
        MATCH (n:Package{name: $name})-[:DEPENDS_ON*]->(b)
        RETURN DISTINCT b.name AS name
    """
    print_purple(query)
    result = tx.run(query, name=name)
    return [record['name'] for record in result]

def get_conflicts(tx, name):
    query = """
        MATCH (n:Package{name: $name})-[:CONFLICTS_WITH]->(b)
        RETURN DISTINCT b.name AS name
    """
    print_purple(query)
    result = tx.run(query, name=name)
    return [record['name'] for record in result]

def empty_database(tx):
    query = "MATCH (n) DETACH DELETE n"
    print_purple(query)
    tx.run(query)
    return "The database is empty"

def get_package(tx, name):
    query = """
        MATCH (node:Package{name:$name}) 
        RETURN node.name, 
               node.url, 
               node.size,
               node.arch,
               node.description, 
               node.owner
    """
    print_purple(query)
    result = tx.run(query, name=name)
    return result.single()
