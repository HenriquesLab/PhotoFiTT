"""
Created on 2022
Henriques Lab

This scripts extracts analyses the motility metrics extracted with `extract_fov_motility`.

The script is not meant to run automatically. It has sections to clean the data or concatenate it.
"""
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

output_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/results/scaled_1.5709_results/stardist_prob03"
folder = "dynamics_clahe"
#
# # EXAMPLE OF HOW TO CLEAN DATA
# # ---------------------------------------
# dynamics_metrics = pd.read_csv(os.path.join(output_path, folder, "data_dynamics_intensity_475.csv"))
# print(len(dynamics_metrics))
# dynamics_metrics_data = dynamics_metrics[dynamics_metrics['Subcategory-00']=="2022-09-07-night"]
#
# dynamics_metrics_video = dynamics_metrics_data[dynamics_metrics_data['video_name']=="CHO_night_475_live-01-Scene-39-P5-A04"]
# index = dynamics_metrics_video.index.to_list()
# dynamics_metrics = dynamics_metrics.drop(index)
#
# dynamics_metrics_video = dynamics_metrics_data[dynamics_metrics_data['video_name']=="CHO_night_475_live-01-Scene-38-P6-A04"]
# index = dynamics_metrics_video.index.to_list()
# dynamics_metrics = dynamics_metrics.drop(index)
#
# dynamics_metrics_video = dynamics_metrics_data[dynamics_metrics_data['video_name']=="CHO_night_475_live-01-Scene-53-P4-B03"]
# index = dynamics_metrics_video.index.to_list()
# dynamics_metrics = dynamics_metrics.drop(index)
#
# dynamics_metrics_video = dynamics_metrics_data[dynamics_metrics_data['video_name']=="CHO_night_475_live-01-Scene-70-P10-B02"]
# index = dynamics_metrics_video.index.to_list()
# dynamics_metrics = dynamics_metrics.drop(index)
#
# dynamics_metrics_video = dynamics_metrics_data[dynamics_metrics_data['video_name']=="CHO_night_475_live-01-Scene-41-P2-B04"]
# index = dynamics_metrics_video.index.to_list()
# dynamics_metrics = dynamics_metrics.drop(index)
#
# dynamics_metrics_video = dynamics_metrics_data[dynamics_metrics_data['video_name']=="CHO_night_475_live-01-Scene-42-P3-B04"]
# index = dynamics_metrics_video.index.to_list()
# dynamics_metrics = dynamics_metrics.drop(index)
#
# dynamics_metrics_video = dynamics_metrics_data[dynamics_metrics_data['video_name']=="CHO_night_475_live-01-Scene-44-P1-B04"]
# index = dynamics_metrics_video.index.to_list()
# dynamics_metrics = dynamics_metrics.drop(index)
#
# dynamics_metrics_video = dynamics_metrics_data[dynamics_metrics_data['video_name']=="CHO_night_475_live-01-Scene-45-P9-B04"]
# index = dynamics_metrics_video.index.to_list()
# dynamics_metrics = dynamics_metrics.drop(index)
#
# dynamics_metrics_video = dynamics_metrics_data[dynamics_metrics_data['video_name']=="CHO_night_475_live-01-Scene-46-P4-B04"]
# index = dynamics_metrics_video.index.to_list()
# dynamics_metrics = dynamics_metrics.drop(index)
#
# dynamics_metrics_video = dynamics_metrics_data[dynamics_metrics_data['video_name']=="CHO_night_475_live-01-Scene-47-P8-B04"]
# index = dynamics_metrics_video.index.to_list()
# dynamics_metrics = dynamics_metrics.drop(index)
#
# dynamics_metrics_video = dynamics_metrics_data[dynamics_metrics_data['video_name']=="CHO_night_475_live-01-Scene-48-P5-B04"]
# index = dynamics_metrics_video.index.to_list()
# dynamics_metrics = dynamics_metrics.drop(index)
#
# dynamics_metrics_video = dynamics_metrics_data[dynamics_metrics_data['video_name']=="CHO_night_475_live-01-Scene-49-P6-B04"]
# index = dynamics_metrics_video.index.to_list()
# dynamics_metrics = dynamics_metrics.drop(index)
#
# dynamics_metrics = dynamics_metrics.reset_index(drop=True)
# print(len(dynamics_metrics))
# dynamics_metrics.to_csv(os.path.join(output_path, folder, "data_dynamics_intensity_475_clean.csv"))


dynamics_metrics = dynamics_metrics.drop(index)
dynamics_metrics = dynamics_metrics.reset_index(drop=True)
print(len(dynamics_metrics))
dynamics_metrics.to_csv(os.path.join(output_path, folder, "data_dynamics_intensity_475_clean.csv"))

