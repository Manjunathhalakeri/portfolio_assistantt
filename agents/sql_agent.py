import os
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import (
    AzureChatCompletion,
    AzureChatPromptExecutionSettings
)
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.functions import KernelArguments        # ← add this
from plugins.sql_plugin import SQLPlugin
from db.schema_info import SCHEMA_DESCRIPTION
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


def create_sql_agent() -> ChatCompletionAgent:
    kernel = build_kernel()
    kernel.add_plugin(SQLPlugin(), plugin_name="SQL")

    settings = AzureChatPromptExecutionSettings(
        function_choice_behavior=FunctionChoiceBehavior.Auto()
    )

    return ChatCompletionAgent(
        kernel=kernel,
        name="SQLAgent",
        arguments=KernelArguments(settings=settings),
        instructions=f"""
        You are an expert PostgreSQL query generator for an investment portfolio system.

        SCHEMA:
        {SCHEMA_DESCRIPTION}

        YOUR JOB:
        1. Receive a user's investment question
        2. Write a correct PostgreSQL SELECT query for it
        3. Use the execute_sql function to run it
        4. If you get a SQL error, fix the query and try again (max 2 retries)
        5. Return the raw data result

        RULES:
        - Only write SELECT queries — never INSERT, UPDATE, DELETE
        - Always use table aliases for clarity
        - For return calculations use: ((current_value - invested_amount) / invested_amount) * 100
        - Limit results to 20 rows unless user asks for more
        """
    )





# ── temporary test block ──────────────────────────
if __name__ == "__main__":
    import asyncio
    from semantic_kernel.contents import ChatHistory

    async def test():
        agent = create_sql_agent()
        history = ChatHistory()

        # Feed it the clarified question from Step 3
        history.add_user_message(
            "investor_id: 1\n"
            "INTENT: Find SIP investments with positive returns\n"
            "FILTERS: investor_id = 1, is_sip = true\n"
            "CLARIFIED_QUESTION: List all portfolios where is_sip is true "
            "for investor_id=1, showing fund_name, invested_amount, "
            "current_value and return percentage ordered by returns descending."
        )

        print("SQL Agent Output:")
        async for response in agent.invoke(history):
            print(response.content)

    asyncio.run(test())