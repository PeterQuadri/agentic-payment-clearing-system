import json
from workflows.payment_flow import PaymentFlow
from config import MOCK_DATA_PATH
from utils.display import print_transaction_report


def main():
   with open(f"{MOCK_DATA_PATH}transactions.json") as f:
       txns = json.load(f)


   flow = PaymentFlow()
   results = []
   for txn in txns:
       res = flow.run(txn)
       print_transaction_report(res)
       results.append(res)


if __name__ == "__main__":
   main()
