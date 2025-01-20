import json
import os
import logging
import re
from pathlib import Path
from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai.chat_models import ChatOpenAI
from scripts.sturcture.frame import *
from scripts.sturcture.graphs import GraphManager


class Planner:
    def __init__(self, api_key, is_vis=True):

        self.data = os.path.join(Path(__file__).parent.parent, "data")
        gpt_config = self.read_json("gpt_config.json")
        self.model = ChatOpenAI(model=gpt_config["model"],
                                temperature=gpt_config["temperature"],
                                api_key=api_key)
        self.manager = GraphManager()
        self.graph_text, self.graph_json = self.set_graph(is_vis=is_vis)

        self.domain_knowledge = self.get_prompt_text("domain")
        self.system_message = SystemMessagePromptTemplate.from_template(self.get_prompt_text("system"))
        self.human_message = HumanMessagePromptTemplate.from_template(self.get_prompt_text("human"))

        self.nodes = set()

    def read_json(self, file_name):
        with open(os.path.join(self.data, file_name), "r") as json_file:
            data = json.load(json_file)
        return data

    def set_graph(self, is_vis=False):
        # Add locations
        env_data = self.read_json(file_name="environment.json")
        # location
        for name, descriptions in env_data["location"].items():
            self.manager.add_location(name, descriptions["description"])
        # objects
        for name, descriptions in env_data["objects"].items():
            # objects
            if descriptions["type"] == "basket":
                basket = ContainerObject(
                    id=descriptions["id"],
                    type="basket",
                    current_location=descriptions["current_location"],
                    compartments=descriptions["compartments"],
                    status=descriptions["status"],
                    carrier=None if not descriptions["carrier"] else descriptions["carrier"]
                )
                self.manager.add_object(basket)
            # fruits
            elif descriptions["type"] == "fruit":
                fruit = FruitObject(
                    is_ripe=descriptions["is_ripe"],
                    is_rotten=descriptions["is_rotten"]
                )
                self.manager.add_object(fruit)
            # raise error
            else:
                pass
        # Add robots
        robot_data = self.read_json(file_name="robot.json")
        for name, descriptions in robot_data.items():
            robot = Robot(
                id=descriptions["id"],
                description=descriptions["description"],
                current_location=descriptions["current_location"],
                action_set=descriptions["action_set"],
                status=descriptions["status"],
                contents=descriptions["contents"],
                now_holding=None if not descriptions["now_holding"] else descriptions["now_holding"])
            self.manager.add_robot(robot)

        # Add edges
        def refine_edge(node1, node2, edge_list):
            edge = (node1, node2)
            if edge not in edge_list and (node2, node1) not in edge_list:  # 중복 방지
                edge_list.append(edge)
            return edge_list

        edges = []
        for node, details in env_data["location"].items():
            for connected_node in details["to_edge"]:
                edges = refine_edge(node, connected_node, edges)
        for edge in edges:
            self.manager.add_edge(edge[0], edge[1])

        # visualize the graph
        if is_vis:
            self.manager.visualize()
        graph_text = self.manager.describe_graph()
        graph_json = json.dumps(self.manager.export_graph_as_json(), indent=4)
        return graph_text, graph_json

    def get_prompt_text(self, role):
        with open(os.path.join(self.data, f"{role}.txt"), "r") as text_file:
            content = text_file.read()
        return content

    def offline_planning(self, instruction):
        plan_parser = PydanticOutputParser(pydantic_object=RobotTextPlan)
        plan_parser_format = plan_parser.get_format_instructions()

        language_plan_prompt = ChatPromptTemplate.from_messages(
            [self.system_message, self.human_message]
        ).partial(domain_knowledge=self.domain_knowledge, env_text=self.graph_text, env_json=self.graph_json,
                  output_format=plan_parser_format)

        chain = language_plan_prompt | self.model.with_structured_output(RobotPlan)
        output = chain.invoke(instruction)

        # self.generate_nodes(output)
        self.log_conversation(output.model_dump_json(indent=4))
        self.log_conversation(self.nodes)
        return output

    def log_conversation(self, content):
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file_name = f"result/conversation_{current_time}.txt"
        logging.basicConfig(
            filename=log_file_name,  # 파일 이름
            level=logging.INFO,      # 로그 레벨 설정
            format="%(asctime)s - %(levelname)s - %(message)s"  # 로그 포맷
        )
        logging.info(content)

    def generate_nodes(self, plans):
        for plan in plans.plan:
            if plan.lstrip().startswith(tuple("0123456789")):
                alphabet_index = next((i for i, char in enumerate(plan) if char.isalpha()), None)
                end = plan.find('|', alphabet_index)
                result = plan[alphabet_index:end].strip()
                if not ("else" or "if" or "for") in result.lower():
                    self.nodes.add(result)
        self.nodes = sorted(self.nodes)
        print(self.nodes)
