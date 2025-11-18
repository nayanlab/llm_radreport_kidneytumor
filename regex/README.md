# Regular Expression (Regex) Feature Extraction

This folder contains a set of Python scripts for extracting structured features from radiology report text using regular expressions.

Given a sample input file (`10_sample_input.xlsx`), the pipeline:

1. Generates a standardized input file (`input.xlsx`) using `Generate_Features.py`.
2. Extracts specific features from `input.xlsx` using four independent scripts:
   - `solidmass_complexcyst.py`
   - `cysticfeatures.py`
   - `multifocal.py`
   - `dimension.py`

Each feature-extraction script can be run independently once `input.xls` has been created.

---

## Repository Structure

```text
.
├── Generate_Features.py
├── solidmass_complexcyst.py
├── cystic_features.py
├── multifocal.py
├── max_dimension.py
├── 10_sample_input.xls
└── README.md
```



## Requirements
- Python 3.9+
- Packages:
  - `pandas`
  - `re`
 
## Getting Started 
1. Download repository as ZIP
2. Unzip folder and open a terminal with that working directory

## Input File 
`10_sample_input.xlsx`

This file serves two purposes:
1. It shows the expected columns and formatting of your raw input.
2. It can be used to test the pipeline end-to-end.

`Generate_Features.py` can read in  `10_sample_input.xlsx` and create the file `input.xlsx` needed to run the 4 regex functions.


## Running the feature extraction scripts

Once the file `input.xlsx ` is generated, the remaining 4 .py files containing regex feature extractions can be run indepdently to extract the following features: 
  - `solidmass_complexcyst.py`: Creates output file `solidmass_complexcyst_output.xlsx`
    - reports a binary outcome indicating 1 if prescence of a solid mass or complex cyst of interest, 0 if not
   - `cysticfeatures.py`: Creates output file `cysticfeatures_output.xlsx`
     - reports a binary outcome indicating 1 if the mass has cystic features, 0 if not
   - `multifocal.py`: Creates output file `multifocal_output.xlsx`
     - reports a binary outcome indicating 1 if there are multiple renal masses, 0 if not
   - `dimension.py`: Creates output file `dimension_output.xlsx`
     - reports a continuous outcome reporting the dimensions of the mass identified


