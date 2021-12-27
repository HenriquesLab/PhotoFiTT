from utils.display import plot_smooth_curves
from utils.mitosis_counting import count_mitosis, smooth
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# Extract measures
# path = '/Volumes/OCB-All/Projects/OCB004_Phototoxicity/Analysis/StarDist/results'

min_roundness = [0.85, 0.9, 0.95, 0.97]
path = "/Users/esti/Documents/PHX/mitosis_mediated_data/results/2021-12-20/CHO_DIC_damage_merged_results"
# path = "/Users/esti/Documents/PHX/mitosis_mediated_data/results/2021-12-20/CHO_DIC_fast-acq_results"
for r in min_roundness:
    data = count_mitosis(path, stacks=True, frame_rate=2, min_roundness=r)
    # data['Subcategory-02'] = 'raw'
    t_win = 5
    videos = np.unique(data['Subcategory-01'])
    data1 = pd.DataFrame()
    for i in videos:
        video = data[data['Subcategory-01'] == i]
        video = video.sort_values('frame')
        video['Subcategory-02'] = 'Raw'
        # normalise
        M = np.max(video['mitosis'])
        video['mitosis_normalised'] = video['mitosis'] / M
        # smooth
        y = smooth(video['mitosis'], t_win)
        y_norm = smooth(video['mitosis_normalised'], t_win)
        # store smooth values
        video2 = video.copy()
        video2['Subcategory-02'] = 'Averaged'
        video2['mitosis'] = y
        video2['mitosis_normalised'] = y_norm
        video = pd.concat([video, video2]).reset_index(drop=True)
        data1 = pd.concat([data1, video]).reset_index(drop=True)

    # Display
    title = "Minimum roundness {}".format(r)
    y_var = "mitosis"
    output_path = path
    name = "mitosis_roundness-{}.png".format(r)
    plot_smooth_curves(data1, y_var, title, output_path, name)
    # Display
    title = "Minimum roundness {}".format(r)
    y_var = "mitosis_normalised"
    output_path = path
    name = "normalised_mitosis_roundness-{}.png".format(r)
    plot_smooth_curves(data1, y_var, title, output_path, name)


## Display roundness
data2 = data1[data1["Subcategory-02"] == "Raw"]
roundness_data = None
r = 0.8
for i in range(len(data2)):
    cell = data2.iloc[i]
    if cell.roundness_axis != []:
        RA = cell.roundness_axis
        RP = cell.roundness_projected
        t = cell.frame
        S0 = cell["Subcategory-00"]
        S1 = cell["Subcategory-01"]
        aux_data = [[t, RA[f], RP[f], S0, S1] for f in range(len(RA)) if RA[f] > r]
        col_names = ["frame", "roundness_axis", "roundness_projected", "Subcategory-00", "Subcategory-01"]
        aux = pd.DataFrame(aux_data, columns=col_names)

    if roundness_data is None:
        roundness_data = aux
    else:
        roundness_data = pd.concat([roundness_data, aux]).reset_index(drop=True)

fig = plt.figure()
plt.subplot(1, 2, 1)
sns.scatterplot(x="frame", y="roundness_axis", hue='Subcategory-00', data=roundness_data,
                linewidth=0, alpha=.5, palette="tab10")
plt.ylabel("Roundness")
plt.xlabel("Time (min)")
# plt.xlim([0,120])
# plt.ylim([0.7, 1])
#
plt.subplot(1, 2, 2)
sns.scatterplot(x="frame", y="roundness_projected", hue='Subcategory-00', data=roundness_data,
                linewidth=0, alpha=.5, palette="tab10")
plt.ylabel("Roundness")
plt.xlabel("Time (min)")
# plt.xlim([0,120])
# plt.ylim([0.7, 1])
fig.savefig(os.path.join(path, "roundness_scatterplot.png"), format='png')
plt.show()
