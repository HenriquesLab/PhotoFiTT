# mitosis-mediated-phototoxic
Python scripts to detect cell mitosis and assess phototoxicity by arrested cell detection

## Description of the python scripts

- `analyse_segmentations.py`: Scripts to extract different curves with information about the number of mitosis. It will contain the main code of the analysis. 
- `create_mosaics.py`: Code to generate mosaics with detected rounded cells (*i.e.,* mitoses).
- `nikon_files.py`: Examples of how to read ND2 files containing more than one stack. Has the scripts used to clean frames and concatenate videos for the final analysis.
- `resize_data.py`: Data has been resized before any analysis. It contains the script used to resize training and final data.
- `temporal_distributions.py`: Displays the distribution of a specific measure (cell size) at each time point. It also plots the average values as a time-dependent function. 

- `utils`: folder with all the functions.
- `notebooks`: notebooks used to train and do inference.

## Proposed workflow to analyse .nd2 videos
1. Run `resize_data.py` script, section `READ NIKON FIELS, RESIZE AND SAVE`.
2. Upload the new stacks to google drive and run the StarDist notebook for inference. 
3. Download the segmentations.
4. Classify the segmentations in folders (each folder for each condition to be analysed).
5. Run `analyse_segmentations.py`, `create_mosaics.py` and `temporal_distributions.py`.

Each of the previous python scripts can be run in the terminal by typing:
```
python3 analyse_segmentations.py \input\to\your\segementations
```