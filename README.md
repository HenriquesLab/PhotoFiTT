[![License](https://img.shields.io/github/license/HenriquesLab/PhotoFiTT?color=Green)](https://github.com/HenriquesLab/PhotoFiTT/blob/main/LICENSE.txt)
[![Contributors](https://img.shields.io/github/contributors-anon/HenriquesLab/PhotoFiTT)](https://github.com/HenriquesLab/PhotoFiTT/graphs/contributors)
[![GitHub stars](https://img.shields.io/github/stars/HenriquesLab/PhotoFiTT?style=social)](https://github.com/HenriquesLab/PhotoFiTT/)
[![GitHub forks](https://img.shields.io/github/forks/HenriquesLab/PhotoFiTT?style=social)](https://github.com/HenriquesLab/PhotoFiTT/)


<img src="https://github.com/HenriquesLab/PhotoFiTT/blob/main/docs/logo/photofitt-logo.png" align="right" width="300"/>

# PhotoFiTT: Phototoxicity Fitness Time Trial
A Quantitative Framework for Assessing Phototoxicity in Live-Cell

# General description of the workflow
PhotoFiTT is designed to quantitatively analyse the impact of fluorescence light excitation on cell behavior during live-cell imaging. It focuses on three key measurements: (1) Identified mitotic cells, (2) Cell size dynamics, and (3) Cell activity.
To replicate our analysis, follow these steps: 
### Deep learning based analysis
Follow these steps to detect cells and mitotic rounding events in the data.
1. Cell Detection and Quantification (deep learning-based image analysis):
   - Virtual Staining: Use [ZeroCostDL4Mic](https://github.com/HenriquesLab/ZeroCostDL4Mic) / [DL4MicEverywhere](https://github.com/HenriquesLab/DL4MicEverywhere) Pix2Pix notebook to train a virtual staining model that infers cell nuclei. This analysis is applied only to the first frame of each video.
   - Nuclei Segmentation: Use ZeroCostDL4Mic/DL4MicEverywhere 2D StarDist notebook to apply the pretrained StarDist-versatile model to segment individual nuclei in the virtually stained images.
2. Mitotic Cell Identification (deep learning-based image analysis):
   - For Chinese Hamster Ovary (CHO) cells imaged with brightfield, you can use our trained StarDist model. If using other cell types or imaging conditions, manually annotate a representative image set and train a new StarDist model using the corresponding ZeroCostDL4Mic/DL4MicEverywhere notebooks.

### Image data analysis
1. Cell Size Analysis and Classification notebook: [`Analyse_mitotic_rounding.ipnynb`](https://github.com/HenriquesLab/PhotoFiTT/blob/main/notebooks/Analyse_mitotic_rounding.ipynb)
2. Quantification of Cellular Activity notebook: [`Analyse_cellactivity.ipnynb`](https://github.com/HenriquesLab/PhotoFiTT/blob/main/notebooks/Analyse_cellactivity.ipynb)
3. Quantification of manually tracked mitotic events in unsynchronised cell populations notebook: [`Analyse_unsynchronised_cells.ipnynb`](https://github.com/HenriquesLab/PhotoFiTT/blob/main/notebooks/Analyse_unsynchronised_cells.ipynb)

By following these steps, you can replicate our workflow and perform a detailed analysis of cell behavior under fluorescence light excitation.

### Example data
Two types of data are provided to test the notebooks:
- This dataset includes synchronised CHO cells and allows you to reproduce the plots and results from our study. You can skip calculating mitotic events or cell activity and section 1 of the notebooks when using these datasets.
   -  [Cell mitotic rounding](https://github.com/HenriquesLab/PhotoFiTT/releases/tag/v1.0.1#:~:text=data_activity_intensity.csv)
   -  [Cell activity](https://github.com/HenriquesLab/PhotoFiTT/releases/tag/v1.0.1#:~:text=normalised_mitosis_counting.csv)
- This dataset ([Download here](https://zenodo.org/records/12733476)) provides an example to start using the notebooks.
- The manual annotations used for our research study on unsynchronised populations are available on [Biorachive](https://www.ebi.ac.uk/biostudies/bioimages/studies/S-BIAD1269). Refer to the 'Manual tracking annotation of mitotic rounding in CHO unsynchronised cells - brightfield' section.

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
      
# Package installation
- To set up the environment and install the necessary dependencies, follow these steps:
## Clone the Repository and Set Up the Conda Environment:
- Open up the terminal and using mamba (if conda is preferred, change the code accordingly) paste the following:

  ```
  git clone https://github.com/HenriquesLab/photofitt.git
  cd photofitt
  mamba env create -f environment.yml  
  mamba activate photofitt
  ```
- The code provides an `environment.yaml` file to create a conda environment with all the required dependencies and places your terminal in the photofitt folder created by cloning our PhotofiTT repo.

## Install the package using pip install or conda as follows:
  - You can install the PhotoFiTT package using pip:
  - ```
    pip install photofitt
    ```

## Common error messages
- Error messages involving `lxml`. 
The most probable solution is to update the developers tools in your system. If you are running our code in Mac M1 copy this in the terminal:
  - 
      ```
      xcode-select --install
      ```
- If you are in Linux, copy this in the terminal instead: 
  - ```
    sudo apt-get update
    sudo apt-get install libxml2-dev libxslt-dev python-dev
    ```



