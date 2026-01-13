from langchain_groq import ChatGroq
from config import GROQ_MODEL, GROQ_API_KEY


class DecisionAgent:
   def __init__(self):
       self.llm = ChatGroq(model=GROQ_MODEL, temperature=0.3, groq_api_key=GROQ_API_KEY)


   def decide(self, compliance_out, fraud_out, txn):
       if compliance_out[0] == "FAIL":
           return "REJECT", compliance_out[1]
       if "HIGH" in fraud_out:
           prompt = f"""
           Transaction: {txn}
           Fraud analysis: {fraud_out}
           Reason why this should be held.
           Start your response with a concise single-sentence summary of the decision.
           Then provide a detailed explanation.
           """
           ans = self.llm.invoke([
               {"role": "system", "content": "You decide why a transaction is held. Always start with a 1-sentence summary."},
               {"role": "user", "content": prompt}
           ])
           return "HOLD", ans.content
       prompt = f"""
       Transaction: {txn}
       Compliance OK
       Fraud analysis: {fraud_out}
       Give a clear reason for approval.
       Start your response with a concise single-sentence summary of the decision.
       Then provide a detailed explanation.
       """
       ans = self.llm.invoke([
           {"role": "system", "content": "You decide why a transaction is approved. Always start with a 1-sentence summary."},
           {"role": "user", "content": prompt}
       ])
       return "APPROVE", ans.content
