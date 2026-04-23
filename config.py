from pathlib import Path

# USER EDIT: set your input folder here
INPUT_FOLDER = Path("input")

# USER EDIT: set your output folder here
OUTPUT_FOLDER = Path("output")

# USER EDIT: change this filename
DEFAULT_INPUT_FILENAME = "sample_media_landscape.xlsx"

# USER EDIT: change this file path
DEFAULT_INPUT_FILEPATH = INPUT_FOLDER / DEFAULT_INPUT_FILENAME

# USER EDIT: change this sheet name
DEFAULT_SHEET_NAME = "MediaData"

# USER EDIT: change this column name
DEFAULT_YEAR_COLUMN = "Year"
# USER EDIT: change this column name
DEFAULT_CATEGORY_COLUMN = "Media Type"
# USER EDIT: change this column name
DEFAULT_VALUE_COLUMN = "Spend"

# USER EDIT: change this filename
CLEANED_WORKBOOK_FILENAME = "atlas_cleaned_media_data.xlsx"
# USER EDIT: change this filename
POWERPOINT_FILENAME = "atlas_media_charts.pptx"
# USER EDIT: change this filename
SUMMARY_TEXT_FILENAME = "atlas_summary_text.txt"

CHART_EXPORT_DPI = 150  # USER EDIT: change this value if chart resolution should be higher/lower
CHART_FIGSIZE = (10, 6)  # USER EDIT: change this value for chart image size

CHARTS_FOLDER = OUTPUT_FOLDER / "charts"  # USER EDIT: change this file path
REPORTS_FOLDER = OUTPUT_FOLDER / "reports"  # USER EDIT: change this file path
POWERPOINT_FOLDER = OUTPUT_FOLDER / "powerpoint"  # USER EDIT: change this file path
TEXT_FOLDER = OUTPUT_FOLDER / "text"  # USER EDIT: change this file path

BRAND_COLORS = {
    "denim": "#00084C",
    "plum": "#B0228C",
    "ocean": "#4F7FF2",
    "sky": "#00D1F9",
}

BRAND_FONT = "Instrument Sans"
FALLBACK_FONT = "DejaVu Sans"

# USER EDIT: set chart exports on/off
EXPORT_CHARTS_BY_DEFAULT = True
# USER EDIT: set PowerPoint export on/off
EXPORT_POWERPOINT_BY_DEFAULT = True
# USER EDIT: set text export on/off
EXPORT_SUMMARY_TEXT_BY_DEFAULT = True
