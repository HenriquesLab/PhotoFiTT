[![License](https://img.shields.io/github/license/HenriquesLab/PhotoFiTT?color=Green)](https://github.com/HenriquesLab/PhotoFiTT/blob/main/LICENSE.txt)
[![Contributors](https://img.shields.io/github/contributors-anon/HenriquesLab/PhotoFiTT)](https://github.com/HenriquesLab/PhotoFiTT/graphs/contributors)
[![GitHub stars](https://img.shields.io/github/stars/HenriquesLab/PhotoFiTT?style=social)](https://github.com/HenriquesLab/PhotoFiTT/)
[![GitHub forks](https://img.shields.io/github/forks/HenriquesLab/PhotoFiTT?style=social)](https://github.com/HenriquesLab/PhotoFiTT/)



# PhotoFiTT: Phototoxicity Fitness Time Trial

<img src="https://github.com/HenriquesLab/PhotoFiTT/blob/main/docs/logo/photofitt-logo.png" align="right" width="300"/>

### A Quantitative Framework for Assessing Phototoxicity in Live-Cell

PhotoFiTT is designed to quantitatively analyse the impact of fluorescence light excitation on cell behaviour during live-cell imaging. It focuses on three key measurements: (1) Identified mitotic cells, (2) Cell size dynamics, and (3) Cell activity.
To replicate our analysis, follow these steps: 

### Key Features
- **Deep Learning-Based Cell Analysis:** Leverage state-of-the-art deep learning models for accurate cell detection, segmentation, and mitotic event identification.
- **Mitotic Cell Identification:** Detect and quantify mitotic rounding events in live-cell imaging data.
- **Cell Size Dynamics:** Analyse changes in cell size over time to assess the impact of phototoxicity.
- **Cellular Activity Quantification:** Measure and compare cellular activity levels across different experimental conditions.
- **Unsynchronized Cell Analysis:** Quantify mitotic events in unsynchronised cell populations through manual tracking.

## Workflow Overview

### Deep learning-based analysis

#### 1. Cell Detection and Quantification:
- Use deep learning-based virtual staining and nuclei segmentation to identify individual cells with [ZeroCostDL4Mic](https://github.com/HenriquesLab/ZeroCostDL4Mic) / [DL4MicEverywhere](https://github.com/HenriquesLab/DL4MicEverywhere) Pix2Pix notebook. This analysis is applied only to the first frame of each video.
- Leverage pre-trained 2D StarDist models available in [ZeroCostDL4Mic](https://github.com/HenriquesLab/ZeroCostDL4Mic) / [DL4MicEverywhere](https://github.com/HenriquesLab/DL4MicEverywhere), or equivalent models trained for your specific cell type and imaging conditions to segment individual nuclei in the virtually stained images.

#### 2. Mitotic Cell Identification:
- Detect and quantify mitotic rounding events using deep learning-based models.
- For Chinese Hamster Ovary (CHO) cells imaged with brightfield, you can use our trained StarDist model.
- If using other cell types or imaging conditions, manually annotate a representative image set and train a new segmentation model (e.g., StarDist) using the corresponding [ZeroCostDL4Mic](https://github.com/HenriquesLab/ZeroCostDL4Mic) / [DL4MicEverywhere](https://github.com/HenriquesLab/DL4MicEverywhere) notebooks.

### Image Data Analysis
1. Cell Size Analysis and Classification notebook: [`Analyse_mitotic_rounding.ipnynb`](https://github.com/HenriquesLab/PhotoFiTT/blob/main/notebooks/Analyse_mitotic_rounding.ipynb)
   - **Example data 1:** CSV file with the results published in our preprint that allows reproducing the plots and results from our study for synchronised CHO cells. Find it in [Biorachive](https://www.ebi.ac.uk/biostudies/bioimages/studies/S-BIAD1269) - Study component *PhotoFiTT published results data - detected mitotic events and cell activity*. Name of the file: `normalised_mitosis_counting.csv`.  When using these datasets, you can skip calculating mitotic events (section 1 of the notebook).
   - **Example data 2:** Image data to start using the notebook from scratch. [Download here](https://zenodo.org/records/12733476) the zip files `mitotic_rounding_masks.zip`and `pix2pix_masks.zip`. 
2. Quantification of Cellular Activity notebook: [`Analyse_cellactivity.ipnynb`](https://github.com/HenriquesLab/PhotoFiTT/blob/main/notebooks/Analyse_cellactivity.ipynb)
   - **Example data 1:** CSV file with the results published in our preprint that allows reproducing the plots and results from our study for synchronised CHO cells. Find it in [Biorachive](https://www.ebi.ac.uk/biostudies/bioimages/studies/S-BIAD1269) - Study component *PhotoFiTT published results data - detected mitotic events and cell activity*. Name of the file: `data_activity_intensity.csv`. When using these datasets, you can skip calculating cell activity (section 1 of the notebook).
   - **Example data 2:** Image data to start using the notebook from scratch. [Download here](https://zenodo.org/records/12733476) the zip files `downsample_data.zip`. 
3. Quantification of manually tracked mitotic events in unsynchronised cell populations notebook: [`Analyse_unsynchronised_cells.ipnynb`](https://github.com/HenriquesLab/PhotoFiTT/blob/main/notebooks/Analyse_unsynchronised_cells.ipynb)
   - **Example dataset:** The manual annotations used for our research study on unsynchronised populations, available on [Biorachive](https://www.ebi.ac.uk/biostudies/bioimages/studies/S-BIAD1269) - Annotation *Manual tracking annotation of mitotic rounding in CHO unsynchronised cells - brightfield*.
By following these steps, you can replicate our workflow and perform a detailed analysis of cell behaviour under fluorescence light excitation.

## Installation

To set up the PhotoFiTT framework, follow these steps in the terminal:

#### 1. Clone the repository:
Open up the terminal and paste the following commands to clone the PhotoFiTT repository and using `mamba` (or `conda` if preferred) create a Python environment with all the required dependencies.
```
git clone https://github.com/HenriquesLab/PhotoFiTT.git
cd PhotoFiTT
```

#### 2. Create and Activate the Conda Environment:
Use `mamba` or `conda`, as preferred.
```
mamba env create -f environment.yml
mamba activate photofitt
```
#### 3. Install the PhotoFiTT Package:
 ```
 pip install photofitt
 ```
#### 4. Launch Jupyter Notebooks to start analysing your data:
```
jupyter notebook
```
This will open the Jupyter Notebook interface in your web browser. Navigate to the `notebooks` folder to access the provided analysis notebooks.


## Data structure

1. The masks and the raw input, should be equally organised by folders, each folder for each condition to be analysed in a hierarchical manner.
   For example:
      ```
       -Raw-images (folder)
       |
       |--Biological-replica-date-1 (folder) [Subcategory-00]
           |
           |--Cell density / UV Light / WL 475 light [Subcategory-01] 
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
           |--Cell density / UV Light / WL 475 light [Subcategory-01]
           ...
       -Masks (folder)
       |
       |--Biological-replica-date-1 (folder) [Subcategory-00]
           |
           |--Cell density / UV Light / WL 475 light [Subcategory-01] 
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
           |--Cell density / UV Light / WL 475 light [Subcategory-01]
           ...
      ```
The key aspects of this data structure are:
1. **Raw-images** and **Masks** are the two main folders containing the raw image data and the corresponding segmentation masks, respectively. Both need to be **.tif** files.
2. Within each main folder, there are subfolders for each biological replicate, denoted as **Biological-replica-date-1**, **Biological-replica-date-2**, etc. in the schema.
3. Each biological replicate folder contains subfolders for different experimental conditions, such as **Cell density / UV Light / WL 475 light**.
4. Inside the condition folders, there are further subfolders for each specific condition, like **control-condition**, **condition1**, **condition2**, etc.
5. The actual image files (`.tif`) and mask files (`.tif`) are stored in the lowest-level condition folders.
This hierarchical structure allows the PhotoFiTT framework to handle multiple experimental conditions and replicates in an organized manner. The notebooks and analysis scripts expect the data to be structured this way for proper processing and analysis.


## Troubleshooting

### Error messages involving `lxml` 

The most probable solution is to update the developers tools in your system.
- For Mac M1, run `xcode-select --install` in the terminal
      ```
- For Linux, run this in the terminal instead: 
    ```
    sudo apt-get update
    sudo apt-get install libxml2-dev libxslt-dev python-dev
    ```

### Jupyter notebooks open as blank pages
  - Copy the URL you get when executing `jupyter notebook` from your terminal into your web browser. This URL has a token to securely open the notebooks and generally looks like this:
`http://127.0.0.1:8888/tree?token=2323dba1e********************************************`

For any other issues or questions, please open an [issue](https://github.com/HenriquesLab/PhotoFiTT/issues). 
