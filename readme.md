# Portfolio Intelligence Agent

Ask investment questions in plain English.
3 AI agents collaborate to query PostgreSQL 
and return financial insights.

## Tech Stack
Python, Semantic Kernel, Azure OpenAI, 
PostgreSQL, FastAPI

## Architecture
QueryAgent → SQLAgent → AnswerAgent

## Example
Input:  "Which SIPs are giving good returns?"
Output: [paste your JSON response here]

## How to Run
pip install -r requirements.txt
uvicorn main:app --reload