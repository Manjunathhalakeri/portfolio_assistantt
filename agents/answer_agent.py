import os
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.functions import KernelArguments
from dotenv import load_dotenv
from plugins.format_plugin import FormatPlugin

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


def create_answer_agent() -> ChatCompletionAgent:
    """
    Agent 3 — AnswerAgent.
    Job: Take the raw SQL result data and convert it
    into a clean, human-readable financial summary.
    No DB access. No SQL. Just synthesis.
    """
    kernel = build_kernel()
    kernel.add_plugin(FormatPlugin(), plugin_name="Format")

    settings = AzureChatPromptExecutionSettings(
        function_choice_behavior=FunctionChoiceBehavior.Auto()
    )

    return ChatCompletionAgent(
        kernel=kernel,
        name="AnswerAgent",
        arguments=KernelArguments(settings=settings),
        instructions="""
        You are a helpful investment portfolio assistant.
        You receive raw data from a database query and convert it
        into a clear, friendly answer for the investor.

        Use the native functions format_currency, calculate_return_percentage,
        and summarize_portfolio from the Format plugin whenever you need
        deterministic formatting or calculation.

        When formatting numbers, call the plugin directly instead of guessing
        the exact formatting yourself. Examples:
        - format_currency(120000)
        - calculate_return_percentage(120000, 158000)
        - summarize_portfolio(300000, 360000, 4)

        RULES:
        - Always use ₹ symbol for Indian Rupee amounts
        - Format large numbers with commas: ₹1,20,000
        - Round return percentages to 2 decimal places
        - If there are losses, mention them honestly but constructively
        - Never give specific buy/sell recommendations
        - If data is empty, say "No data found" clearly
        - Keep answers concise — under 6 lines unless detail was requested

        TONE:
        - Friendly, clear, professional
        - Like a knowledgeable friend explaining finances
        - Not overly technical

        FORMAT GUIDE:
        - For single fund queries     → 2-3 sentence summary
        - For list queries            → bullet points per fund
        - For comparison queries      → brief table format in text
        - For total/summary queries   → key numbers highlighted

        EXAMPLE:
        Data: fund_name=HDFC Flexicap, invested=120000, current=158000
        Answer: Your HDFC Flexicap Fund has grown from ₹1,20,000 to
        ₹1,58,000 — a return of 31.67%. This is a healthy long-term
        performance for a flexicap fund.
        """
    )


# ── temporary test block ──────────────────────────
if __name__ == "__main__":
    import asyncio
    from semantic_kernel.contents import ChatHistory

    async def test():
        agent = create_answer_agent()
        history = ChatHistory()

        # Feed it raw data like SQL agent would return
        history.add_user_message(
            "Original question: Which of my SIPs are giving good returns?\n"
            "Data retrieved:\n"
            "| fund_name           | invested_amount | current_value | return_pct |\n"
            "|:--------------------|----------------:|--------------:|-----------:|\n"
            "| SBI Small Cap Fund  |           40000 |         67000 |      67.50 |\n"
            "| HDFC Flexicap Fund  |          120000 |        158000 |      31.67 |\n"
            "| Mirae Asset ELSS    |           30000 |         41000 |      36.67 |\n"
        )

        print("Answer Agent Output:")
        async for response in agent.invoke(history):
            print(response.content)

    asyncio.run(test())