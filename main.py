import os

from dotenv import load_dotenv

from scripts.planner import Planner

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
tavily_key = os.getenv("TAVILY_API_KEY")
langchain_tracing = os.getenv("LANGCHAIN_TRACING_V2")
langchain_endpoint = os.getenv("LANGCHAIN_ENDPOINT")
langchain_apikey = os.getenv("LANGCHAIN_API_KEY")
langchain_project = os.getenv("LANGCHAIN_PROJECT")


def main():
    load_dotenv()
    planner = Planner(api_key)
    instruction = ("Harvest all the ripe tomatoes. The rotten tomatoes should be placed in the left of the basket "
                   "and the other tomatoes should be put in the right part of the basket.")
    output = planner.offline_planning(instruction=instruction)


def hello():
    print("hi")

def test():
    print("test")

if __name__ == '__main__':
    main()
