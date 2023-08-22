import pandas as pd
import os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# synchro data
synchro_data = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/CHO/results/scaled_1.5709_results/new_data/activity_clahe-intensity/data_activity_intensity.csv"
synchro_data = pd.read_csv(synchro_data)
# synchro_data["experiment"] = "SYNCHRO"
# synchro_data_control = synchro_data[synchro_data["Subcategory-02"] == 'Synchro']
# synchro_data_control = synchro_data_control.reset_index(drop=True)
wl568 = synchro_data[synchro_data["Subcategory-01"] == 'WL 568 - high density']
index = wl568.index.to_list()
synchro_data = synchro_data.drop(index)
synchro_data = synchro_data.reset_index(drop=True)

# REORGANISE
synchro_data_both = pd.concat(
    [synchro_data[synchro_data["Subcategory-02"] == 'Synchro'], synchro_data[synchro_data["Subcategory-02"] == 'Control-sync']])
index = synchro_data_both.index.to_list()
# remove control
synchro_data = synchro_data.drop(index)
# Add a new variable
synchro_data["Illumination"] = synchro_data["Subcategory-01"]
synchro_data_both["Illumination"] = synchro_data_both["Subcategory-02"]
# Concatenate
synchro_data = pd.concat([synchro_data, synchro_data_both])

#
# # Unsynchro data
# unsycnhro_data = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/CHO-UNSYNCH/activity_clahe-normalised-all-intensity/data_activity_intensity_unsynchro.csv"
# unsycnhro_data = pd.read_csv(unsycnhro_data)
# unsycnhro_data = unsycnhro_data[unsycnhro_data["Subcategory-02"] == 'control-00ms']
# unsycnhro_data = unsycnhro_data.reset_index(drop=True)
# unsycnhro_data["experiment"] = "UNSYNCHRO"
#
# unsycnhro_data = pd.concat(
#     [unsycnhro_data, synchro_data[synchro_data["Subcategory-02"] == 'Control-sync']]).reset_index(drop=True)

variables = ['mean activity', 'SUM activity',
             'area active cells', 'masked mean activity', 'total area active cells',
             'masked cumulative activity', 'TOTAL masked cumulative activity']

# for v in variables:
#     plt.figure()
#     sns.lineplot(data=unsycnhro_data, y=v, x="frame", style="Subcategory-01", hue="experiment")
#     plt.title(f"{v}")
#     plt.show()
#
# for v in variables:
#     plt.figure()
#     sns.lineplot(data=synchro_data_control, y=v, x="frame", hue="Subcategory-01", style="Subcategory-00")
#     plt.title(f"{v}")
#     plt.show()
#
# for v in variables:
#     plt.figure()
#     sns.lineplot(data=synchro_data_both, y=v, x="frame", style="Subcategory-02", hue="Subcategory-02")
#     plt.title(f"{v}")
#     plt.show()

hue_order = ['Control-sync', 'Synchro', 'WL 630 - high density', 'WL 475 - high density', 'WL UV - high density']
variables = ['masked mean activity',
             'masked cumulative activity']

for v in variables:
    fig = plt.figure()
    sns.lineplot(data=synchro_data, y=v, x="frame", hue="Illumination", hue_order=hue_order, errorbar="se",
                 palette=sns.color_palette("husl", 5))

    plt.title(f"{v} - standard deviation")
    fig.savefig(
        f"/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/CHO/results/scaled_1.5709_results/new_data/activity_clahe-intensity/manual/{v}.pdf",
        format="pdf", transparent=True)
    plt.show()

