
def create_package(tx, package):
    result = tx.run("""
            MERGE (p:Package{
                name: $name, url: $url, version: $version, owner: $owner, 
                description: $description, arch: $arch, size: $size,
                manualIndex: $manual})
            RETURN p.name AS name """, 

             name=package["Name"], 
             version=package["Version"],
             url=package["URL"],
             owner=package["Packager"],
             arch=package["Architecture"],
             size=package["Installed Size"],
             description=package["Description"],
             manual=package["Manual"])

def label_as_library(tx, package):
    result = tx.run("""MERGE (p:Package{name: $name})
                       SET p:Library""", 
                    name=package["Name"])

def label_as_leaf(tx, package):
    result = tx.run("""MERGE (p:Package{name: $name})
                       SET p:Leaf""", 
                    name=package["Name"])

def create_depend_on_relation(tx, name, dep):
    result = tx.run("""
                    MERGE (p:Package {name: $name})
                    MERGE (p2:Package {name: $dep_name})
                    SET p2:DEPENDENCY
                    MERGE (p)-[d:DEPENDS_ON]->(p2)
                    """, 
                    name=name, dep_name=dep)

def create_conflicts_with_relation(tx, name, conflict):
    result = tx.run("""
                    MERGE (p:Package {name: $name})
                    MERGE (p2:Package {name: $conflictor})
                    MERGE (p)-[d:CONFLICTS_WITH]-(p2)
                    """, 
                    name=name, conflictor=conflict)

def project_graph(tx, package_name): 
    # drop previous in memory graph for package
    tx.run("CALL gds.graph.drop($name, false)", name=package_name)

    # project the graph to memory
    tx.run("""
                MATCH (:Package{name: $name})-[rels:DEPENDS_ON*]->(leaf)
                WHERE NOT (leaf)-[:DEPENDS_ON]->()
                UNWIND rels AS r
                WITH DISTINCT r
                RETURN gds.graph.project($name, STARTNODE(r), ENDNODE(r))
                    """, 
                name=package_name)

