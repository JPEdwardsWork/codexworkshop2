from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt
import pandas as pd


def _save(fig, output_path: Path) -> str:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, facecolor="white")
    plt.close(fig)
    return str(output_path)


def export_charts(df: pd.DataFrame, output_folder: Path, colors: Dict[str, str], figsize=(10, 6), font_family="DejaVu Sans") -> Dict[str, str]:
    """Export 5 simple charts and return a map of chart title to file path."""
    output_folder.mkdir(parents=True, exist_ok=True)
    plt.rcParams["font.family"] = font_family
    chart_paths = {}

    yearly = df.groupby(["year", "category"], as_index=False)["value"].sum()
    pivot = yearly.pivot(index="year", columns="category", values="value").fillna(0)
    fig, ax = plt.subplots(figsize=figsize)
    pivot.plot(ax=ax, marker="o")
    ax.set_title("Trend Over Time by Channel")
    ax.set_xlabel("Year")
    ax.set_ylabel("Value")
    chart_paths["Trend Over Time by Channel"] = _save(fig, output_folder / "chart_1_trend_by_channel.png")

    shares = df.groupby("category", as_index=False)["value"].sum().sort_values("value", ascending=False)
    fig, ax = plt.subplots(figsize=figsize)
    ax.pie(shares["value"], labels=shares["category"], autopct="%1.1f%%", startangle=90)
    ax.set_title("Market Share by Media Type")
    chart_paths["Market Share by Media Type"] = _save(fig, output_folder / "chart_2_market_share.png")

    top_cats = shares.head(10).sort_values("value")
    fig, ax = plt.subplots(figsize=figsize)
    ax.barh(top_cats["category"], top_cats["value"], color=colors["ocean"])
    ax.set_title("Ranked Biggest Categories")
    ax.set_xlabel("Value")
    chart_paths["Ranked Biggest Categories"] = _save(fig, output_folder / "chart_3_ranked_categories.png")

    totals = df.groupby("year", as_index=False)["value"].sum().sort_values("year")
    fig, ax = plt.subplots(figsize=figsize)
    ax.bar(totals["year"].astype(str), totals["value"], color=colors["plum"])
    ax.set_title("Total Media Value by Year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Total Value")
    chart_paths["Total Media Value by Year"] = _save(fig, output_folder / "chart_4_total_value_year.png")

    growth = totals.copy()
    growth["growth_pct"] = growth["value"].pct_change() * 100
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(growth["year"], growth["growth_pct"], marker="o", color=colors["sky"])
    ax.axhline(0, linestyle="--", color=colors["denim"], linewidth=1)
    ax.set_title("Year-over-Year Growth (%)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Growth %")
    chart_paths["Year-over-Year Growth (%)"] = _save(fig, output_folder / "chart_5_growth_pct.png")

    return chart_paths
