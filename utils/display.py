from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.text import Text
from rich.layout import Layout
from rich import box


console = Console()


def print_transaction_report(result):
   """
   Prints a formatted report for a single transaction.
  
   Args:
       result (dict): The result dictionary from PaymentFlow.run()
   """
   txn_id = result.get("transaction_id", "Unknown ID")
  
   # 1. Header
   console.print(f"\n[bold blue]━" * 5)
   console.print(f"[bold white on blue] TRANSACTION REPORT: {txn_id} [/]")
   console.print(f"[bold blue]━" * 5)


   # 2. Compliance Section
   compliance_status, compliance_msg = result.get("compliance", ("UNKNOWN", "No data"))
  
   comp_color = "green" if compliance_status == "PASS" else "red"
   compliance_panel = Panel(
       f"[{comp_color}]{compliance_msg}[/]",
       title=f"[{comp_color}]Compliance: {compliance_status}[/]",
       border_style=comp_color,
       box=box.ROUNDED
   )
   console.print(compliance_panel)


   # 3. Fraud Analysis Section (Markdown)
   fraud_content = result.get("fraud", "")
   if fraud_content:
       fraud_md = Markdown(fraud_content)
       fraud_panel = Panel(
           fraud_md,
           title="[yellow]Fraud Analysis[/]",
           border_style="yellow",
           box=box.ROUNDED
       )
       console.print(fraud_panel)
   else:
       console.print("[italic yellow]No fraud analysis data available.[/]")


   # 4. Final Decision Section
   final_decision = result.get("final", "UNKNOWN")
   reason = result.get("reason", "")
  
   decision_color = "green" if final_decision == "APPROVE" else "red" if final_decision == "REJECT" else "orange1"
  
   # If reason is markdown, render it, otherwise just text
   if reason and ("**" in reason or "#" in reason or "-" in reason):
       reason_content = Markdown(reason)
   else:
       reason_content = Text(str(reason))


   decision_panel = Panel(
       reason_content,
       title=f"[bold {decision_color}]Final Decision: {final_decision}[/]",
       border_style=decision_color,
       box=box.DOUBLE
   )
   console.print(decision_panel)
   console.print("\n")


