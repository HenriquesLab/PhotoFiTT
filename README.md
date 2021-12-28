# mitosis-mediated-phototoxic
Python scripts to detect cell mitosis and assess phototoxicity by cell arrestment detection

## Description of the python scripts

- `analyse_segmentations.py`: Scripts to extract different curves with information about the number of mitosis. It will contain the main code of the analysis. 
- `create_mosaics.py`: Code to generate mosaics with detected rounded cells (*i.e.,* mitoses).
- `nikon_files.py`: Examples of how to read ND2 files containing more than one stack. Has the scripts used to clean frames and concatenate videos for the final analysis.
- `resize_data.py`: Data has been resized before any analysis. It contains the script used to resize training and final data.

- `utils`: folder with all the functions.
- `notebooks`: notebooks used to train and do inference.