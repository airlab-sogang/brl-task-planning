toy_data = {
    "Earth": {
        "continents": [
            {
                "name": "North America",
                "countries": [
                    {
                        "name": "USA",
                        "relations": { "Canada": "alliance", "Russia": "enemy" },
                        "cities": [
                            { "name": "Washington, D.C.", "type": "capital" },
                            { "name": "New York", "type": "city" },
                            { "name": "Los Angeles", "type": "city" }
                        ]
                    },
                    {
                        "name": "Canada",
                        "relations": { "USA": "alliance", "Russia": "neutral" },
                        "cities": [
                            { "name": "Ottawa", "type": "capital" },
                            { "name": "Toronto", "type": "city" },
                            { "name": "Vancouver", "type": "city" }
                        ]
                    }
                ]
            },
            {
                "name": "Europe",
                "countries": [
                    {
                        "name": "Germany",
                        "relations": { "France": "alliance", "Russia": "neutral" },
                        "cities": [
                            { "name": "Berlin", "type": "capital" },
                            { "name": "Munich", "type": "city" },
                            { "name": "Hamburg", "type": "city" }
                        ]
                    },
                    {
                        "name": "France",
                        "relations": { "Germany": "alliance", "Russia": "neutral" },
                        "cities": [
                            { "name": "Paris", "type": "capital" },
                            { "name": "Lyon", "type": "city" },
                            { "name": "Marseille", "type": "city" }
                        ]
                    },
                    {
                        "name": "Russia",
                        "relations": { "China": "alliance", "USA": "enemy" },
                        "cities": [
                            { "name": "Moscow", "type": "capital" },
                            { "name": "Владивосток", "type": "town" },
                            { "name": "Новосибирск", "type": "city" }
                        ]
                    }
                ]
            },
            {
                "name": "Asia",
                "countries": [
                    {
                        "name": "China",
                        "relations": {"Japan": "enemy", "Korea": "enemy", "USA": "enemy", "Canada": "neutral"},
                        "cities": [
                            { "name": "Bejing", "type": "capital" },
                            { "name": "Sanghai", "type": "city" },
                            { "name": "Guangzhou", "type": "city" }
                        ]
                    },
                    {
                        "name": "Japan",
                        "relations": {"USA": "alliance", "Russia": "enemy", "China": "enemy", "Korea": "neutral"},
                        "cities": [
                            { "name": "Tokyo", "type": "capital" },
                            { "name": "Osaka", "type": "city" },
                            { "name": "Fukuoka", "type": "city" }
                        ]
                    },
                    {
                        "name": "Korea",
                        "relations": {"USA": "alliance", "Russia": "neutral", "China": "enemy"},
                        "cities": [
                            { "name": "Seoul", "type": "capital" },
                            { "name": "Busan", "type": "city" },
                            { "name": "Daejon", "type": "city" }
                        ]
                    }
                ]
            }
        ]
    }
}


class CypherEncoder:
    def __init__(self):
        pass

    def merge(self, value, label, name): return f"Merge ({value}: {label} {{name: '{name}'}})"
    def uni_match(self, label1, label2, name1, name2, relation):
        return f"""Match (a: {label1} {{name: '{name1}'}}), (b: {label2} {{name: '{name2}'}})
                   Merge (a) -[r:{relation}]-> (b)
"""
    def bi_match(self, label1, label2, name1, name2, relation1, relation2):
        return f"""Match (a: {label1} {{name: '{name1}'}}), (b: {label2} {{name: '{name2}'}})
                   Merge (a) -[r:{relation1}]-> (b)
                   Merge (b) -[r:{relation2}]-> (a)
"""
    def query_graph():
        pass


if __name__ == "__main__":
    encoder = CypherEncoder()
    message = encoder.merge(value='c', label='Continent', name="continent")
    print(message)