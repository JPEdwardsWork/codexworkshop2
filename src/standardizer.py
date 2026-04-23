import pandas as pd


def standardize_data(df: pd.DataFrame, year_col: str, category_col: str, value_col: str) -> pd.DataFrame:
    """Standardize selected columns to a tidy table format."""
    out = df[[year_col, category_col, value_col]].copy()
    out.columns = ["year", "category", "value"]

    out["year"] = pd.to_numeric(out["year"], errors="coerce")
    out["value"] = pd.to_numeric(out["value"], errors="coerce")
    out["category"] = out["category"].astype(str).str.strip()
    out = out.dropna(subset=["year", "category", "value"])
    out["year"] = out["year"].astype(int)

    return out.reset_index(drop=True)
