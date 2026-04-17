from typing import Annotated
from semantic_kernel.functions import kernel_function


class FormatPlugin:
    """
    Native functions for formatting data.
    No LLM involved — pure Python.
    Fast, free, always consistent.
    """

    @kernel_function(
        name="format_currency",
        description="Formats a number as Indian Rupee currency string with ₹ symbol"
    )
    def format_currency(
        self,
        amount: Annotated[float, "The amount to format in INR"]
    ) -> str:
        """Converts 120000 → ₹1,20,000"""
        amount = float(amount)
        # Indian number formatting (lakhs/crores style)
        is_negative = amount < 0
        amount = abs(amount)

        # Split into integer and decimal
        int_part = int(amount)
        decimal_part = round(amount - int_part, 2)

        # Indian comma formatting: last 3 digits, then groups of 2
        s = str(int_part)
        if len(s) > 3:
            last3 = s[-3:]
            rest = s[:-3]
            groups = []
            while len(rest) > 2:
                groups.append(rest[-2:])
                rest = rest[:-2]
            if rest:
                groups.append(rest)
            groups.reverse()
            formatted = ",".join(groups) + "," + last3
        else:
            formatted = s

        result = f"₹{formatted}"
        if decimal_part > 0:
            result += f".{int(decimal_part * 100):02d}"
        if is_negative:
            result = f"-{result}"

        return result

    @kernel_function(
        name="calculate_return_percentage",
        description="Calculates return percentage given invested amount and current value"
    )
    def calculate_return_percentage(
        self,
        invested_amount: Annotated[float, "Original amount invested"],
        current_value: Annotated[float, "Current market value"]
    ) -> str:
        """Returns formatted return percentage with gain/loss indicator."""
        invested = float(invested_amount)
        current = float(current_value)

        if invested == 0:
            return "0.00%"

        pct = ((current - invested) / invested) * 100
        gain_loss = "gain" if pct >= 0 else "loss"
        symbol = "▲" if pct >= 0 else "▼"

        return f"{symbol} {abs(pct):.2f}% {gain_loss}"

    @kernel_function(
        name="summarize_portfolio",
        description="Takes total invested and current value, returns a one-line portfolio summary"
    )
    def summarize_portfolio(
        self,
        total_invested: Annotated[float, "Total amount invested across all funds"],
        total_current: Annotated[float, "Total current value across all funds"],
        num_funds: Annotated[int, "Number of funds in portfolio"]
    ) -> str:
        """Returns a clean one-line portfolio summary."""
        invested = float(total_invested)
        current = float(total_current)
        gain = current - invested
        pct = ((current - invested) / invested) * 100 if invested > 0 else 0
        direction = "up" if gain >= 0 else "down"

        return (
            f"Portfolio of {num_funds} funds | "
            f"Invested: ₹{invested:,.0f} | "
            f"Current: ₹{current:,.0f} | "
            f"{direction} {abs(pct):.2f}%"
        )