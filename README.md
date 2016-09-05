# clinical_trials_dataset_etl
These are the scripts i use for performing ETL on ClinicalTrials.gov dataset
clinical_trials_unzip_move.py ---> unzips the ClinicalTrials.gov zip file downloaded from the site and moves it to a folder it creates for the next step in the ETL process.
clinical_trials_functions.py ---> contains fucntions i use for Extraction, Transformation, Validation, Cleaning and then Loading to the destination relational database.
clinical_trials_insert.py ----> the main ETL process script.
