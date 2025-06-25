from langchain.chains import LLMChain
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent, Tool
import os
from dotenv import load_dotenv
# from fastapi import FastAPI, Request, HTTPException

# Load environment variables from .env file
load_dotenv()

# app = FastAPI()

# Check if OpenAI API key is available
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key or openai_api_key == "your_openai_api_key_here":
    print("Warning: OPENAI_API_KEY not set or using placeholder value.")
    print("Please set your OpenAI API key in the .env file or as an environment variable.")
    print("You can get an API key from: https://platform.openai.com/api-keys")
    llm = None
    agent = None
else:
    # Initialize the language model
    llm = OpenAI(api_key=openai_api_key, temperature=0.3)
    print("OpenAI API key loaded successfully")

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
def create_tools():
    if llm is None:
        return []
    
    return [
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
tools = create_tools()
if tools and llm:
    agent = initialize_agent(tools, llm, agent_type="zero-shot-react-description", verbose=True)
else:
    agent = None

def handle_user_query(query: str):
    """Handles user queries and returns the response from the LangChain agent."""
    if agent is None:
        return {
            "error": "OpenAI API key not configured. Please set OPENAI_API_KEY in your .env file or environment variables.",
            "instructions": "To fix this:\n1. Get an API key from https://platform.openai.com/api-keys\n2. Create a .env file in the backend directory\n3. Add: OPENAI_API_KEY=your_actual_api_key_here"
        }
    
    try:
        response = agent.invoke(query)
        return response
    except Exception as e:
        return {
            "error": f"Error processing query: {str(e)}",
            "query": query
        }
