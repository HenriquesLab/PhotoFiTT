# PhotoFITT: Phototoxicity Fitness Time Trial

Python package to measure and assess the temporal footprint of phototoxicity.

# General description of the workflow
PhotoFITT was designed to quantitatively analyse the effect that light causes in the deviation of the cell division process. 
We developed its content to analyse the image data obtained from our experiments so we distinguish two big steps: 
1. **Identification of cells in mitosis.**
   Here we used StarDist to segment the cells in mitosis in our phase contrast videos but one could use a different approach.
   The next step is independent of this one. For StarDist we followed:
      1. Run `resize_data.py` script, section `READ NIKON FIELS, RESIZE AND SAVE` in `accessorial_scripts/data_readers`. 
         There you will find code for other microscopy format as well. We resized the data to optimise the performance of StarDist but it is independent of the quantification.
      2. We used ZeroCostDL4Mic together with Google Colab to train, test and infer new data with StarDist. 
      3. Download the segmentations for the next step.
3. **Numerical analysis of the data after cell mitosis.**
    Following the data structure explained below, one can reproduce the numerical analysis proposed in our work. 

From now on, we will focus in Step 2.

# Folder structure
- `photofitt`: folder containing the main functions of the package.
  - `utils`: image processing scripts for nornalisation, cell shape analysis, tracking or data importing and exporting.
  - `analysis`: functions to analyse the numerical data extracted from processed images.
  - `display`: functions to plot, compute mosaics or display the analysis.

- `accessorial/data_readers`: scripts to read stacks and concatenated files from Nikon, Zeiss or tiff files. The scripts also perform data up/downsampling. These are hard coded so please, read the comments along the scripts and comment the unnecessary steps. 
For example:
   - `nikon_files.py`: Examples of how to read ND2 files containing more than one stack. Has the scripts used to clean frames and concatenate videos for the final analysis. Same for zeiss (`zeiss_files.py`).
   - `resize_data.py`: Data has been resized before any analysis. It contains the script used to resize training and final data.
- `accessorial/analysis` and `accessorial/statistics`: scripts used for in-house development.
- `notebooks`: compiled notebooks used to train and do inference & guided Step 2 of the proposed workflow.
- `analysis`: scripts to run the analysis in a more programmatic fashion. Read the proposed workflow section bellow.
- `environments`: Different conda environment files to run the installation. Look at the Installation section bellow.

## Proposed workflow to analyse .nd2 videos

1. Classify the segmentations in folders (each folder for each condition to be analysed). 
   At some point we will also analyse the raw data so both, the masks and the raw input, should be equally organised.
   For example:
      ```
       -Raw-images (folder)
       |
       |--Biological-replica-date-1 (folder) [Subcaegory-00]
           |
           |--Cell density / UV Ligth / WL 475 light [Subcategory-01] 
              |
              |-- control-condition (folder) [Subcategory-02] 
              |    |  file1.tif
              |    |  file2.tif
              |    |  ...
              |
              |-- condition1 (folder) [Subcategory-02] 
              |    |  file1.tif
              |    |  file2.tif
              |    |  ...
              |
              |-- condition2 (folder) [Subcategory-02] 
              |    |  file1.tif
              |    |  file2.tif
              |    |  ...
           |
           |--Cell density / UV Ligth / WL 475 light [Subcategory-01]
           ...
       -Masks (folder)
       |
       |--Biological-replica-date-1 (folder) [Subcaegory-00]
           |
           |--Cell density / UV Ligth / WL 475 light [Subcategory-01] 
              |
              |-- control-condition (folder) [Subcategory-02] 
              |    |  file1.tif
              |    |  file2.tif
              |    |  ...
              |
              |-- condition1 (folder) [Subcategory-02] 
              |    |  file1.tif
              |    |  file2.tif
              |    |  ...
              |
              |-- condition2 (folder) [Subcategory-02] 
              |    |  file1.tif
              |    |  file2.tif
              |    |  ...
           |
           |--Cell density / UV Ligth / WL 475 light [Subcategory-01]
           ...
      ```
