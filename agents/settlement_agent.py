import json
import os
from config import MOCK_DATA_PATH


class SettlementAgent:
   def __init__(self):
       self.accounts_file = f"{MOCK_DATA_PATH}accounts.json"
       self.ledger_file = f"{MOCK_DATA_PATH}ledger.json"


   def _load_accounts(self):
       with open(self.accounts_file, 'r') as f:
           return json.load(f)


   def _save_accounts(self, accounts):
       with open(self.accounts_file, 'w') as f:
           json.dump(accounts, f, indent=4)


   def _load_ledger(self):
       if not os.path.exists(self.ledger_file):
           return []
       with open(self.ledger_file, 'r') as f:
           try:
               return json.load(f)
           except json.JSONDecodeError:
               return []


   def _save_ledger(self, ledger_data):
       with open(self.ledger_file, 'w') as f:
           json.dump(ledger_data, f, indent=4)


   def settle(self, txn, status, reason):
       """
       Settle a transaction: update balances if approved, and record to ledger.
       """
       sender_id = txn["sender_id"]
       receiver_id = txn["receiver_id"]
       amount = txn["amount"]
      
       sender_balance = 0
       receiver_balance = 0
      
       accounts = self._load_accounts()
      
       # Helper to find account index
       sender_idx = next((i for i, acc in enumerate(accounts) if acc["account_id"] == sender_id), -1)
       receiver_idx = next((i for i, acc in enumerate(accounts) if acc["account_id"] == receiver_id), -1)
      
       if status == "APPROVE":
           if sender_idx != -1 and receiver_idx != -1:
               accounts[sender_idx]["balance"] -= amount
               accounts[receiver_idx]["balance"] += amount
               self._save_accounts(accounts)
              
       # Get current/final balances for logging
       if sender_idx != -1:
           sender_balance = accounts[sender_idx]["balance"]
       if receiver_idx != -1:
           receiver_balance = accounts[receiver_idx]["balance"]
          
       record = {
           "transaction_id": txn["transaction_id"],
           "sender_id": sender_id,
           "receiver_id": receiver_id,
           "amount": amount,
           "currency": txn["currency"],
           "status": status,
           "timestamp": txn["timestamp"],
           "sender_balance_after": sender_balance,
           "receiver_balance_after": receiver_balance,
           "reason": reason
       }
      
       ledger_data = self._load_ledger()
       ledger_data.append(record)
       self._save_ledger(ledger_data)
      
       return record
