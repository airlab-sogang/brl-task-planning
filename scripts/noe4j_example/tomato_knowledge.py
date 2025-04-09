import numpy as np

from dataclasses import dataclass
from typing import List


@dataclass
class Tomato:
    index: int
    ripeness: bool
    rottoness: bool
    harvested: bool

    on: str = "stem1"
    loc: tuple = (1,2,3)

    def on_action(self, trigger):
        if trigger == "harvest":
            self.harvested = True
            self.on = "gripper"
        elif trigger == "discard":
            self.on = "basket_rotten"
        elif trigger == "place":
            self.on = "basket_good"
        else:
            raise ValueError("The trigger is wrong. ")


@dataclass
class Stem:
    index: int



class Evnironment:
    pass



def main():
    tomato_1 = Tomato(index=1, ripeness=True, rottoness=False, harvested=False, on="stem2")
    print(tomato_1.on)
    tomato_1.on_action("discard")
    print(tomato_1.on)

if __name__ == "__main__":
    main()


