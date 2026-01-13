import json
from config import MOCK_DATA_PATH


class IntakeAgent:
   def __init__(self):
       with open(f"{MOCK_DATA_PATH}accounts.json") as f:
           self.accounts = json.load(f)


   def validate(self, txn):
       sender = next((a for a in self.accounts if a["account_id"] == txn["sender_id"]), None)
       receiver = next((a for a in self.accounts if a["account_id"] == txn["receiver_id"]), None)


       if not sender:
           return False, "Sender account not found"
       if not receiver:
           return False, "Receiver account not found"
       if txn["amount"] <= 0:
           return False, "Invalid amount"
       if sender["balance"] < txn["amount"]:
           return False, f"Insufficient funds: Balance {sender['balance']} < Amount {txn['amount']}"
       return True, "Valid transaction"
