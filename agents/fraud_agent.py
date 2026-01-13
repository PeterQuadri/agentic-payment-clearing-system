import json
import pandas as pd
from langchain_groq import ChatGroq
from config import GROQ_MODEL, GROQ_API_KEY, MOCK_DATA_PATH
from tools.calculator import Calculator


class FraudAgent:
   def __init__(self):
       with open(f"{MOCK_DATA_PATH}fraud_log.json") as f:
           self.df = pd.DataFrame(json.load(f))
       self.llm = ChatGroq(model=GROQ_MODEL, temperature=0.1, groq_api_key=GROQ_API_KEY)
       self.calc = Calculator()


   def analyze(self, txn):
       history = self.df[self.df["sender_id"] == txn["sender_id"]]
       avg_amt = history["amount"].mean() if not history.empty else 0
       thr = self.calc.mul(avg_amt, 2)


       prompt = f"""
       Transaction: {txn}
       History for sender: {history.to_dict(orient='records')}
       Dynamic threshold: {thr}
       Assess risk level LOW, MEDIUM, or HIGH with reasoning.
       """
       response = self.llm.invoke([
           {"role": "system", "content": "You assess transaction risk given history."},
           {"role": "user", "content": prompt}
       ])
       return response.content
