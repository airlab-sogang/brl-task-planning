from knowledgebase.knowledge_structure import *
from scripts.utils.env_importer import Map2KB

class Env:
    def __init__(self):
        self.stems = []
        self.tomatoes = []
        self.baskets = []
        self.tools = []
        self.dock_station = []
        self.prepare_station = []

        self.relation_type = ["ADJACENT_TO", "PART_OF", "ON"]

    def update_all(self, info):
        """object"""
        for stem in info.stems:
            self.stems.append(Stem(name=stem.name, index=stem.index, loc=stem.loc))

        for basket in info.baskets:
            self.baskets.append(
                Basket(name=basket.name, index=basket.index, loc=basket.loc)
            )

        for tool in info.tools:
            self.tools.append(Tools(name=tool.name, index=tool.index, loc=tool.loc))

        """ place """
        for dock in info.dock_stations:
            self.dock_station.append(DockStation(where=dock.where, adjant=dock.adjant))
            
        for prepare in info.prepare_station:
            self.prepare_station.append(
                DockStation(where=prepare.where, adjant=prepare.adjant)
            )
        
        """ robot """
        
        

    def update_all_places(self, info):
        pass

"""

docker run \
--name ros1 \
-it \
--privileged \
--env="DISPLAY=:0.0" \
-v=/tmp/.X11-unix:/tmp/.X11-unix:ro \
-v=/dev:/dev \
-v=/home/changmin/PyProject/brl:/home/changmin/brl \
-w=/home/changmin \
osrf/ros:melodic-desktop-full
apt install python3-pip python3-yaml
apt install python3-catkin-tools python3-numpy
apt install wget curl
"""