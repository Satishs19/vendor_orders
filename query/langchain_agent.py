import os
import pandas as pd
from sqlalchemy import create_engine
from langchain_openai import OpenAI
from langchain_ollama import OllamaLLM
from langchain_experimental.agents import create_pandas_dataframe_agent
from dotenv import load_dotenv

# Load environment variables for OpenAI
# load_dotenv()
# openai_key = os.getenv("OPENAI_API_KEY")

# Create LangChain LLM and Agent
# llm = OpenAI(temperature=0, api_key=openai_key)
llm = OllamaLLM(model="llama3:8b")
engine = create_engine('sqlite:///db.sqlite3')  
df = pd.read_sql("SELECT * FROM metrics_vendormetrics", con=engine)
df['vendor_id'] = df['vendor_id'].astype(str) # Ensure vendor_id is string type not integer

agent = create_pandas_dataframe_agent(
    llm,
    df,
    verbose=True,
    allow_dangerous_code=True
)


def answer_question(question: str) -> str:
    prompt = f"Important: 'vendor_id' is always a string like 'V001', 'V004', etc. Never treat vendor_id as a number. \nQuestion: {question}"
    return agent.run(prompt)