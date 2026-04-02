# Radiology Report Preprocessing Script

## Overview

This script preprocesses radiology report data stored in an Excel file to generate text fields that can be used for the two large language model (LLM) extraction approaches employed in this study:

- **AI-Dependent**: uses the full narrative and impression text concatenated in a one pass fashion
- **AI-Assisted**: attempts to isolate targetted and kidney-specific text when possible

The script reads an input Excel file, applies several text-processing steps, and outputs a new Excel file with additional derived columns.

---

## Input

The input file must be an Excel file (`.xlsx`) containing at least the following columns:

- `narrative`
- `impression`

An example input file is provided by the following name:

`10_sample_input.xlsx`

You can change the input filename in this line of the script:

```python
df = pd.read_excel('10_sample_input.xlsx')
```

---
## Output

The script creates a new Excel file named with the current date in the format:

`segmented_DDMonthYYYY.xlsx`

---

## Processing Steps

### 1. Combine narrative and impression for AI-Dependent input
A new column called `narrative_imp_combined` is created by concatenating:
- `narrative`
- `impression`

This provides a full-text input approach for LLM extraction.



### 2. Recover missing impression text
If the `impression` column is empty, the script searches the `narrative` field for the text patterns:
- `impression:`
- `impressions:`

If found, that text is extracted and placed into the `impression` column.



### 3. Segment kidney-specific narrative text
The script attempts to isolate kidney-related content from the `narrative` field by identifying sections beginning with:
- `kidneys:`
- `kidneys and ureters:`

Text is captured until the next likely section header.



### 4. Fill missing segmented narrative
If no structured kidney section is found:
- the script looks for a `kidney:` section
- otherwise, it defaults to the full original `narrative`
- Thus, if no kidney-specific section is identified, the script defaults to using the full narrative rather than discarding data.


This ensures `segmented_narrative` is populated.



### 5. Create fallback text for AI-Assisted input
A new column `impression_fillednarrative` is created:
- uses `impression` if available
- otherwise fills with `segmented_narrative`


---

## Dependencies

Install the required packages before running the script:
- `pandas`
- `datetime`
- `re`

---

## How to Run

1. Place your input Excel file (e.g., `10_sample_input.xlsx`) in the same directory as the script.
2. Update the file path in the script if needed:

```python
df = pd.read_excel('10_sample_input.xlsx')
```

3. Run the script:

```bash
python your_script_name.py
```

4. A new Excel file will be generated in the same directory with the processed data.

---

