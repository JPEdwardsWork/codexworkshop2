# ATLAS Media Chart Builder (MVP)

ATLAS Media Chart Builder is a small local Python app for non-technical users.

It helps you:
1. load one Excel media file,
2. standardize it into a clean format,
3. review simple charts in a Streamlit dashboard,
4. export files for reporting.

---

## What this app does

This app takes **one local Excel workbook** and exports:
- a cleaned Excel workbook (`standardized_data` and `data_quality_notes` sheets),
- 5 PNG charts,
- a simple PowerPoint deck (title slide + one slide per chart),
- editable summary text for slides.

The app first tries a known default template. If that fails, it gives you a fallback mapping UI where you pick:
- sheet name,
- year column,
- category/media column,
- value column.

---

## Input file you need

You need one Excel workbook (`.xlsx` preferred) with values that can map to:
- year,
- media/category,
- numeric value (for example spend).

A sample file is created automatically by `smoke_test.py` if none exists.

---

## Where to place the input file

Put your file in:

```text
input/
```

Default sample name in `config.py` is:

```text
sample_media_landscape.xlsx
```

You can change this in `config.py`.

---

## Step-by-step setup (local laptop)

### 1) Create a virtual environment

**Windows (PowerShell):**
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Mac/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install requirements

```bash
pip install -r requirements.txt
```

### 3) Run the app

```bash
streamlit run app.py
```

That is the main command to run.

---

## What output to expect

After running exports in the app, outputs are written to:

```text
output/
```

Main files/folders:
- `output/reports/atlas_cleaned_media_data.xlsx`
- `output/charts/*.png` (5 charts)
- `output/powerpoint/atlas_media_charts.pptx`
- `output/text/atlas_summary_text.txt`

---

## How to run the demo notebook

Notebook path:

```text
notebooks/demo_atlas_media_chart_builder.ipynb
```

Start Jupyter:

```bash
jupyter notebook
```

Then open the notebook and run cells top-to-bottom.

---

## 3 likely beginner mistakes (and fixes)

1. **Mistake: “File not found” error**  
   **Fix:** Put your Excel file in `input/` or update `DEFAULT_INPUT_FILENAME` in `config.py`.

2. **Mistake: App loads file but charts look wrong**  
   **Fix:** Use the fallback mapping in the Streamlit sidebar and choose the correct sheet/columns.

3. **Mistake: Export button runs but files not where expected**  
   **Fix:** Check `OUTPUT_FOLDER` and subfolder paths in `config.py`.

---

## Assumptions for this MVP

- You process **one market file at a time**.
- Files are **local only** (no cloud/database).
- Most files are similar to one template, but not always identical.
- Goal is fast, practical workflow over complex automation.

---

## User-editable settings

All key settings are in `config.py` and marked with comments like:
- `# USER EDIT: change this file path`
- `# USER EDIT: change this filename`
- `# USER EDIT: set your input folder here`
- `# USER EDIT: set your output folder here`
- `# USER EDIT: change this sheet name`
- `# USER EDIT: change this column name`

If you are new to Python, start by editing only `config.py`.
