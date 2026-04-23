from pathlib import Path

import pandas as pd

import config
from src.charts import export_charts
from src.data_loader import load_workbook_sheets
from src.exporters import export_cleaned_excel, export_powerpoint
from src.insights import generate_summary_text
from src.quality import build_quality_notes
from src.standardizer import standardize_data


def ensure_sample_file() -> Path:
    sample_path = config.INPUT_FOLDER / config.DEFAULT_INPUT_FILENAME
    sample_path.parent.mkdir(parents=True, exist_ok=True)
    if not sample_path.exists():
        df = pd.DataFrame(
            {
                "Year": [2022, 2022, 2023, 2023, 2024, 2024],
                "Media Type": ["TV", "Digital", "TV", "Digital", "TV", "Digital"],
                "Spend": [100, 120, 110, 150, 95, 170],
            }
        )
        with pd.ExcelWriter(sample_path, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name=config.DEFAULT_SHEET_NAME, index=False)
    return sample_path


def main() -> None:
    sample_file = ensure_sample_file()
    sheets = load_workbook_sheets(sample_file)
    raw_df = sheets[config.DEFAULT_SHEET_NAME]

    standardized_df = standardize_data(
        raw_df,
        config.DEFAULT_YEAR_COLUMN,
        config.DEFAULT_CATEGORY_COLUMN,
        config.DEFAULT_VALUE_COLUMN,
    )
    assert not standardized_df.empty, "Standardized data is empty"

    notes_df = build_quality_notes(raw_df, standardized_df)
    assert not notes_df.empty, "No data quality notes were generated"

    chart_paths = export_charts(standardized_df, config.CHARTS_FOLDER, config.BRAND_COLORS, config.CHART_FIGSIZE)
    assert chart_paths, "No charts were exported"
    first_chart_path = Path(next(iter(chart_paths.values())))
    assert first_chart_path.exists(), "First chart file was not created"

    cleaned_excel = export_cleaned_excel(
        standardized_df,
        notes_df,
        config.REPORTS_FOLDER / config.CLEANED_WORKBOOK_FILENAME,
    )
    assert cleaned_excel.exists(), "Cleaned Excel export failed"

    summary_text = generate_summary_text(standardized_df)
    ppt_path = export_powerpoint(chart_paths, summary_text, config.POWERPOINT_FOLDER / config.POWERPOINT_FILENAME)
    assert ppt_path.exists(), "PowerPoint export failed"

    print("Smoke test passed: sample load, standardization, chart export, Excel export, and PowerPoint export all worked.")


if __name__ == "__main__":
    main()
