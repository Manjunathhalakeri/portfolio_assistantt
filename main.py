import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from semantic_kernel.contents import ChatHistory
from agents.query_agent import create_query_agent
from agents.sql_agent import create_sql_agent
from agents.answer_agent import create_answer_agent

app = FastAPI(
    title="Portfolio Intelligence Agent",
    description="Natural language investment portfolio queries powered by SK agents"
)


class QueryRequest(BaseModel):
    question: str
    investor_id: int = 1


class QueryResponse(BaseModel):
    question: str
    clarified_question: str
    raw_data: str
    answer: str


@app.post("/query", response_model=QueryResponse)
async def query_portfolio(request: QueryRequest):

    try:
        # ── Agent 1: Understand and rewrite the question ──
        query_agent = create_query_agent()
        q_history = ChatHistory()
        q_history.add_user_message(
            f"investor_id: {request.investor_id}\n"
            f"question: {request.question}"
        )
        clarified = ""
        async for r in query_agent.invoke(q_history):
            clarified = str(r.content)

        # ── Agent 2: Generate SQL and fetch data ──
        sql_agent = create_sql_agent()
        s_history = ChatHistory()
        s_history.add_user_message(
            f"investor_id: {request.investor_id}\n{clarified}"
        )
        raw_data = ""
        async for r in sql_agent.invoke(s_history):
            raw_data = str(r.content)

        # ── Agent 3: Synthesize final answer ──
        answer_agent = create_answer_agent()
        a_history = ChatHistory()
        a_history.add_user_message(
            f"Original question: {request.question}\n"
            f"Data retrieved:\n{raw_data}"
        )
        final_answer = ""
        async for r in answer_agent.invoke(a_history):
            final_answer = str(r.content)

        return QueryResponse(
            question=request.question,
            clarified_question=clarified,
            raw_data=raw_data,
            answer=final_answer
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    return {
        "status": "running",
        "agents": ["QueryAgent", "SQLAgent", "AnswerAgent"]
    }