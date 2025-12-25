# agentic-payment-clearing-system

## Overview
This project implements the core logic of a **payment gateway** — a **Payment Clearing System**.

It evaluates incoming payment transactions, checks for **validity, compliance, and fraud**, and decides whether a transaction should be **approved, held, or rejected**.

> **One question only:**  
> *Should this payment be allowed?*

---

## Architecture

User Wallet
↓
AI Clearing System
(Intake → Compliance → Fraud → Decision)
↓
Settlement Engine
(Ledger & Balances)
↓
Merchant Wallet

markdown
Copy code

---

## Agent Pipeline

The system uses **5 specialized agents** in a **sequential pipeline**:

### 1. Transaction Intake Agent (Gatekeeper)
- Rule-based validation
- Verifies users and sufficient balance
- Rejects invalid transactions early

### 2. Compliance Agent (Law Officer)
- Enforces compliance rules and blacklists
- Uses an LLM to explain violations
- Returns **PASS** or **FAIL**

### 3. Fraud Agent (Detective)
- Analyzes user spending behavior
- Flags transactions greater than **2× the user’s average**
- Assigns risk: **LOW / MEDIUM / HIGH**
- Uses a calculator tool for precise thresholds

### 4. Decision Agent (Judge)
- Aggregates compliance and fraud results
- Decision logic:
  - Compliance FAIL → **REJECT**
  - Fraud HIGH → **HOLD**
  - Otherwise → **APPROVE**
- Generates a human-readable explanation

### 5. Settlement Agent (Accountant)
- Updates balances if approved
- Writes all outcomes to an immutable ledger

---

## Data & State Management

- `accounts.json` — user balances  
- `transactions.json` — incoming payment requests  
- `ledger.json` — immutable transaction history  
- `compliance.json` — compliance rules and blacklists  

State is **file-based**, with the Settlement Agent as the single source of truth.

---

## Key Concepts Demonstrated

- Agent-based system design
- Hybrid **rule-based + LLM** decision making
- Tool-assisted reasoning
- Sequential pipeline coordination
- Explainable AI decisions

---

## Disclaimer
This project is a **logical simulation** for learning and demonstration purposes.  
It does **not** move real money or connect to any payment network.
