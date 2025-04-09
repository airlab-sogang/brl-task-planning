import pandas as pd
import numpy as np
import re

from toy_database import toy_data, CypherEncoder
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USERNAME = "changmin"
PASSWORD = "00000000"


class Neo4jToy:
    def __init__(self, uri, user, pw):
        self.driver = GraphDatabase.driver(uri=uri, auth=(user, pw))
        self.data = toy_data
        self.hierarchy = ["Earth", "continets", "countries", "cities"]
        self.cypher = []
        self.encoder = CypherEncoder()

    def close(self):
        self.driver.close()

    def watch_session(self):
        q = 'MATCH (n) RETURN n LIMIT 5'
        with self.driver.session() as session:
            nodes = session.run(q)
            for node in nodes:
                print(node)

    def cypher_query_parser(self, index=0):
        with self.driver.session() as session:

            for planet in ["Earth"]:
                message = self.encoder.merge(value='e', label='Earth', name=planet)
                session.run(message)

                for continent in ["North America", "Asia", "Europe"]:
                    message = self.encoder.merge(value='c', label='Continent', name=continent)
                    session.run(message)

                    if continent == "North America":
                        for country in ["USA", "Canada"]:
                            message = self.encoder.merge(value='ct', label='Country', name=country)
                            session.run(message)
                    elif continent == "Asia":
                        for country in ["China", "Japan", "Korea"]:
                            message = self.encoder.merge(value='ct', label='Country', name=country)
                            session.run(message)
                    elif continent == "Europe":
                        for country in ["Germany", "France", "Russia"]:
                            message = self.encoder.merge(value='ct', label='Country', name=country)
                            session.run(message)
                    else:
                        raise ValueError("Wrong country")
            
            # Earth2continent
            for continent in ["North America", "Asia", "Europe"]:
                message = self.encoder.uni_match("Earth", "Continent", "Earth", continent, "PART_OF")
                session.run(message)
                if continent == "North America":
                    for country in ["USA", "Canada"]:
                        message = self.encoder.uni_match("Continent", "Country", continent, country, "PART_OF")
                        session.run(message)
                elif continent == "Asia":
                    for country in ["China", "Japan", "Korea"]:
                        message = self.encoder.uni_match("Continent", "Country", continent, country, "PART_OF")
                        session.run(message)
                elif continent == "Europe":
                    for country in ["Germany", "France", "Russia"]:
                        message = self.encoder.uni_match("Continent", "Country", continent, country, "PART_OF")
                        session.run(message)
                else:
                    raise ValueError("Wrong country")

            match_message1 = """MATCH (ee:Person {name: 'Changmin'})
            SET ee.from = 'KyoKyo'
            SET ee += {city:'Seoul', hobby:'Robot'}
            """
            
            match_message2 = """
            MATCH (ee:Person {name: 'Aram'})
            SET ee.from = 'KyoKyo'
            SET ee += {city: 'Sejong', hobby: 'Mingu'}
            SET ee += {age: 30}
            """
            

    def delete_all(self):
        with self.driver.session() as session:
            session.run("""MATCH (n)
                           DETACH DELETE n""")

    def create_graph(self):
        with self.driver.session() as session:
            # initialize the database
            # session.run("MATCH (n) DETACH DELETE n")
            session.run("MERGE (e: Earth {name: 'Earth'})")

            for continet, countries in toy_data["Earth"].items():
                pass

            # Create Continents, Countries, and Cities
            for continent in self.data["Earth"]["continents"]:
                session.run("""
            MATCH (e:Earth {name: 'Earth'})
            MERGE (c:Continent {name: $name})
            MERGE (c)-[:PART_OF]->(e)
        """, name=continent["name"])

                
                for country in continent["countries"]:
                    session.run("""
                MATCH (c:Continent {name: $continent})
                MERGE (co:Country {name: $name})
                MERGE (co)-[:PART_OF]->(c)
            """, name=country["name"], continent=continent["name"])
                    
                    for city in country["cities"]:
                        session.run("""
                    MATCH (co:Country {name: $country})
                    MERGE (ci:City {name: $name})
                    ON CREATE SET ci.type = $type
                    MERGE (ci)-[:PART_OF]->(co)
                """, name=city["name"], type=city["type"], country=country["name"])
                        
            # Create Relationships
            for continent in self.data["Earth"]["continents"]:
                for country in continent["countries"]:
                    for related_country, relation in country["relations"].items():
                        session.run("""
                            MATCH (a:Country {name: $country}), (b:Country {name: $related})
                            MERGE (a)-[:RELATION {type: $relation}]->(b)
                """, country=country["name"], related=related_country, relation=relation)
                        
            # -----------------------
            # for country in countries:
            #     session.run("""
            #         CREATE (c:Country {name: $name})
            #         CREATE (cap:Capital {name: $capital})
            #         MERGE (c)-[:HAS_CAPITAL]->(cap)
            #     """, country)

            #     for city in country["cities"]:
            #         session.run("""
            #             MATCH (c:Country {name: $name})
            #             CREATE (ci:City {name: $city})
            #             MERGE (c)-[:HAS_CITY]->(ci)
            #         """, {"name": country["name"], "city": city})
    
    def query_graph(self):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (c:Country)-[:HAS_CAPITAL]->(cap),
                      (c)-[:HAS_CITY]->(ci)
                RETURN c.name AS country, cap.name AS capital, collect(ci.name) AS cities
            """)
            for record in result:
                print(f"나라: {record['country']}, 수도: {record['capital']}, 도시들: {', '.join(record['cities'])}")


def main():
    neo4j_example = Neo4jToy(URI, USERNAME, PASSWORD)
    neo4j_example.delete_all()
    neo4j_example.cypher_query_parser()
    neo4j_example.close()


if __name__ == "__main__":
    main()