# Formatting node


# import rospy
import numpy as np
import pandas as pd
import re


from neo4j import GraphDatabase
from knowledgebase.knowledge_base import CypherLangEncoder
from knowledgebase.knowledge_structure import *


URI = "bolt://localhost:7687"
USERNAME = "changmin"
PASSWORD = "00000000"

def custom_env():
    room = ["farm"]
    places = [
        PrepareStation(name="prepare", adjancy="dock"),
        DockStation(name="dock", adjancy="prepare, stem1"),
        Stem(name="stem1", adjancy="dock, stem2"),
        Stem(name="stem2", adjancy="stem1, stem3"),
        Stem(name="stem3", adjancy="stem2")
    ]
    
    objects = [
        Tomatoes(name="tomato1", index=1),
        Tomatoes(name="tomato2", index=2),
        Tomatoes(name="tomato3", index=3),
        Tomatoes(name="tomato4", index=4),
        Tomatoes(name="tomato5", index=5),
        Basket(name="GoodBasket1", index=1),
        Basket(name="BadBasket2", index=2),
    ]
    
    return room, places, objects

def custom_robot():
    return 0


class Neo4jCommunicator:
    def __init__(self, uri, user, pw):
        self.driver = GraphDatabase.driver(uri=uri, auth=(user, pw))
        self.encoder = CypherLangEncoder()
        
        # example
        _, self.places, self.objects = custom_env()

    def close(self):
        self.driver.close()

    def create_graph(self):
        
        # create node
        with self.driver.session() as session:
            session.run(self.encoder.merge("r", "Room", "farm"))
            for place in self.places:
                session.run(self.encoder.merge("p", "Place", place.name))
            for obj in self.objects:
                session.run(self.encoder.merge("o", "Object", obj.name))
        
        # set base attributes
        with self.driver.session() as session:
            for place in self.places:
                session.run(self.encoder.set_node("p", "Place", place.name, place, mode="Place"))
            for obj in self.objects:
                session.run(self.encoder.set_node("o", "Object", obj.name, obj, mode="object"))
        
        # set tomato attributes
        with self.driver.session() as session:
            for obj in self.objects:
                if "tomato" in obj.name:
                    session.run(self.encoder.set_tomato_node("o", "Object", obj.name, obj))
        
        # set hierarchy
        # with self.driver.session() as session:
            # pass
        
    def delete_all(self):
        with self.driver.session() as session:
            session.run(
                """MATCH (n)
                           DETACH DELETE n"""
            )


def main():
    neo4j_example = Neo4jCommunicator(URI, USERNAME, PASSWORD)
    neo4j_example.delete_all()
    neo4j_example.create_graph()
    neo4j_example.close()


if __name__ == "__main__":
    main()
    