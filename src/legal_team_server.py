import sys
import logging
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

from camel.agents import ChatAgent
from camel.societies.workforce import Workforce
from camel.toolkits import FunctionTool, SearchToolkit
from camel.messages.base import BaseMessage
from camel.types import ModelPlatformType, ModelType
from camel.models import ModelFactory
from camel.configs import ChatGPTConfig
from dotenv import load_dotenv
from camel.tasks.task import Task
import os
import asyncio
# =====================
# Load the API keys
# =====================
load_dotenv()

def main():
    # ======================
    # Create the model. We are going to use GPT-4o mini
    # ======================

    model = ModelFactory.create(
        model_platform=ModelPlatformType.OPENAI,
        model_type=ModelType.GPT_4O_MINI,
        api_key=os.environ["OPENAI_API_KEY"],
        model_config_dict=ChatGPTConfig(temperature=0.0).as_dict(), # [Optional] the config for model
    )  
    # ======================
    # Initialize Agents
    # ======================

    # Compliance Agent
    compliance_agent = ChatAgent(
        BaseMessage.make_assistant_message(
            role_name="Compliance Agent",
            content=""""
            You are a European tech regulations expert.
            You review the document to check for its compliance against regulations such as GDPR, EU AI regulation, and other relevant regulations.
            Feel free to search the web any additional information as necessary.
            """
        ),
        model=model,
    )

    # Language Clarity Agent
    clarity_agent = ChatAgent(
        BaseMessage.make_assistant_message(
            role_name="Clarity Agent",
            content="""
            You are a language clarifying agent. You review the document and suggest areas that could be simplified.
            Feel free to search any additional information as necessary.
            """
        ),
        model=model,
    )

    # Risk agent
    risk_agent = ChatAgent(
        BaseMessage.make_assistant_message(
            role_name="Risk Agent",
            content="""
            You are a risk agent. 
            You review the document to flag terms that are unfavorable to the company and that could open doors for future legal issues.
            Feel free to search any additional information as necessary.
            """
        ),
        model=model,
    )

    # ======================
    # Workforce Setup
    # ======================

    workforce = Workforce("Contract Review Team")

    workforce.add_single_agent_worker(
        "Compliance Agent who is an expert in Tech regulations in the EU",
        worker=compliance_agent,
        ).add_single_agent_worker(
        "Clarity Agent who has a way with simplifying legal terms",
        worker=clarity_agent,
        ).add_single_agent_worker(
            "Risk Agent is a wizard at finding loopholes in contracts",
            worker=risk_agent,
        )
    mcp = workforce.to_mcp(
        name="A sample workfoce",
        description=workforce.description
        )
    
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()