from dataclasses import dataclass
from typing import Optional

x, y, z, w, qx, qy, qz = 0, 0, 0, 1, 0, 0, 0

@dataclass
class BaseObject:
    name: str = ""
    index: int = 0
    loc: tuple = (x, y, z, w, qx, qy, qz)


@dataclass
class Container:
    pass


@dataclass
class Place:
    name: str = ""
    adjancy: str = ""
    where: tuple = (x, y, z)
    
    