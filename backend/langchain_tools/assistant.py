from langchain.chains import LLMChain
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent, Tool
import os
# from fastapi import FastAPI, Request, HTTPException

# app = FastAPI()

# Initialize the language model
llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), temperature=0.3)
print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))
# Define prompt templates for user queries
wallet_score_prompt = PromptTemplate(
    input_variables=["wallet_address"],
    template="What is the trustworthiness score of the wallet address {wallet_address}?"
)

fraud_detection_prompt = PromptTemplate(
    input_variables=["wallet_address"],
    template="Can you detect any fraudulent activity associated with the wallet address {wallet_address}?"
)

user_pattern_analysis_prompt = PromptTemplate(
    input_variables=["wallet_address"],
    template="What are the user patterns observed for the wallet address {wallet_address}?"
)

# Define tools for the LangChain assistant
tools = [
    Tool(
        name="Wallet Score",
        func=LLMChain(llm=llm, prompt=wallet_score_prompt).invoke,
        description="Get the trustworthiness score of a wallet address."
    ),
    Tool(
        name="Fraud Detection",
        func=LLMChain(llm=llm, prompt=fraud_detection_prompt).invoke,
        description="Detect fraudulent activity for a wallet address."
    ),
    Tool(
        name="User Pattern Analysis",
        func=LLMChain(llm=llm, prompt=user_pattern_analysis_prompt).invoke,
        description="Analyze user patterns for a wallet address."
    )
]

# Initialize the LangChain agent with the defined tools
agent = initialize_agent(tools, llm, agent_type="zero-shot-react-description", verbose=True)

def handle_user_query(query: str):
    """Handles user queries and returns the response from the LangChain agent."""
    response = agent.invoke(query)
    return response
