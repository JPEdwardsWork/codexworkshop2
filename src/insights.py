import pandas as pd


def generate_summary_text(df: pd.DataFrame) -> str:
    """Rule-based insights for slide headline text."""
    if df.empty:
        return "No data available to summarize."

    totals = df.groupby("year", as_index=False)["value"].sum().sort_values("year")
    top_categories = df.groupby("category", as_index=False)["value"].sum().sort_values("value", ascending=False)

    latest_year = int(totals.iloc[-1]["year"])
    latest_total = float(totals.iloc[-1]["value"])

    if len(totals) > 1:
        previous_total = float(totals.iloc[-2]["value"])
        yoy = ((latest_total - previous_total) / previous_total * 100) if previous_total else 0
    else:
        yoy = 0.0

    top_3 = ", ".join(top_categories.head(3)["category"].tolist())
    outlier_category = top_categories.iloc[0]["category"]
    outlier_value = top_categories.iloc[0]["value"]

    return (
        f"Top 3 headline insights:\n"
        f"1) {latest_year} total media value is {latest_total:,.0f} ({yoy:+.1f}% vs previous year).\n"
        f"2) Highest-contributing categories are: {top_3}.\n"
        f"3) Potential outlier: '{outlier_category}' contributes {outlier_value:,.0f} in total value.\n\n"
        f"Edit this text in the app before exporting if needed."
    )
