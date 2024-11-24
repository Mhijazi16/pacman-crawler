
def create_package(tx, package):
    result = tx.run("""
            MERGE (p:Package{
                name: $name, url: $url, version: $version, owner: $owner, 
                description: $description, arch: $arch, size: $size})
            RETURN p.name AS name """, 

             name=package["Name"], 
             version=package["Version"],
             url=package["URL"],
             owner=package["Packager"],
             arch=package["Architecture"],
             size=package["Installed Size"],
             description=package["Description"])

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
