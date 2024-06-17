"""
Created on 2021
Henriques Lab

This script is meant to run automatically. Results are stored as csv files with the corresponding conditions, dates and
video names so all the results can be fully tracked.
"""
import os
import numpy as np
import pandas as pd
import photofitt
from photofitt.analysis import count_mitosis_all, quantify_peaks, compare_peaks#, total_cell_number, add_inferred_nuclei
from photofitt import display
from photofitt.analysis import extract_gaussian_params
from photofitt.utils import power_conversion, numerical_dose
import seaborn as sns
import sys
import matplotlib.pyplot as plt

masks_path = "/home/ocb/HardDrive_4TB/EGM/PHX/DATA/MASKS/HELA-SYNCHRO/scaled_1.5709_results/stardist_prob03"
frame_rate = 4 # The time gap we will use to compute all the metrics
output_path =  "/home/ocb/HardDrive_4TB/EGM/PHX/ANALYSIS/HELA-SYNCHRO/NEW"
pis2pix_data = "/media/ocb/OCB-Data2/PhotoFiTT/PIX2PIX/SINGLE_FRAMES/STARDIST/HELA-SYNCHRO/"


# Create folders
os.makedirs(output_path, exist_ok=True)
os.makedirs(os.path.join(output_path, "plots"), exist_ok=True)

# Count mitoses
data = count_mitosis_all(masks_path, frame_rate = frame_rate)
# save the information
data.to_csv(os.path.join(output_path, "mitosis_counting.csv"))

# Calculate numbers from pix2pix
sys.path.append("/home/ocb/HardDrive_4TB/EGM/PHX/PhotoFITT/photofitt/analysis/")
from mitosis_counting import total_cell_number,add_inferred_nuclei
cell_number = total_cell_number(pis2pix_data, type="image")
cell_number.to_csv(os.path.join(output_path, "cell_counting_pix2pix.csv"))

# Merge data
updated_data = add_inferred_nuclei(data, cell_number)
updated_data["Cell percentage"] = updated_data["Number of cells"] / updated_data['cell_counts_stardist']
# Remove anny potential frame that was not well segmented
data_filtered = updated_data.loc[lambda updated_data: updated_data["Cell percentage"] <= 1]
data_filtered.to_csv(os.path.join(output_path, "normalised_mitosis_counting_pix2pix.csv"))

# Estimate the ligth dose
light_power = 6.255662 # fixed power value according to our microscope
data = photofitt.utils.numerical_dose(data_filtered, column_name="Subcategory-02", power=light_power)
data = power_conversion(data, dose_column="Light dose", condition_col="Subcategory-02", condition_name="Synchro")
data.to_csv(os.path.join(output_path, "normalised_mitosis_counting_pix2pix.csv"))
del updated_data, data_filtered, cell_number




## PLOT THE CURVES OF MITOSIS COUNTS
hue_order = ['non-synchro-0 J/cm2', '0 J/cm2', '0.2 J/cm2',
             '0.3 J/cm2', '0.6 J/cm2', '1.3 J/cm2', '2.5 J/cm2',
             '5.0 J/cm2', '6.3 J/cm2', '31.3 J/cm2', 
             '62.6 J/cm2', '93.8 J/cm2', '125.1 J/cm2', '156.4 J/cm2', '187.7 J/cm2']
## There is raw and smooth data. We show the smooth data (with a moving average of kernel 5) for the plots.
groups = np.unique(data["Subcategory-01"])
smoothing = np.unique(data["processing"])
## Name of the variable to display in the plot.
plot_y_var = "Cell percentage" #  "Percentage" # "Norm. Number of cells"
fig_format = ["png", "pdf"]
for g in groups:
    ploting_data_g = data[data["Subcategory-01"]==g].reset_index(drop=True)  
    for s in smoothing:
        # sns.set_style()
        ploting_data = ploting_data_g[ploting_data_g["processing"]==s].reset_index(drop=True)    
        title = f"{g}"
        condition = "Light dose cat" # "Subcategory-02"
        #hue_order = ['Control-sync', 'Synchro', '25ms', '50ms', '100ms', '200ms', '400ms', '800ms',
                     #'01sec', '05sec', '10sec', '15sec', '20sec', '25sec']
        for f in fig_format:
            name = "{0}_{1}_{2}.{3}".format(g, plot_y_var, s, f)
            display.conditions(ploting_data, plot_y_var, title, condition, os.path.join(output_path, "plots"), name,
                            hue_order=hue_order, palette=sns.color_palette("CMRmap_r", 17))

