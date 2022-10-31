# PhotoPrint: Assessent of mitosis-mediated phototoxicity temporal footprint

Python scripts to detect cell mitosis, measure cell arrestment and assess the temporal hallmarks of phototoxicity.

## Proposed workflow to analyse .nd2 videos
1. Run `resize_data.py` script, section `READ NIKON FIELS, RESIZE AND SAVE`.
2. Upload the new stacks to google drive and run the StarDist notebook for inference. 
3. Download the segmentations.
4. Classify the segmentations in folders (each folder for each condition to be analysed). For example:
   ```
   Biological-replica-date-1
   |
   |-- Control-sync
   |    |  file1.tif
   |    |  file2.tif
   |    |  ...
   |
   |-- UV10sec
   |    |  file1.tif
   |    |  file2.tif
   |    |  ...
   |
   |-- Synchro
   |    |  file1.tif
   |    |  file2.tif
   |    |  ...
   ```
5. Run `analyse_segmentations.py`, `create_mosaics.py` and `temporal_distributions.py`. 
   1. Example for `analyse_segmentations.py`: It will take the conditions from the dataset (2022-01-26) and it will create a folder `2022-01-26` in which everything will be saved.
      ```
      cd mitosis-mediated-phototoxic
      python3 analyse_segmentations.py ../mitosis_mediated_data/masks/scaled_x8/stardist_prob03/2022-01-26 ../mitosis_mediated_data/results/scaled_x8/stardist_prob03/2022-01-26
      ```
   2. Example for `create_mosaics.py`:
      ```
       python3 create_mosaics.py ../mitosis_mediated_data/masks/scaled_x8/stardist_prob03/2022-01-28 ../mitosis_mediated_data/input_data/2022-01-28/scaled_8 ../mitosis_mediated_data/results/scaled_x8/stardist_prob03/2022-01-28
      ```
   3. Example for `temporal_distributions.py`. :
      ```
      python3 temporal_distributions.py ../mitosis_mediated_data/masks/scaled_x8/stardist_prob03/2022-01-26 ../mitosis_mediated_data/results/scaled_x8/stardist_prob03
      ```
## Description of the content

- `analyse_segmentations.py`: Scripts to extract different curves with information about the number of mitosis. It will contain the main code of the analysis. 
- `create_mosaics.py`: Code to generate mosaics with detected rounded cells (*i.e.,* mitoses).
- `temporal_distributions.py`: Displays the distribution of a specific measure (cell size) at each time point. It also plots the average values as a time-dependent function. 

### Folder structure
- `utils`: folder with all the functions.
- `data_readers`: scripts to read stacks and concatenated files from Nikon, Zeiss or tiff files. The scripts also perform data up/downsampling. These are hard coded so please, read the comments along the scripts and comment the unnecessary steps. 
For example:
   - `nikon_files.py`: Examples of how to read ND2 files containing more than one stack. Has the scripts used to clean frames and concatenate videos for the final analysis.
   - `resize_data.py`: Data has been resized before any analysis. It contains the script used to resize training and final data.

- `notebooks`: notebooks used to train and do inference.


# Package installation

The code provides an `environment.yaml` file with most of the dependencies needed. As some dependencies might not be installed for all the operating system, we provide longer but still general enough guidelines.

- Create a new environment using `environment.yaml`. All the packages will be installed from conda-forge.
  Place your terminal in the `mitosis-mediated-phototoxic` folder. Use either conda or mamba:
  ```
  mamba env create -n mitphoto -f environment.yml  
  mamba activate mitphoto
  ```
- The current code uses `connected-components-3d `, which is not available for osx-arm64 (MacOS M1). 
  Thus, we need to install it manually in the environment that we have just created.
  ```
  git clone https://github.com/seung-lab/connected-components-3d.git
  pip install -r requirements.txt
  python setup.py develop
  
  ```
- Similar to `slideio`, which is not existing for MacOS M1. Check out their documentation for your OS: https://pypi.org/project/slideio/