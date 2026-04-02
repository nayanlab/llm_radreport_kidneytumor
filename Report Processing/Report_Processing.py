import pandas as pd
from datetime import datetime
import re

today_date = datetime.now().strftime("%d%B%Y")
today_date

def extract_impression(row):
    """
    If impression only exists within the narrative field, separates impression using regex
    to put in its own impression field.
    :row: the input row from the dataframe of reports
    :return: the impression if found either on its own or within narrative field, None if none 
    """
    # If 'impression' already has a value, return it
    if pd.notnull(row['impression']):
        return row['impression']
    
    narrative = row['narrative']
    if isinstance(narrative, str):
        # Search for "impression:" or "impressions:" (case-insensitive)
        match = re.search(r'(?i)impression[s]?:\s*(.*)', narrative)
        if match:
            return match.group(1).strip()
    return None

def segment_narrative(narrative):
    """
    If narrative is structured such that kidney specific info can be segmented out using regular expressions,
    this function separates that information and places it in the "segmented narrative" field.
    :narrative: the input narrative for segmentation
    :return: the segmented narrative if possible to create, None if not
    """
    # Check if narrative is a valid string
    if not isinstance(narrative, str):
        return None

    # Use a regex that matches either "kidneys:" or "kidneys and ureters:" (case insensitive)
    match = re.search(r'(?i)kidneys(?:\s+and\s+ureters)?:\s*(.*)', narrative)
    if not match:
        return None
    text_after = match.group(1)
    
    # Look for stopping patterns:
    # 1. A space, one or two digits, a period, and a space (e.g., " 3. " or " 35. ")
    # 2. A space, exactly three capital letters, a colon, and a space (e.g., " ABC: ")
    stop_match = re.search(r'(?=\s\d{1,2}\.\s)|(?=\s[A-Z]{3}:\s)', text_after)
    if stop_match:
        segmented = text_after[:stop_match.start()]
    else:
        segmented = text_after

    return segmented.strip()

def fill_missing_segmented_narrative(row):
    """
    if no segmented narrative is possible, this replaces the segmented narrative field with the origiinal narrative
    :row: the input row from the dataframe of reports
    :return: segmented_narrative field if it already exists, original narrative if not.
    """
    # If segmented_narrative already has a value, return it.
    if pd.notnull(row['segmented_narrative']):
        return row['segmented_narrative']
    
    narrative = row['narrative']
    if isinstance(narrative, str):
        # Search for "kidney:" (singular, case-insensitive) and capture everything after it.
        match = re.search(r'(?i)kidney:\s*(.*)', narrative)
        if match:
            return match.group(1).strip()
        else:
            # If no match is found, use the entire narrative
            return narrative.strip()
    return row['segmented_narrative']

# DECLARE INPUT FILES HERE:
# Input file should at a minimum have the features 'narrative' and 'impression'
# Adjust path as needed.
df = pd.read_excel('10_sample_input.xlsx')

### AI-Dependent ###
# Create a field with narrative and impression simply concatenated
df['narrative_imp_combined'] = (
    df['narrative'].fillna('') + "\n" + df['impression'].fillna('')
)

### AI-Assisted ###
# Update the 'impression' column by seeking impression concatenated to narrative if it exists
df['impression'] = df.apply(extract_impression, axis=1)

# Create the new column 'segmented_narrative' by applying the segmentation function to 'narrative'
df['segmented_narrative'] = df['narrative'].apply(segment_narrative)

# Update the 'segmented_narrative' column to include original narrative if not segmented prior.
df['segmented_narrative'] = df.apply(fill_missing_segmented_narrative, axis=1)

# Create a field in which any row without an impression available has the segmented narrative filled in
df['impression_fillednarrative'] = df['impression'].fillna(df['segmented_narrative'])


# Output to excel file containing features for AI-A or AI-D approaches
df.to_excel(f'segmented_{today_date}.xlsx', index=False)