aux = None
for v in np.unique(dynamics_metrics["video_name"]):
    video_data = dynamics_metrics[dynamics_metrics["video_name"]==v]
    frame_rate = 4
    init_mit = int(30/frame_rate)
    final_mit = int(80/frame_rate)
    alpha = np.max(video_data.iloc[init_mit:final_mit]["time_variance"])
    init_mit = int(250 / frame_rate)
    final_mit = int(300 / frame_rate)
    beta = np.mean(video_data.iloc[init_mit:]["time_variance"])
    columns = [c for c in video_data.columns if c.__contains__("Subcategory")]
    data = [video_data.iloc[0][c] for c in columns]
    if alpha == 0. and beta == 0.:
        ratio = 0.
    elif beta == 0.:
        print(v)
        ratio = np.infty
    else:
        ratio = alpha/beta
    #ratio = (alpha - beta) / (alpha + beta)
    data += [v, alpha, beta, ratio]
    columns += ["video_name", "alpha", "beta", "ratio"]

    if aux is None:
        aux = pd.DataFrame(np.expand_dims(np.array(data), axis=0), columns=columns)
    else:
        aux = pd.concat([aux,
                         pd.DataFrame(np.expand_dims(np.array(data), axis=0), columns=columns)]).reset_index(drop=True)
aux = aux.astype({'ratio': 'float32', 'alpha': 'float32', 'beta': 'float32'})
# plt.figure()
# sns.set_theme(style="whitegrid")
# # Draw a nested barplot by species and sex
# conditions = ['Control-sync', 'Synchro', 'UV50ms', 'UV100ms', 'UV200ms', 'UV400ms', 'UV800ms', 'UV1000ms', 'UV01sec',
#                     'UV05sec', 'UV10sec', 'UV15sec', 'UV20sec', 'UV25ms', 'UV25sec']
# g = sns.catplot(
#     data=aux, kind="violin", x="Subcategory-02", y="ratio", hue="Subcategory-01", order=conditions,
#     palette="dark", alpha=.6, height=6
# )
# g.despine(left=True)
# g.set_axis_labels("", "motility")
# plt.yscale("log")
# plt.show()

### points
plt.figure()
# conditions = ['Control-sync', 'Synchro', 'UV50ms', 'UV100ms', 'UV200ms', 'UV400ms', 'UV800ms', 'UV1000ms']
conditions = ['Control-sync', 'Synchro', 'UV50ms', 'UV100ms', 'UV200ms', 'UV400ms', 'UV800ms', 'UV1000ms', 'UV01sec',
                    'UV05sec', 'UV10sec', 'UV15sec', 'UV20sec', 'UV25ms', 'UV25sec']
ax = sns.swarmplot(data=aux, x="Subcategory-02", y="ratio", hue="Subcategory-02", order=conditions, palette="dark")
# plt.ylim([0,10])
plt.yscale("log")
plt.show()

### POINTS
# conditions = ['Control-sync', 'Synchro', 'UV50ms', 'UV100ms', 'UV200ms', 'UV400ms', 'UV800ms', 'UV1000ms']
conditions = ['Control-sync', 'Synchro', 'UV50ms', 'UV100ms', 'UV200ms', 'UV400ms', 'UV800ms', 'UV1000ms', 'UV01sec',
                    'UV05sec', 'UV10sec', 'UV15sec', 'UV20sec', 'UV25ms', 'UV25sec']
g = sns.catplot(data=aux, x="Subcategory-02", y="ratio", hue="Subcategory-00", order=conditions, height=5, aspect=2,)
# g.set_axis_labels("", "Survival Rate")
# g.set_xticklabels()
g.despine(left=True)
# plt.ylim([0,10])
plt.yscale("log")
plt.show()

### BARS
# conditions = ['Control-sync', 'Synchro', 'UV50ms', 'UV100ms', 'UV200ms', 'UV400ms', 'UV800ms', 'UV1000ms']
conditions = ['Control-sync', 'Synchro', 'UV50ms', 'UV100ms', 'UV200ms', 'UV400ms', 'UV800ms', 'UV1000ms', 'UV01sec',
                    'UV05sec', 'UV10sec', 'UV15sec', 'UV20sec', 'UV25ms', 'UV25sec']
g = sns.catplot(
    data=aux, x="Subcategory-02", y="ratio", hue="Subcategory-00", order=conditions,kind="bar",
   height=5, aspect=2,
)
# g.set_axis_labels("", "Survival Rate")
# g.set_xticklabels()
g.despine(left=True)
# plt.ylim([0,10])
plt.yscale("log")
plt.show()

### BARS COLUMNS
# conditions = ['Control-sync', 'Synchro', 'UV50ms', 'UV100ms', 'UV200ms', 'UV400ms', 'UV800ms', 'UV1000ms']
conditions = ['Control-sync', 'Synchro', 'UV50ms', 'UV100ms', 'UV200ms', 'UV400ms', 'UV800ms', 'UV1000ms', 'UV01sec',
                    'UV05sec', 'UV10sec', 'UV15sec', 'UV20sec', 'UV25ms', 'UV25sec']
g = sns.catplot(
    data=aux, x="Subcategory-02", y="ratio", col="Subcategory-00", order=conditions,
    kind="bar", height=5, aspect=2,
)
# g.set_axis_labels("", "Survival Rate")
# g.set_xticklabels()
g.despine(left=True)
# plt.ylim([0,10])
plt.yscale("log")
plt.show()
#

