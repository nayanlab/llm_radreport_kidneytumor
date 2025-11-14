import numpy as np
import pandas as pd
import regex as re
from datetime import datetime
today_date = datetime.today().strftime('%Y-%m-%d')


def find_phrases(search_text):
    """
    Searches for specified phrases in a given block of text.
    :param search_text: The input text to be searched.
    :param search_class: either "mass" or "cyst"
    :return: A dictionary with phrases as keys and their occurrences as values.
    """
    
    # 'renal mass', 'renal lesion', 'renal tumor',
    # 'kidney tumor', 'kidney mass' , 'kidney lesion',
    # 'pole tumor', 'pole mass', 'pole lesion'
    # r'\b(renal|kidney[s]{0,1}|pole[s]{0,1}) (mass[es]{0,1}|lesion[s]{0,1}|tumor[s]{0,1})\b'
    #
    # 'mass in kidney', 'tumor in kidney', 'lesion in kidney',
    # 'mass in pole', 'tumor in pole', 'lesion in pole',
    # 'mass in upper pole', 'tumor in upper pole', 'lesion in upper pole',
    # 'mass in lower pole', 'tumor in lower pole', 'lesion in lower pole',             
    # r'\b(mass[es]{0,1}|lesion[s]{0,1}|tumor[s]{0,1}) (?:(in|within) )?(?:the )?(?:(right|left) )?kidney[s]{0,1}\b',
    #                
    # 'mass in right upper pole', 'tumor in right upper pole', 'lesion in right upper pole',
    # 'mass in right lower pole', 'tumor in right lower pole', 'lesion in right lower pole',
    # 'mass in left upper pole', 'tumor in left upper pole', 'lesion in left upper pole',
    # 'mass in left lower pole', 'tumor in left lower pole', 'lesion in left lower pole',
    # r'\b(mass[es]{0,1}|lesion[s]{0,1}|tumor[s]{0,1}) (?:(in|within) )?(?:the )?(?:(right|left) )?(?:(upper|lower) )?pole[s]{0,1}\b
    
   
    
    #(?:\s*.{1,10})? -- added occasionally to make it inclusive of unexpected filler words (up to 10 characters) at possible locations
    # \s* used to account for possible errors in white space
        
    # capturing masses
    phrases = {r'\b(?<!no\s|no\snew\s|no\s+suspicious\s+|without\s+)(renal|kidney[s]{0,1}|pole[s]{0,1})\s*(mass|masses|lesion[s]{0,1}|tumor[s]{0,1})\b',
                    r'\b(?<!no\s|no\snew\s|no\s+suspicious\s+|without\s+)(mass|masses|lesion[s]{0,1}|tumor[s]{0,1})\s*(?:(in|within)\s*)?(?:the\s*)?(?:\s*.{1,10})?(?:(right|left)\s*)?(?:\s*.{1,10})?kidney[s]{0,1}\b',
                    r'\b(?<!no\s|no\snew\s|no\s+suspicious\s+|without\s+)(mass|masses|lesion[s]{0,1}|tumor[s]{0,1})\s*(?:\s*.{1,10})?(?:(in|within)\s*)?(?:the\s*)?(?:\s*.{1,10})?(?:(right|left)\s*)?(?:\s*.{1,10})?(?:(upper|lower)\s*)?(?:\s*.{1,10})?pole[s]{0,1}\b',
                    r'(?<!no\s|no\snew\s|no\s+suspicious\s+|without\s+)renal cell carcinoma[s]{0,1}', 
                    r'\b(?<!no\s|no\snew\s|no\s+suspicious\s+|without\s+)(?!simple\s)(complex\s+cyst[s]?|complex\s+cystic\s+lesion[s]?|cyst[s]?\s+with\s+complex\s+feature[s]?)\b',
                    r'\b(?<!no\s|no\snew\s|no\s+suspicious\s+|without\s+)(indeterminate\s+(lesion[s]?|mass[es]?|finding[s]?))\b',
                    r'\b(?<!no\s|no\snew\s|no\s+suspicious\s+|without\s+)(bosniak\s*(2f|iif|iii|iv|v|3|4|5))\b'
                    r'(?<!no\s|no\snew\s|no\s+suspicious\s+|without\s+)(renal\s+neoplasm[s]?)\b',
                    r'(?<!no\s|no\snew\s|no\s+suspicious\s+|without\s+)suspicious\s+for\s+renal\s+\w+\b',
                    r'(?<!no\s|no\snew\s|no\s+suspicious\s+|without\s+)(chromophobe|clear\s+cell|papillary|rcc|renal\s+mass)\b'
                   }
    
    # capturing cystic features of a found mass
    cystic = re.compile(
    r'\b(?<!no\s|no\snew\s|no\s+suspicious\s+|without\s+|no\s+evidence\s+of\s+|not\s+suspicious\s+for\s+)'
    r'(?!simple\s|bosniak\s*(i|ii|1|2)\b)'
    r'(complex\s+cyst[s]?|cystic\s+lesion[s]?|cyst[s]?\s*(with\s+complex\s+features)?|cystic|'
    r'hypoechoic|calcified|calcifications|lobulated|thickened|septated|septation[s]?|fluid)',
    re.IGNORECASE)
    
    # capturing mass dimesnions
    dimensions_phrases = {r'\b\d+(\.\d+)?\s*x\s*\d+(\.\d+)?\s*x\s*\d+(\.\d+)?\s*cm\b', 
                          r'\b\d+(\.\d+)?\s*x\s*\d+(\.\d+)?\s*cm\b',
                          r'\b\d+(\.\d+)?\s*cm\b'}
                           
        
    # will contain the item to be return, dictionary in the format {"matched text": ["no dimensions", "not cystic"]}
    results = {}


    for phrase in phrases:
        mass_pattern = re.compile(phrase, re.IGNORECASE)
        
        for match in mass_pattern.finditer(search_text):
            match_text = match.group()
            results[match_text] = ["", ""]
            match_end_index = match.end()
            match_start_index = match.start()
            
            
            
            for dimensions in dimensions_phrases:
                dimension_pattern = re.compile(dimensions, re.IGNORECASE)
                # Search for the first dimension AFTER the mass phrase or immediately BEFORE
                # break the loop if any found, no dimenions if none found
                dimension_match = dimension_pattern.search(search_text[match_start_index - 20: match_end_index + 100])

                if dimension_match:
                    dimension_text = dimension_match.group()  # Extract the matched dimension
                    results[match_text][0] = dimension_text  # Store mass phrase with first found dimension
                    break
                else:
                    results[match_text][0] = "no dimensions"
                
            # Search for cystic features within or after the mass phrase
            cystic_match = cystic.search(search_text[match_start_index - 50:match_end_index + 100])
            
            if cystic_match:
                cystic_text = cystic_match.group()  # Extract the matched cyst phrase
                results[match_text][1] = cystic_text  # Store mass phrase with cyst phrase
            else:
                results[match_text][1] = "not cystic"
    return results

