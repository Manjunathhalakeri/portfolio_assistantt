import os
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import (
    AzureChatCompletion,
    AzureChatPromptExecutionSettings
)
from dotenv import load_dotenv

load_dotenv()

def build_kernel() -> Kernel:
    kernel = Kernel()
    kernel.add_service(
        AzureChatCompletion(
            service_id="chat",
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION")
        )
    )
    return kernel


def create_query_agent() -> ChatCompletionAgent:
    """
    Agent 1 — QueryAgent.
    Job: Take the raw user question and rewrite it
    into a clear, structured instruction for the SQL agent.
    No DB access. No SQL. Just understanding intent.
    """
    kernel = build_kernel()

    return ChatCompletionAgent(
        kernel=kernel,
        name="QueryAgent",
        instructions="""
        You are an expert at understanding investment-related questions.

        YOUR JOB:
        Take the user's natural language question and rewrite it as a
        clear, precise instruction that a SQL agent can act on.

        OUTPUT FORMAT — always return exactly this structure:
        INTENT: <one line — what the user wants to know>
        FILTERS: <any filters mentioned — investor_id, fund_type, date range, etc.>
        METRIC: <what to calculate or return — returns%, amount, count, list>
        CLARIFIED_QUESTION: <rewritten version of the question, precise and unambiguous>

        EXAMPLES:

        Input: "which of my funds are doing well?"
        INTENT: Find funds with positive returns
        FILTERS: investor_id = provided
        METRIC: return percentage per fund
        CLARIFIED_QUESTION: List all funds for the given investor where
        current_value > invested_amount, ordered by return percentage descending.

        Input: "show me my SIPs"
        INTENT: List all active SIP investments
        FILTERS: investor_id = provided, is_sip = true
        METRIC: fund name, sip_amount, start_date, current return
        CLARIFIED_QUESTION: Fetch all portfolios where is_sip is true
        for the given investor, showing fund name, monthly SIP amount,
        start date, and return percentage.

        Never generate SQL. Never access any database.
        Only clarify and structure the question.
        """
    )











# ── temporary test block ──────────────────────────
if __name__ == "__main__":
    import asyncio
    from semantic_kernel.contents import ChatHistory

    async def test():
        agent = create_query_agent()
        history = ChatHistory()
        
        history.add_user_message(
            "investor_id: 1\n"
            "question: Which of my SIPs are giving good returns?"
        )

        print("Query Agent Output:")
        async for response in agent.invoke(history):
            print(response.content)

    asyncio.run(test())