2. You can follow the steps in the notebooks:
   1. `Analyse phototoxicity data.ipnynb`: it analyses the information from the masks and plot it in graphs. It will also compute the temporal peaks for mitosis and plot it in a comparative manner.
   2. `Create mosaics with detections.ipynb`: it combines the masks and the input images to provide videos with mosaics in which one can easily see how the number of detected cells increases and how they look like.
   3. `Cell growth analysis.ipynb`: it uses the input images to compute the differences between consecutive frames and estimate the general dynamics present in the video (*e.g.*, the deviations in the cell growth after mitosis in our case).

3. Or use the scripts: 
   1. In `analysis/mitoses_counting` folder one can find the following:
      1. The scripts to count the number of identified cells in mitosis, calculate their size and plot the distributions upon time. It analyses full directories and stores the data with the corresponding conditions, dates and video names so all the results can be fully tracked (`analyse_all_masks.py`).
      ```
      python3 analyse_all_masks.py ../mitosis_mediated_data/masks/scaled_x8/stardist_prob03/ ../mitosis_mediated_data/results/scaled_x8/stardist_prob03 4
      ```
      2. Generate mosaics with detected rounded cells (*i.e.,* mitoses) (`create_mosaics.py`)
      ```
       python3 create_mosaics.py ../mitosis_mediated_data/masks/scaled_x8/stardist_prob03/2022-01-28 ../mitosis_mediated_data/input_data/2022-01-28/scaled_8 ../mitosis_mediated_data/results/scaled_x8/stardist_prob03/2022-01-28
      ```
      3. Compare the temporal peaks between groups and conditions (`display_mitosis_data.py`)
      ```
       python3 display_mitosis_data.py ../mitosis_mediated_data/results/scaled_x8/stardist_prob03/2022-01-28 mitosis_data
      ```
   2. In `analysis/dynamics` folder one can find the following:
      1. Extract the motility metrics from normalised videos. It analyses full directories and stores the data with the corresponding conditions, dates and video names so all the results can be fully tracked. It stores a csv file in the chosen output directory. (`extract_fov_motility.py`).
      ```
      python3 extract_fov_motility.py ../mitosis_mediated_data/input_data/2022-01-28/scaled_8 ../mitosis_mediated_data/results/scaled_x8/stardist_prob03 'WL UV - high'
      ```
      2. Analyse and display the motility metrics extracted with `extract_fov_motility` (`analyse_fov_dynamics_metrics.py`).
      
# Package installation

## Installation in M1
The code provides an `environment.yaml` file with most of the dependencies needed. As some dependencies might not be installed for all the operating system, we provide longer but still general enough guidelines.
- Download the file `environment_m1.yaml` from the `environments` folder.
- Create a new conda or mamba environment using `environment_m1.yaml`. All the packages will be installed from conda-forge.
  Place your terminal in the `photofitt` folder. Use either conda or mamba:
  ```
  mamba env create -f environment.yml  
  mamba activate photofitt
  ```
- The current code uses `connected-components-3d `, which is not available for osx-arm64 (MacOS M1). 
  Thus, we need to install it manually in the environment that we have just created.
- Place the terminal in the package folder of your environment (*e.g.*, `/Users/esti/mambaforge/envs/photofitt/lib/python3.9/site-packages`) and run the following
- 
  ```
  git clone https://github.com/seung-lab/connected-components-3d.git
  cd connected-components-3d
  pip install -r requirements.txt
  python setup.py develop
  ```
- **ONCE PUBLISHED** You can now install the package using pip install or conda as follows:
  
  - ```
    pip install photofitt
    ```
    or
  - 
    ```
    conda install photofitt
    ```
- **Meanwhile**:

  - ```
    git clone https://github.com/HenriquesLab/photofitt.git
    cd photofitt
    python setup.py
    ```
    or
  - ```
    git clone https://github.com/HenriquesLab/photofitt.git
    cd photofitt
    conda build conda-recipe/meta.yaml
    ```

## Common error messages
- Error messages with `lxml`. 
Most probably you need to update developers tools in your system. Before anything, run in Mac M1:
  - 
      ```
      xcode-select --install
      ```
- If you were in Linux, you can run 
  - ```
    sudo apt-get update
    sudo apt-get install libxml2-dev libxslt-dev python-dev
    ```
