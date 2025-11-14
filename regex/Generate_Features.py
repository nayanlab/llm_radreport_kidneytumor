import numpy as np
import pandas as pd
import regex as re
from datetime import datetime

today_date = datetime.today().strftime('%Y-%m-%d')

def segment_narrative(narrative):
    """
    creates a segmented narrative
    :narrative: the report's narrative for that row
    :return: the narrative segmented to include relevant text with less extraneous text
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
    Fills in errors/missing data for creation of segmented narrative
    :row: row from dataframe on which apply the function
    :return: the updated segmented narrative field
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


def narrative_imp_combined(row):
    """
    creates a concatenated narrative and impression
    :row: row from dataframe on which apply the function
    :return: the narrative and impression concatenated
    """
    return str(row['narrative']) + " " + str(row['impression'])

def impression_fillednarrative(row):
    """
    creates a field that is the most likely place to find the relevant information
    :row: row from dataframe on which apply the function
    :return: the impression if available, the narrative if not
    """
    if pd.notnull(row['impression']):
        return row['impression']
    else:
        return row['narrative']


# DECLARE INPUT FILES HERE:
# Input file should at a minimum have the features 'narrative' and 'impression'
# Folder Location:
path = ''
# File Name
df = pd.read_excel(fr'{path}\filename.xlsl')


# Create the new column 'narrative_imp_combined' 
df['narrative_imp_combined'] = df.apply(narrative_imp_combined, axis=1)

# Update the 'impression_fillednarrative' column by applying the function row-wise.
df['impression_fillednarrative'] = df.apply(impression_fillednarrative, axis =1) 

# Create the new column 'segmented_narrative' by applying the function to 'narrative'
df['segmented_narrative'] = df['narrative'].apply(segment_narrative)

# Update the 'segmented_narrative' column by applying the function row-wise for missing data
df['segmented_narrative'] = df.apply(fill_missing_segmented_narrative, axis=1)



# Output to a file to use as an input file for regex tasks
df.to_excel(f'input_{today_date}.xlsx', index=False)