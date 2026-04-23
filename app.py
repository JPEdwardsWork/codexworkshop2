from pathlib import Path

import pandas as pd
import streamlit as st

import config
from src.charts import export_charts
from src.data_loader import list_excel_files, load_workbook_sheets, try_default_template
from src.exporters import export_cleaned_excel, export_powerpoint, export_summary_text
from src.insights import generate_summary_text
from src.quality import build_quality_notes
from src.standardizer import standardize_data

st.set_page_config(page_title="ATLAS Media Chart Builder", layout="wide")

st.title("ATLAS Media Chart Builder (MVP)")
st.write("Upload or select one local Excel file, standardize data, preview charts, and export outputs.")

available_files = list_excel_files(config.INPUT_FOLDER)

selected_file = st.selectbox(
    "Select input workbook",
    options=[str(p) for p in available_files] if available_files else [str(config.DEFAULT_INPUT_FILEPATH)],
)

if selected_file:
    file_path = Path(selected_file)
    if not file_path.exists():
        st.warning(f"File not found: {file_path}. Place one workbook in {config.INPUT_FOLDER}/")
        st.stop()

    sheets = load_workbook_sheets(file_path)
    st.sidebar.header("Template / Mapping")

    mapping = try_default_template(
        sheets,
        config.DEFAULT_SHEET_NAME,
        config.DEFAULT_YEAR_COLUMN,
        config.DEFAULT_CATEGORY_COLUMN,
        config.DEFAULT_VALUE_COLUMN,
    )

    if mapping:
        st.sidebar.success("Default template detected.")
    else:
        st.sidebar.warning("Default template not found. Use fallback mapping.")
        sheet_name = st.sidebar.selectbox("Sheet name", list(sheets.keys()))
        columns = list(sheets[sheet_name].columns)
        year_col = st.sidebar.selectbox("Year column", columns)
        category_col = st.sidebar.selectbox("Category/Media column", columns)
        value_col = st.sidebar.selectbox("Value column", columns)
        mapping = {
            "sheet_name": sheet_name,
            "year_col": year_col,
            "category_col": category_col,
            "value_col": value_col,
        }

    raw_df = sheets[mapping["sheet_name"]]
    standardized_df = standardize_data(raw_df, mapping["year_col"], mapping["category_col"], mapping["value_col"])
    notes_df = build_quality_notes(raw_df, standardized_df)

    st.subheader("File status")
    st.write(f"Loaded: `{file_path}` | Rows standardized: **{len(standardized_df)}**")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Cleaned data preview")
        st.dataframe(standardized_df.head(30))
    with col2:
        st.subheader("Data quality notes")
        st.dataframe(notes_df)

    st.sidebar.header("Charts")
    chart_choices = [
        "Trend Over Time by Channel",
        "Market Share by Media Type",
        "Ranked Biggest Categories",
        "Total Media Value by Year",
        "Year-over-Year Growth (%)",
    ]
    selected_charts = st.sidebar.multiselect("Select charts to display", chart_choices, default=chart_choices)

    chart_paths = export_charts(standardized_df, config.CHARTS_FOLDER, config.BRAND_COLORS, config.CHART_FIGSIZE)

    st.subheader("Charts")
    for title in selected_charts:
        if title in chart_paths:
            st.markdown(f"**{title}**")
            st.image(chart_paths[title])

    st.subheader("Editable summary text for slides")
    default_summary = generate_summary_text(standardized_df)
    summary_text = st.text_area("Edit the suggested summary text", value=default_summary, height=220)

    st.sidebar.header("Export actions")
    do_export_excel = st.sidebar.checkbox("Export cleaned Excel", value=True)
    do_export_charts = st.sidebar.checkbox("Export chart PNGs", value=config.EXPORT_CHARTS_BY_DEFAULT)
    do_export_ppt = st.sidebar.checkbox("Export PowerPoint", value=config.EXPORT_POWERPOINT_BY_DEFAULT)
    do_export_text = st.sidebar.checkbox("Export summary text", value=config.EXPORT_SUMMARY_TEXT_BY_DEFAULT)

    if st.button("Run export"):
        exported = []
        if do_export_excel:
            excel_path = export_cleaned_excel(
                standardized_df,
                notes_df,
                config.REPORTS_FOLDER / config.CLEANED_WORKBOOK_FILENAME,
            )
            exported.append(str(excel_path))
        if do_export_charts:
            exported.extend(chart_paths.values())
        if do_export_ppt:
            ppt_path = export_powerpoint(
                chart_paths,
                summary_text,
                config.POWERPOINT_FOLDER / config.POWERPOINT_FILENAME,
            )
            exported.append(str(ppt_path))
        if do_export_text:
            txt_path = export_summary_text(summary_text, config.TEXT_FOLDER / config.SUMMARY_TEXT_FILENAME)
            exported.append(str(txt_path))

        st.success("Export completed.")
        st.write(pd.DataFrame({"output_file": exported}))
