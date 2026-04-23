from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd


def list_excel_files(folder: Path) -> List[Path]:
    """Return Excel files from a folder."""
    if not folder.exists():
        return []
    return sorted([p for p in folder.iterdir() if p.suffix.lower() in {".xlsx", ".xlsm", ".xls"}])


def load_workbook_sheets(file_path: Path) -> Dict[str, pd.DataFrame]:
    """Load all sheets from a workbook."""
    return pd.read_excel(file_path, sheet_name=None)


def try_default_template(
    sheets: Dict[str, pd.DataFrame],
    default_sheet: str,
    year_col: str,
    category_col: str,
    value_col: str,
) -> Optional[dict]:
    """Try to detect default template quickly."""
    if default_sheet not in sheets:
        return None

    df = sheets[default_sheet]
    required = {year_col, category_col, value_col}
    if not required.issubset(df.columns):
        return None

    return {
        "sheet_name": default_sheet,
        "year_col": year_col,
        "category_col": category_col,
        "value_col": value_col,
    }