def solidmasscomplexcyst(text):
    """
    Interprets results of regex function.
    :param text: The input text to be searched and passed on to regex function.
    :return: 0 if no presence of solid mass or complex cyst, 1 if present.
    """
    if len(find_phrases(text)) == 0:
        return 0
    return 1
    
def any_cystic_mass(text):
    """
    Interprets results of regex function.
    :param text: The input text to be searched and passed on to regex function.
    :return: 0 if no cystic features present, 1 if present.
    """
    results = find_phrases(text) 
    cystic = 0
    if len(results) != 0:
        for result in results:
            if results[result][1] != 'not cystic':
                cystic = 1
    return cystic

# DECLARE INPUT FILES HERE:
# File Name: input_{today's date}.xls
# File should have features narrative_imp_combined, impression_fillednarrative, and segmented_narrative
df = pd.read_excel(f'input_{today_date}.xlsx')


# RE-Depdendent - Single Staged Approach
# Completed on narrative_imp_combined, a concatenated full-text narrative and impression
df['any_cystic_mass_re'] = df['narrative_imp_combined'].apply(any_cystic_mass)


# RE-Assisted - Two Staged Approach
# Completed first stage on impression_fillednarative, a targetted text most likely to have relevant data pointing to mass of interest
df['solidmasscomplexcyst_re_fs'] = df['impression_fillednarrative'].apply(solidmasscomplexcyst)
# Completed second stage on segmented narative, a targetted text most likely to have relevant data describing details of mass of interest
df['any_cystic_mass_re_ds'] = df.apply(
    lambda row: any_cystic_mass(row['segmented_narrative']) if row['solidmasscomplexcyst_re_fs'] == 1 else '',
    axis=1
)


# Output file
df.to_excel(f'output_cysticfeatures{today_date}.xlsx', index=False)