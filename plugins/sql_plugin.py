import pandas as pd
from typing import Annotated
from sqlalchemy import text
from semantic_kernel.functions import kernel_function
from db.connection import AsyncSessionLocal

class SQLPlugin:

    @kernel_function(
        name="execute_sql",
        description="Executes a PostgreSQL SELECT query and returns results as formatted text. Use this to fetch investment data."
    )
    async def execute_sql(
        self,
        sql_query: Annotated[str, "A valid PostgreSQL SELECT query to execute"]) -> str:
        """Runs the SQL and returns results as readable text."""

        # Safety check — only allow SELECT
        if not sql_query.strip().upper().startswith("SELECT"):
            return "Error: Only SELECT queries are allowed."

        try:
            async with AsyncSessionLocal() as session:
                result = await session.execute(text(sql_query))
                rows = result.fetchall()
                columns = result.keys()

                if not rows:
                    return "No data found for this query."

                # Convert to DataFrame for clean formatting
                df = pd.DataFrame(rows, columns=columns)
                return df.to_markdown(index=False)

        except Exception as e:
            # Return error to agent so it can self-correct
            return f"SQL Error: {str(e)}"
        



# ── temporary test block ──────────────────────────
if __name__ == "__main__":
    import asyncio

    async def test():
        plugin = SQLPlugin()
        
        # Simple query — just fetch all funds for investor 1
        result = await plugin.execute_sql(
            "SELECT fund_name, invested_amount, current_value FROM portfolios WHERE investor_id = 1"
        )
        print("DB Result:")
        print(result)

    asyncio.run(test())