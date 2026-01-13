class Calculator:
   """Simple arithmetic tool for dynamic analysis."""
   @staticmethod
   def add(a, b): return a + b


   @staticmethod
   def sub(a, b): return a - b


   @staticmethod
   def mul(a, b): return a * b


   @staticmethod
   def div(a, b): return a / b if b != 0 else None