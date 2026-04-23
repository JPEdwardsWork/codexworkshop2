import pandas as pd


def build_quality_notes(raw_df: pd.DataFrame, standardized_df: pd.DataFrame) -> pd.DataFrame:
    """Create a beginner-friendly data quality notes table."""
    notes = []

    missing_counts = raw_df.isna().sum()
    for col, cnt in missing_counts.items():
        if cnt > 0:
            notes.append({"issue": "missing_values", "detail": f"Column '{col}' has {cnt} missing values."})

    if not standardized_df.empty:
        dupes = standardized_df.duplicated(subset=["year", "category"]).sum()
        if dupes > 0:
            notes.append(
                {
                    "issue": "duplicate_year_category_rows",
                    "detail": f"Found {dupes} duplicate rows with the same year and category.",
                }
            )

        inconsistent_labels = (
            standardized_df.assign(lower=standardized_df["category"].str.lower())
            .groupby("lower")["category"]
            .nunique()
        )
        inconsistent_count = int((inconsistent_labels > 1).sum())
        if inconsistent_count > 0:
            notes.append(
                {
                    "issue": "possible_inconsistent_labels",
                    "detail": f"Found {inconsistent_count} category labels that differ only by letter case.",
                }
            )

    if not notes:
        notes.append({"issue": "none", "detail": "No major data quality issues were detected."})

    return pd.DataFrame(notes)
