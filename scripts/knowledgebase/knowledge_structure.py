from . import BaseObject, Container, Place
from dataclasses import dataclass
from typing import Optional


x, y, z, w, qx, qy, qz = 0, 0, 0, 1, 0, 0, 0

"""Object"""
@dataclass
class Stem(BaseObject, Place, Container):
    pass


@dataclass
class Tomatoes(BaseObject):
    ripeness: bool = False
    rottoness: bool = False
    harvested: bool = False

    on: Optional[Container] = False


@dataclass
class Basket(BaseObject, Container):
    on: Optional[Place] = False


@dataclass
class Tools(BaseObject):
    pass


"""Place"""
@dataclass
class DockStation(Place):
    pass


class PrepareStation(Place):
    pass


"""Robot"""
@dataclass
class Robot:
    name: str = "UR5"
    index: int = 1

    # params
    payload: float = 30
    battery: int = 100

    # discrete value
    holding: Optional[BaseObject] = False
    harvesting: bool = False
    navigating: bool = False
    detecting: bool = False
    scanning: bool = False
    loading: Optional[Basket] = False

    # continuous value
    current_loc: tuple = (x, y, z, w, qx, qy, qz)
    end_effector: tuple = (x, y, z, w, qx, qy, qz)
    joint_state: tuple = ()
    end_effector_vel: float = (x, y, z)

    # ???
    current_images: tuple = ()

    # available actions
    def action_pick(self):
        pass

    def action_harvest(self):
        pass

    def action_scan(self):
        pass


"""Environment"""


class Environment:
    """
    DockStation
    Stems
    PrepareStation
    """

    def __init__(self):
        self.relation_type = ["ADJACENT_TO", "PART_OF", "ON"]

    def load_map(self):
        pass
