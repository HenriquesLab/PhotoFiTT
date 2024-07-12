[![License](https://img.shields.io/github/license/HenriquesLab/PhotoFiTT?color=Green)](https://github.com/HenriquesLab/PhotoFiTT/blob/main/LICENSE.txt)
[![Contributors](https://img.shields.io/github/contributors-anon/HenriquesLab/PhotoFiTT)](https://github.com/HenriquesLab/PhotoFiTT/graphs/contributors)
[![GitHub stars](https://img.shields.io/github/stars/HenriquesLab/PhotoFiTT?style=social)](https://github.com/HenriquesLab/PhotoFiTT/)
[![GitHub forks](https://img.shields.io/github/forks/HenriquesLab/PhotoFiTT?style=social)](https://github.com/HenriquesLab/PhotoFiTT/)


<img src="https://github.com/HenriquesLab/PhotoFiTT/blob/main/docs/logo/photofitt-logo.png" align="right" width="300"/>

# PhotoFiTT: Phototoxicity Fitness Time Trial
A Quantitative Framework for Assessing Phototoxicity in Live-Cell

# General description of the workflow
PhotoFiTT was designed to quantitatively analyse the impact that fluorescence light excitation has in cell behaviour.
PhotoFiTT focuses on three different measurements: (1) Identified pre-mitotic cells, (2) Cell size dynamics and (3) Cell activity.
These are the steps to follow to replicate the analysis: 
### Deep learning based analysis
Follow these steps to detect cells and pre-mitotic rounding events in the data.
1. Cell Detection and Quantification (deep learning-based image analysis: This processing is only applied to the first time point of each video.
   - Virtual Staining: Use [ZeroCostDL4Mic](https://github.com/HenriquesLab/ZeroCostDL4Mic) / [DL4MicEverywhere](https://github.com/HenriquesLab/DL4MicEverywhere) Pix2Pix notebook to train a virtual staining model that infers cell nuclei. Analyse the first frame of each video.
   - Nuclei Segmentation: Use ZeroCostDL4Mic/DL4MicEverywhere 2D StarDist notebook to apply the pretrained StarDist-versatile model to segment individual nuclei in the virtually stained images.
2. Pre-mitotic Cell Identification (deep learning-based image analysis):
   - For CHO cells imaged with brightfield, you can use our trained StarDist model. Otherwise, manually annotate a representative image set and train a new StarDist model using the corresponding ZeroCostDL4Mic/DL4MicEverywhere notebooks.

### Image data analysis
1. Cell Size Analysis and Classification notebook: [`Analyse_premitotic_rounding.ipnynb`](https://github.com/HenriquesLab/PhotoFiTT/blob/main/notebooks/Analyse_premitotic_rounding.ipynb)
2. Quantification of Cellular Activity notebook: [`Analyse_cellactivity.ipnynb`](https://github.com/HenriquesLab/PhotoFiTT/blob/main/notebooks/Analyse_cellactivity.ipynb)
3. Quantification of manually tracked mitotic events in unsynchronised cell populations notebook: [`Analyse_unsynchronised_cells.ipnynb`](https://github.com/HenriquesLab/PhotoFiTT/blob/main/notebooks/Analyse_unsynchronised_cells.ipynb)

### Example data
Two types of data is provided to test the notebooks:
- Data to reproduce the plots and results from our study with synchronised cells. When using this, one could skip calculating the mitotic events or cell activity and skip section 1 of the notebooks.
   -  [Cell pre-mitotic rounding](https://github.com/HenriquesLab/PhotoFiTT/releases/tag/v1.0.1#:~:text=data_activity_intensity.csv)
   -  [Cell activity](https://github.com/HenriquesLab/PhotoFiTT/releases/tag/v1.0.1#:~:text=normalised_mitosis_counting.csv)
- Example data to start using the notebooks for synchronised populations. (TODO Zenodo link)
- The manual annotations of unsynchronised populations used for our research study.

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
- The code provides an `environment.yaml` file to create a conda environment with all the dependencies needed.
  Place your terminal in the `photofitt` folder. Use either conda or mamba:
  ```
  git clone https://github.com/HenriquesLab/photofitt.git
  cd photofitt
  mamba env create -f environment.yml  
  mamba activate photofitt
  ```

- Install the package using pip install or conda as follows:
  
  - ```
    pip install photofitt
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



