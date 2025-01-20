import networkx as nx
from matplotlib import pyplot as plt

from scripts.sturcture.frame import *


# Helper Class for Graph Management
class GraphManager:
    def __init__(self):
        self.graph = nx.Graph()

    # Method to add location nodes
    def add_location(self, location_id: str, description: str):
        location = Location(id=location_id)
        self.graph.add_node(location_id, data=location)
        # print(f"Location '{location_id}' added with description: {description}")

    # Method to add a robot
    def add_robot(self, robot: Robot):
        if robot.current_location not in self.graph:
            raise ValueError(f"Location '{robot.current_location}' does not exist in the graph.")

        # Add robot to the location's data
        location_data = self.graph.nodes[robot.current_location]["data"]
        location_data.robot.append(robot.id)

        # Add robot as a node for metadata (optional)
        self.graph.add_node(robot.id, data=robot)
        # print(f"Robot '{robot.id}' added at location '{robot.current_location}'.")

    # Method to add an object
    def add_object(self, obj: BaseObject):
        if obj.current_location not in self.graph:
            raise ValueError(f"Location '{obj.current_location}' does not exist in the graph.")

        # Add object to the location's data
        location_data = self.graph.nodes[obj.current_location]["data"]
        location_data.objects.append(obj.id)

        # Add object as a node for metadata (optional)
        self.graph.add_node(obj.id, data=obj)
        # print(f"Object '{obj.id}' of type '{obj.type}' added at location '{obj.current_location}'.")

    # Method to add edges between locations
    def add_edge(self, from_location: str, to_location: str):
        if from_location not in self.graph or to_location not in self.graph:
            raise ValueError(f"One or both locations '{from_location}' or '{to_location}' do not exist.")
        self.graph.add_edge(from_location, to_location)
        # print(f"Edge added from '{from_location}' to '{to_location}'.")

    # Display the graph
    def display_graph(self):
        for node, data in self.graph.nodes(data=True):
            print(f"Node: {node}, Data: {data['data']}")
        for edge in self.graph.edges:
            print(f"Edge: {edge}")

    def describe_graph(self):
        description = []
        for node, data in self.graph.nodes(data=True):
            if isinstance(data["data"], Location):
                location = data["data"]
                description.append(
                    f"- {location.id}: Contains {len(location.robot)} robot(s) "
                    f"and {len(location.objects)} object(s)."
                )
            elif isinstance(data["data"], Robot):
                robot = data["data"]
                description.append(
                    f"- {robot.id}: Located at {robot.current_location} with status {robot.status}."
                )
            elif isinstance(data["data"], BaseObject):
                obj = data["data"]
                description.append(
                    f"- {obj.id}: {obj.type} located at {obj.current_location}."
                )

        edges = [f"{edge[0]} <-> {edge[1]}" for edge in self.graph.edges]
        edge_description = "Edges connect: " + ", ".join(edges)
        return "\n".join(description) + "\n" + edge_description

    def export_graph_as_json(self):
        nodes = {
            node: data["data"].model_dump(mode='json') for node, data in self.graph.nodes(data=True)
        }
        edges = list(self.graph.edges)
        return {"nodes": nodes, "edges": edges}

    def visualize(self):
        nx.draw(self.graph, with_labels=True, node_color='skyblue', font_weight='bold')
        plt.show()



"""
class FruitObject(BaseObject):
    parent: Optional[str] = Field(
        None, description="Parent object ID (e.g., stem, tree, robot or container) the fruit is attached to."
    )
    is_ripe: bool = Field(False, description="Whether the fruit is ripe.")
    is_rotten: bool = Field(False, description="Whether the fruit is rotten.")
"""

#
# if __name__ == '__main__':
#     manager = GraphManager()
#     # Add locations
#     manager.add_location("dock_station", "Starting point for all robots.")
#     manager.add_location("prepare_station", "Station with baskets for sorting tomatoes.")
#     manager.add_location("stem_1", "A tomato stem produces multiple tomatoes.")
#     manager.add_location("stem_2", "A tomato stem produces multiple tomatoes.")
#
#     # Add robot
#     robot_1 = Robot(
#         id="robot_1",
#         description="A mobile robot equipped with a manipulator featuring a two-finger gripper and a camera. "
#                     "Capable of navigating, scanning, harvesting, and sorting tomatoes. "
#                     "The robot has a dedicated area to place the basket.",
#         current_location="dock_station",
#         action_set=[
#             "navigate",
#             "scan_tomatoes",
#             "scan_ripeness",
#             "scan_rottenness",
#             "harvest",
#             "pick",
#             "place"
#         ],
#         status="idle"
#     )
#
#     manager.add_robot(robot_1)
#
#     # Add basket object
#     basket_1 = ContainerObject(
#         id="basket_1",
#         type="basket",
#         current_location="prepare_station",
#         compartments={"left": [], "right": []},
#         status="idle"
#     )
#
#     manager.add_object(basket_1)
#
#     # Add edges between locations
#     manager.add_edge("dock_station", "prepare_station")
#     manager.add_edge("prepare_station", "stem_1")
#     manager.add_edge("prepare_station", "stem_2")
#     manager.add_edge("stem_1", "stem_2")
#
#     manager.visualize()
#
#     graph_text = manager.describe_graph()
#     graph_json = json.dumps(manager.export_graph_as_json(), indent=4)
#     print(graph_text, "\n\n\n")
#     print(graph_text)
