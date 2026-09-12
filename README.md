# ResolveAI — Autonomous Customer Resolution Agent

## 🚀 Overview

ResolveAI is an Agentic AI system designed to autonomously resolve customer issues by interacting with simulated enterprise systems.

Unlike a normal chatbot that only generates responses, ResolveAI can:

* Understand the customer's goal
* Retrieve customer, order, inventory, and policy information
* Make decisions based on available evidence
* Execute actions such as replacement, refund, or cancellation
* Observe the result of its actions
* Detect failures or changing conditions
* Replan and choose an alternative action
* Verify the final outcome
* Escalate only when the issue cannot be safely resolved

## 🎯 Problem Statement

Build an autonomous customer resolution agent that can investigate and resolve customer issues across multiple simulated enterprise systems.

The agent should be able to retrieve relevant information, select an appropriate resolution, execute the required action, verify the result, and adapt when the original plan fails because of inventory, policy, or system constraints.

## 💡 Example Scenario

A customer reports:

> "My headphones arrived damaged. I want a replacement."

The agent will:

1. Understand the customer's request
2. Verify the customer and order
3. Check the replacement policy
4. Check product inventory
5. Select the best replacement option
6. Execute the replacement
7. Detect if the selected warehouse becomes unavailable
8. Replan using another available warehouse
9. Execute the alternative replacement
10. Verify that the replacement was successfully created
11. Provide the final outcome

## 🧠 Agentic Workflow

```text
Customer Request
       ↓
Understand Goal
       ↓
Retrieve Information
       ↓
Check Policy & Constraints
       ↓
Make Decision
       ↓
Execute Action
       ↓
Observe Result
       ↓
 ┌─────┴─────┐
 │           │
Success    Failure
 │           │
 │        Replan
 │           ↓
 │      Alternative
 │        Action
 │           ↓
 └─────→ Verify
            ↓
      Final Outcome
```

## 🛠️ Technology Stack

* Python
* LLM
* FastAPI
* SQLite
* Streamlit
* RAG / Policy Retrieval
* REST APIs
* GitHub

## 👥 Tea
