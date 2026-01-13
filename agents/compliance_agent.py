import json
from langchain_groq import ChatGroq
from config import GROQ_MODEL, GROQ_API_KEY, MOCK_DATA_PATH




class ComplianceAgent:
  def __init__(self):
      with open(f"{MOCK_DATA_PATH}compliance.json") as f:
          self.rules = json.load(f)
      self.llm = ChatGroq(model=GROQ_MODEL, temperature=0.3, groq_api_key=GROQ_API_KEY)




  def check(self, txn):
      sender_black = txn["sender_id"] in self.rules["blacklisted_accounts"]
      recv_black = txn["receiver_id"] in self.rules["blacklisted_accounts"]
      curr_ok = txn["currency"] in self.rules["allowed_currencies"]




      if sender_black or recv_black or not curr_ok:
          prompt = f"""
          Transaction: {txn}
          Compliance rules: {self.rules}
          Explain whether this fails compliance and why.
          Start your response with a concise single-sentence summary of the decision.
          Then provide a detailed explanation.
          """
          ans = self.llm.invoke([
              {"role": "system", "content": "You assess compliance logically. Always start with a 1-sentence summary."},
              {"role": "user", "content": prompt}
          ])
          return "FAIL", ans.content
      else:
          prompt = f"""
          Transaction: {txn}
          Compliance rules: {self.rules}
          Explain whether this passes compliance and why.
          Start your response with a concise single-sentence summary of the decision.
          Then provide a detailed explanation.
          """
          ans = self.llm.invoke([
              {"role": "system", "content": "You assess compliance logically. Always start with a 1-sentence summary."},
              {"role": "user", "content": prompt}
          ])
          return "PASS", ans.content
