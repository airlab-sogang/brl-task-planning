from knowledgebase.knowledge_structure import *
from neo4j import GraphDatabase


class CypherLangEncoder:
    def __init__(self):
        pass

    def merge(self, value, label, name):
        return f"Merge ({value}: {label} {{name: '{name}'}})"

    def uni_match(self, label1, label2, name1, name2, relation):
        return f"""Match (a: {label1} {{name: '{name1}'}}), (b: {label2} {{name: '{name2}'}})
                   Merge (a) -[r:{relation}]-> (b)
"""

    def bi_match(self, label1, label2, name1, name2, relation1, relation2):
        return f"""Match (a: {label1} {{name: '{name1}'}}), (b: {label2} {{name: '{name2}'}})
                   Merge (a) -[r:{relation1}]-> (b)
                   Merge (b) -[r:{relation2}]-> (a)
"""

    def query_graph(self):
        pass

    def set_node(self, value, label, name, info, mode="place"):
        if mode.lower() == "place":
            return f"""MATCH ({value}:{label} {{name: '{name}'}})  
SET {value} += {{adjancy: '{info.adjancy}', where: '{info.where}'}}"""
        elif mode.lower() == "object":
            return f"""MATCH ({value}:{label} {{name: '{name}'}})  
SET {value} += {{index: {info.index}, loc: '{info.loc}'}}"""
        else:
            raise ValueError("Type is worng")
    
    def set_tomato_node(self, value, label, name, info):
        return f"""MATCH ({value}:{label} {{name: '{name}'}})  
SET {value} += {{ripeness: {info.ripeness}, rottoness: {info.rottoness}, harvested: {info.harvested}, on: {info.on}}}"""
            
            
class GraphUpdater(CypherLangEncoder):
    def __init__(self, domain="tomato"):
        super().__init__()
        self.domain = domain

    def update_env(env_json):
        pass
