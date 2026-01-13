from agents.intake_agent import IntakeAgent
from agents.compliance_agent import ComplianceAgent
from agents.fraud_agent import FraudAgent
from agents.decision_agent import DecisionAgent
from agents.settlement_agent import SettlementAgent


class PaymentFlow:
   def __init__(self):
       self.intake = IntakeAgent()
       self.compliance = ComplianceAgent()
       self.fraud = FraudAgent()
       self.decision = DecisionAgent()
       self.settlement = SettlementAgent()


   def run(self, txn):
       ok, intake_msg = self.intake.validate(txn)
       if not ok:
           reason = intake_msg
           status = "REJECT"
          
           # Create a minimal record for the ledger even if it failed intake
           self.settlement.settle(txn, status, reason)
          
           return {
               "transaction_id": txn["transaction_id"],
               "final": status,
               "reason": reason
           }


       compliance_res = self.compliance.check(txn)
       fraud_res = self.fraud.analyze(txn)
       decision_res = self.decision.decide(compliance_res, fraud_res, txn) # Returns (status, reason)
      
       status = decision_res[0]
       reason = decision_res[1]
      
       # Process settlement
       # Extract just the first line/sentence for the ledger to keep it clean
       ledger_reason = reason.strip().split('\n')[0]
       self.settlement.settle(txn, status, ledger_reason)


       return {
           "transaction_id": txn["transaction_id"],
           "compliance": compliance_res,
           "fraud": fraud_res,
           "final": status,
           "reason": reason
       }
