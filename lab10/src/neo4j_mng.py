from src.definitions import NEO4J_URI, PASSWORD, USERNAME
from neo4j import GraphDatabase


class Neo4jManager:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def run_query(self, query, parameters=None):
        with self.driver.session() as session:
            return session.run(query, parameters).data()

    def create_concept(self, name):
        query = "MERGE (:Concept {name: $name})"
        self.run_query(query, {"name": name})

    def create_relationship(self, name1, name2, relation):
        query = (
            """
        MATCH (a:Concept {name: $name1}), (b:Concept {name: $name2})
        MERGE (a)-[:`"""
            + relation
            + """`]->(b)
        """
        )
        self.run_query(query, {"name1": name1, "name2": name2})

    def visualize_graph(self):
        query = "MATCH (n)-[r]->(m) RETURN n, r, m"
        result = self.run_query(query)

        for record in result:
            print(record)


db = Neo4jManager(NEO4J_URI, USERNAME, PASSWORD)

concepts = ["Алгоритм", "Дані", "Обробка"]
for concept in concepts:
    db.create_concept(concept)

db.create_relationship("Алгоритм", "Дані", "USES")
db.create_relationship("Дані", "Обробка", "PROCESSES")

db.visualize_graph()

db.close()
