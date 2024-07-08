[![License](https://img.shields.io/github/license/HenriquesLab/PhotoFiTT?color=Green)](https://github.com/HenriquesLab/PhotoFiTT/blob/main/LICENSE.txt)
[![Contributors](https://img.shields.io/github/contributors-anon/HenriquesLab/PhotoFiTT)](https://github.com/HenriquesLab/PhotoFiTT/graphs/contributors)
[![GitHub stars](https://img.shields.io/github/stars/HenriquesLab/PhotoFiTT?style=social)](https://github.com/HenriquesLab/PhotoFiTT/)
[![GitHub forks](https://img.shields.io/github/forks/HenriquesLab/PhotoFiTT?style=social)](https://github.com/HenriquesLab/PhotoFiTT/)


<img src="https://github.com/HenriquesLab/PhotoFiTT/blob/main/docs/logo/photofitt-logo.png" align="right" width="200"/>

# PhotoFiTT: Phototoxicity Fitness Time Trial
A Quantitative Framework for Assessing Phototoxicity in Live-Cell

# General description of the workflow
PhotoFiTT was designed to quantitatively analyse the imapct that fluorescence light excitation has in the cell behaviour.
PhotoFiTT focuses on three different measurements: (1) Identified pre-mitotic cells, (2) Cell size dynamics and (3) Cell activity.
These are the steps to follow to replicate the analysis: 
### Deep learning based analysis
Follow these steps to detect cell and pre-mitotic rounding events in the data.
1. Cell Detection and Quantification (deep learning-based image analysis: This processing is only applied to the first time point of each video.
   - Virtual Staining: Use ZeroCostDL4Mic/DL4MicEverywhere Pix2Pix notebook to train a virtual staining model that infers cell nuclei. Analyse the first frame of each video.
   - Nuclei Segmentation: Use ZeroCostDL4Mic/DL4MicEverywhere 2D StarDist notebook to apply the pretrained StarDist-versatile model to segment individual nuclei in the virtually stained images.
   - Initial Cell Quantification: Count the number of detected nuclei (Use notebook `XXXXX.ipnynb` to generate a CSV file with the counts). The number of detected nuclei serves as the baseline cell count for each field of view, enabling tracking of population dynamics over time.
2. Pre-mitotic Cell Identification (deep learning-based image analysis):
   - For CHO cells imaged with brightfield, you can use our trained StarDist model. Otherwise, manually annotate a representative image set and train a new StarDist model using the corresponding ZeroCostDL4Mic/DL4MicEverywhere notebooks.
### Image data Analysis
1. Cell Size Analysis and Classification `XXXXX.ipnynb`
2. Quantification of Cellular Activity `XXXXX.ipnynb`



## Data structure

1. The masks and the raw input, should be equally organised by folders, each folder for each condition to be analysed in a hierarchical manner.
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
      
# Package installation
- The code provides an `environment.yaml` file top ceeate a conda environment with all the dependencies needed.
  Place your terminal in the `photofitt` folder. Use either conda or mamba:
  ```
  git clone https://github.com/HenriquesLab/photofitt.git
  cd photofitt
  mamba env create -f environment.yml  
  mamba activate photofitt
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
    pip install .
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



