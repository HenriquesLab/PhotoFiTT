import os
from photofitt.statistics import extract_gaussian_params
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

## LOAD THE DATA
output_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/CHO/results/scaled_1.5709_results/stardist_prob03/"
# output_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/HELA/results/scaled_1.5709_results/stardist_prob03/"
folder = "mitosis_mediated_analysis"
# folder = "mitosis-mediated-results"
data = pd.read_csv(
    os.path.join(output_path, folder, "data_clean.csv"))

## RETAIN ONLY THE RAW DATA AND NOT THE SMOOTH ONE
data = data[data["processing"] == "Raw"].reset_index(drop=True)

## RENAME THE 1000ms CATEGORY BY 01sec to avoid duplicity
aux = data[data["Subcategory-02"] == 'UV1000ms']
data.loc[aux.index.to_list(), ["Subcategory-02"]] = ['UV01sec']
conditions = ['Control-sync', 'Synchro', 'UV25ms', 'UV50ms', 'UV100ms', 'UV200ms', 'UV400ms', 'UV800ms', 'UV01sec',
              'UV05sec', 'UV10sec', 'UV15sec', 'UV20sec', 'UV25sec']

### PLOTS FOR THE PAPER (ONLY FEW CONDITIONS)
c = 'WL UV - high density'
output_path_plots = os.path.join(output_path, "PAPER-PLOTS", c)
os.makedirs(output_path_plots, exist_ok=True)
hue_order = ['Control-sync', 'Synchro', 'UV25ms', 'UV50ms', 'UV100ms', 'UV200ms', 'UV400ms', 'UV800ms', 'UV01sec',
             'UV05sec', 'UV10sec', 'UV15sec', 'UV20sec', 'UV25sec']
LEN_C = len(hue_order)
data_c = data[data["Subcategory-01"] == c].reset_index(drop=True)
non_conditions = ['UV25ms', 'UV50ms', 'UV100ms', 'UV200ms', 'UV400ms', 'UV800ms', 'UV01sec', 'UV10sec', 'UV15sec',
                  'UV20sec', 'UV25sec']
for c in non_conditions:
    aux = data_c[data_c["Subcategory-02"] == c]
    index = aux.index.to_list()
    data_c = data_c.drop(index)
data_c = data_c.reset_index(drop=True)

##
fig = plt.figure(figsize=(5, 8))
plt.rcParams.update({'font.size': 15})
sns.lineplot(x="frame", y="mitosis", hue="Subcategory-02", data=data_c,
             palette=sns.color_palette("husl", 14), legend=False,
             hue_order=hue_order, linewidth=1.5, alpha=1)
plt.tight_layout()
plt.xlabel("Time (minutes)")
plt.ylabel("Counts of rounded cells")
plt.show()

###
distribution_data = extract_gaussian_params(data_c, "cell_size")

fig = plt.figure(figsize=(5, 8))
plt.rcParams.update({'font.size': 15})
sns.lineplot(x="frame", y="average", hue="Subcategory-02", data=distribution_data,
             palette=sns.color_palette("husl", 14), legend=False,
             hue_order=hue_order, linewidth=1.5, alpha=1)
plt.tight_layout()
plt.xlabel("Time (minutes)")
plt.ylabel("Cell size (pixels)")
plt.title("{0} along time".format("mitosis"))
# fig.savefig(os.path.join(output_path_plots, "data_{}_counting.png".format("mitosis")), format='png',
#             transparent=True)
plt.show()

##
c = 'WL UV - high density'
folder = "dynamics_clahe"
dynamics_metrics = pd.read_csv(
    os.path.join(output_path, folder, "data_dynamics_intensity_{}.csv".format(c)))

aux = dynamics_metrics[dynamics_metrics["Subcategory-02"] == 'UV1000ms']
dynamics_metrics.loc[aux.index.to_list(), ["Subcategory-02"]] = ['UV01sec']
for c in non_conditions:
    aux = dynamics_metrics[dynamics_metrics["Subcategory-02"] == c]
    index = aux.index.to_list()
    dynamics_metrics = dynamics_metrics.drop(index)
dynamics_metrics = dynamics_metrics.reset_index(drop=True)

fig = plt.figure(figsize=(5, 8))
plt.rcParams.update({'font.size': 15})
sns.lineplot(x="frame", y="time_variance", hue="Subcategory-02", data=dynamics_metrics,
             palette=sns.color_palette("husl", 14), legend=False,
             hue_order=hue_order, linewidth=1.5, alpha=1)
plt.tight_layout()
plt.xlabel("Time (minutes)")
plt.ylabel("Cell shape dynamics")

plt.title("{0} along time".format("mitosis"))
plt.show()
