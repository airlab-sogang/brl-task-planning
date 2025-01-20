from typing import List, Dict, Optional

from pydantic import BaseModel, Field


class Location(BaseModel):
    id: str = Field(..., description="Unique identifier for the location the robot can traverse.")
    objects: List[str] = Field(default_factory=list, description="List of object IDs currently at this location.")
    robot: List[str] = Field(default_factory=list, description="List of robot IDs currently at this location.")


class Robot(BaseModel):
    id: str = Field(..., description="Unique identifier for the robot.")
    description: str = Field(..., description="The specific description of the robot.")
    current_location: str = Field(..., description="The current location of the robot.")
    action_set: List[str] = Field(..., description="Available actions.")
    status: str = Field("idle", description="Current status of the robot (e.g., idle, working).")
    contents: List[str] = Field(default_factory=list, description="List of object IDs currently carried by the robot.")
    now_holding: Optional[str] = Field(False, description="An object which robot holds now")


class BaseObject(BaseModel):
    id: str = Field(..., description="Unique identifier for the object.")
    type: str = Field(..., description="Type of the object (e.g., container, fruit).")
    current_location: str = Field(None, description="The current location ID of the object.")
    status: str = Field("idle", description="Current status of the object (e.g., idle, in use, transported).")


class ContainerObject(BaseObject):
    compartments: Dict[str, List[str]] = Field(
        default_factory=lambda: {"left": [], "right": []},
        description="Compartments in the container, divided into left and right sections."
    )
    carrier: Optional[str] = Field(
        False, description="ID of the robot currently carrying this container, if any."
    )


class FruitObject(BaseObject):
    parent: Optional[str] = Field(
        None, description="Parent object ID (e.g., stem, tree, robot or container) the fruit is attached to."
    )
    is_ripe: bool = Field(False, description="Whether the fruit is ripe.")
    is_rotten: bool = Field(False, description="Whether the fruit is rotten.")


class PlanStep(BaseModel):
    step: int = Field(..., description="The step number.")
    action: str = Field(
        ...,
        description="The action to perform. It includes iterative expressions such as 'for each' as well as robot atomic actions. "
    )
    target: List[str] = Field(..., description="The target of the action (e.g., location, object).")
    state: str = Field(..., description="What robot holding after the action")
    condition: Optional[str] = Field(
        None,
        description="Condition for conditional actions 'if'."
    )
    details: Optional[List["PlanStep"]] = Field(
        None,
        description="Sub-actions or nested actions for composite actions like 'for_each' or 'if'."
    )


class RobotTextPlan(BaseModel):
    robot_id: str = Field(..., description="Unique_identifier for the robot.")
    plan: List[str] = Field(..., description="List of sequential steps of available actions")

class RobotPlan(BaseModel):
    robot_id: str = Field(..., description="Unique identifier for the robot.")
    plan: List[PlanStep] = Field(..., description="List of sequential steps of available actions.")


class MultiRobotPlan(BaseModel):
    plans: List[RobotPlan] = Field(..., description="List of plans for each robot.")


# plan_parser = PydanticOutputParser(pydantic_object=RobotTextPlan)
# plan_parser_format = plan_parser.get_format_instructions()


if __name__ == '__main__':
    basket = ContainerObject(
        id="basket_1",
        type="basket",
        current_location="here",
        compartments={
            "left": [],
            "right": []
        },
        status="idle",
        carrier=None
    )
    print(basket)
