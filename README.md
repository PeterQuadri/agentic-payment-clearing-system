# agentic-payment-clearing-system
Overview

This project implements the core logic of a payment gateway — a Payment Clearing System.

It evaluates incoming payment transactions, checks for validity, compliance, and fraud, and decides whether a transaction should be approved, held, or rejected.

One question only:
Should this payment be allowed?

Architecture
User Wallet
     ↓
AI Clearing System
(Intake → Compliance → Fraud → Decision)
     ↓
Settlement Engine
(Ledger & Balances)
     ↓
Merchant Wallet

Agent Pipeline

The system uses 5 specialized agents in a sequential pipeline:

Transaction Intake (Gatekeeper)

Rule-based validation

Checks user existence and sufficient balance

Compliance Agent (Law Officer)

Enforces blacklists and rules

Uses an LLM to explain violations

Fraud Agent (Detective)

Detects abnormal spending patterns

Flags transactions > 2× user’s average

Assigns risk: LOW / MEDIUM / HIGH

Decision Agent (Judge)

Aggregates results

Rules:

Compliance FAIL → REJECT

Fraud HIGH → HOLD

Otherwise → APPROVE

Produces a human-readable explanation

Settlement Agent (Accountant)

Updates balances if approved

Writes all outcomes to an immutable ledger

Data & State

accounts.json — user balances

transactions.json — incoming requests

ledger.json — immutable history

compliance.json — rules & blacklists

State updates are file-based, with a single settlement authority.

Key Concepts Demonstrated

Agent-based system design

Hybrid rule-based + LLM decision making

Tool-assisted reasoning (calculator for fraud thresholds)

Sequential pipeline coordination

Explainable AI decisions

Disclaimer

This is a logical simulation, not a real payment processor.
No real money is moved.