wl = np.unique(data["Subcategory-01"])
fig_format = ["png", "pdf"]
for w in wl:
    data_w = data.loc[lambda data: data["Subcategory-01"]==w]
    for s in smoothing:
        ploting_data = data_w[data_w["processing"]==s].reset_index(drop=True)   
        for f in fig_format:
            name = "{0}_{1}_{2}.{3}".format(w, plot_y_var, s, f) # name we want to give to the plot
            new_name="cells_vertical_subplots_{}".format(name)
        
            display.vertical_distributions(ploting_data, plot_y_var, os.path.join(output_path, "plots"), 
                                           new_name, 
                                           ylabel="Cells",
                                           raw="Light dose cat",
                                           hue="Light dose cat", 
                                           hue_order=hue_order, 
                                           palette=sns.color_palette("CMRmap_r", 17))

## PLOT RELATIVE CHANGES WITH RESPECT TO CONTROL
# We still use the data calculated in 1. We use the smooth data this time, but one could used the raw data.
data = data.loc[lambda data: data["processing"]=='Averaged-kernel5']
plot_y_var = "Cell percentage"
data_peaks = quantify_peaks(data, plot_y_var)

# Show each distribution with both violins and points
# Rename the columns to get the proper naming in the plots
data_peaks = data_peaks.rename(columns={'peak_time': 'Peak time point (min)', 
                            'delay_synchro': 'Delay w.r.t. synchronised cells (min)',
                           'proportional_delay_synchro': 'Proportional delay w.r.t. synchronised cells'})

x_var = ["Peak time point (min)", "Delay w.r.t. synchronised cells (min)",
         "Proportional delay w.r.t. synchronised cells", "Resistant cell decrease",
         "Proportional resistant decrease"]

reduce_order = ['non-synchro-0 J/cm2', '0 J/cm2', '0.2 J/cm2',
             '0.3 J/cm2', '0.6 J/cm2', '1.3 J/cm2', '2.5 J/cm2',
             '5.0 J/cm2']
wl_order = ['WL UV - high density', 'WL 475 - high density', 'WL 568 - high density', 'WL 630 - high density']
# Estimate the ligth dose
light_power = 6.255662 # fixed power value according to our microscope
data_peaks = photofitt.utils.numerical_dose(data_peaks, column_name="Subcategory-02", power=light_power)
data_peaks = power_conversion(data_peaks, dose_column="Light dose", condition_col="Subcategory-02", condition_name="Synchro")

fig_format = ["png", "pdf"]
wl = np.unique(data_peaks["Subcategory-01"])

fig_format = ["png", "pdf"]
for x in x_var:
    for f in fig_format:
        for w in wl:
            data_peaks_w = data_peaks.loc[lambda data_peaks: data_peaks["Subcategory-01"]==w]
            name = f"{w}_{x}.{f}"# name we want to give to the plot
            new_name = f"peaktime_violin_horizontal_exposure_time{name}"
            display.violinplots_horizontal(data_peaks_w,'Light dose cat', x,
                                           os.path.join(output_path, "plots"),
                                           new_name, hue_order,
                                           palette=sns.color_palette("CMRmap_r", 17),
                                           ylabel=f"{w}_{x}")
            ## Bar plots
            name = f"{w}_{x}.{f}"# name we want to give to the plot
            new_name = f"barplot_{name}"
            fig = plt.figure(figsize=(7,5))
            g = sns.barplot(data_peaks_w, x='Light dose cat', y=x,
                        palette=sns.color_palette("CMRmap_r", 17),
                        errorbar=("ci", 95),  capsize=.1,
                        order=reduce_order)
            plt.setp(g.get_xticklabels(), rotation=30)
            plt.tight_layout()
            fig.savefig(os.path.join(output_path, "plots", new_name), format=f, transparent=True)
            plt.show()
        
        # Plot all barplots together
        name = f"{x}.{f}"# name we want to give to the plot
        new_name = f"barplot_all_{name}"
        
        fig = plt.figure()
        g = sns.catplot(
            data_peaks, kind="bar",
            x='Light dose cat', y=x,
            col="Subcategory-01",
            palette=sns.color_palette("CMRmap_r", 17),
            height=3, aspect=1, 
            order=reduce_order, 
            errorbar=("ci", 95),  capsize=.1,
            col_order=wl_order
        )
        plt.tight_layout()
        g.set_xticklabels(rotation=45)
        g.set_titles("{col_name}")
        g.savefig(os.path.join(output_path, "plots", new_name), format=f, transparent=True)
        plt.show()
