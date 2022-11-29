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
condition = "UV"
# dynamics_metrics = pd.read_csv(os.path.join(output_path, folder, "data_dynamics_intensity_{}.csv".format(condition)))
dynamics_metrics = pd.read_csv(
    os.path.join(output_path, folder, "data_dynamics_intensity_{}_clean.csv".format(condition)))

#
# # EXAMPLE OF HOW TO CLEAN DATA
# # ---------------------------------------
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
#


# dynamics_metrics_data = dynamics_metrics[dynamics_metrics['Subcategory-01']=='WL UV - high density']
# dynamics_metrics_data = dynamics_metrics_data.reset_index(drop=True)
# dynamics_metrics_data.to_csv(os.path.join(output_path, folder, "data_dynamics_intensity_{}.csv".format("UV")))
#
# dynamics_metrics_data = dynamics_metrics[dynamics_metrics["Subcategory-00"]=='2022-09-08-night']
# dynamics_metrics_video = dynamics_metrics_data[dynamics_metrics_data['video_name']=="CHO_live_UV_live-01-Scene-52-P10-B03"]
# index = dynamics_metrics_video.index.to_list()
# dynamics_metrics = dynamics_metrics.drop(index)
# dynamics_metrics.to_csv(os.path.join(output_path, folder, "data_dynamics_intensity_{}_clean.csv".format("UV")))
#
# dynamics_metrics_data = dynamics_metrics[dynamics_metrics["Subcategory-00"]=='2022-08-09']
# dynamics_metrics_video = dynamics_metrics_data[dynamics_metrics_data['video_name']=="CHO_live-01-Scene-47-P8-B04"]
# index = dynamics_metrics_video.index.to_list()
# dynamics_metrics = dynamics_metrics.drop(index)
# dynamics_metrics.to_csv(os.path.join(output_path, folder, "data_dynamics_intensity_{}_clean.csv".format("UV")))
#
# dynamics_metrics_data = dynamics_metrics[dynamics_metrics["Subcategory-00"]=='2022-09-08-night']
# dynamics_metrics_video = dynamics_metrics_data[dynamics_metrics_data['video_name']=="CHO_live_UV_live-01-Scene-48-P10-B04"]
# index = dynamics_metrics_video.index.to_list()
# dynamics_metrics = dynamics_metrics.drop(index)
# dynamics_metrics.to_csv(os.path.join(output_path, folder, "data_dynamics_intensity_{}_clean.csv".format("UV")))
# dynamics_metrics_data = dynamics_metrics[dynamics_metrics["Subcategory-00"]=='2022-08-09']
# dynamics_metrics_video = dynamics_metrics_data[dynamics_metrics_data['video_name']=="CHO_live-01-Scene-58-P9-B03"]
# index = dynamics_metrics_video.index.to_list()
# dynamics_metrics = dynamics_metrics.drop(index)
# dynamics_metrics.to_csv(os.path.join(output_path, folder, "data_dynamics_intensity_{}_clean.csv".format("UV")))

# dynamics_metrics_data = dynamics_metrics[dynamics_metrics["Subcategory-00"]=='2022-09-08-night']
# dynamics_metrics_video = dynamics_metrics_data[dynamics_metrics_data['video_name']=="CHO_live_UV_live-01-Scene-50-P6-B04"]
# index = dynamics_metrics_video.index.to_list()
# dynamics_metrics = dynamics_metrics.drop(index)
# dynamics_metrics.to_csv(os.path.join(output_path, folder, "data_dynamics_intensity_{}_clean.csv".format("UV")))

# dynamics_metrics_data = dynamics_metrics[dynamics_metrics["Subcategory-00"]=='2022-09-08-night']
# dynamics_metrics_video = dynamics_metrics_data[dynamics_metrics_data['video_name']=="CHO_live_UV_live-01-Scene-29-P3-A03"]
# index = dynamics_metrics_video.index.to_list()
# dynamics_metrics = dynamics_metrics.drop(index)
# dynamics_metrics.to_csv(os.path.join(output_path, folder, "data_dynamics_intensity_{}_clean.csv".format("UV")))
#
# dynamics_metrics_data = dynamics_metrics[dynamics_metrics["Subcategory-00"]=='2022-08-09-night']
# dynamics_metrics_video = dynamics_metrics_data[dynamics_metrics_data['video_name']=="CHO_live_night_-01-Scene-49-P1-B04"]
# index = dynamics_metrics_video.index.to_list()
# dynamics_metrics = dynamics_metrics.drop(index)
# dynamics_metrics_video = dynamics_metrics_data[dynamics_metrics_data['video_name']=="CHO_live_night_-01-Scene-47-P10-B04"]
# index = dynamics_metrics_video.index.to_list()
# dynamics_metrics = dynamics_metrics.drop(index)
# dynamics_metrics_video = dynamics_metrics_data[dynamics_metrics_data['video_name']=="CHO_live_night_-01-Scene-44-P5-B04"]
# index = dynamics_metrics_video.index.to_list()
# dynamics_metrics = dynamics_metrics.drop(index)
#
# dynamics_metrics.to_csv(os.path.join(output_path, folder, "data_dynamics_intensity_{}_clean.csv".format("UV")))

conditions = ['Control-sync', 'Synchro', 'UV25ms', 'UV50ms', 'UV100ms', 'UV200ms', 'UV400ms', 'UV800ms', 'UV01sec',
              'UV05sec', 'UV10sec', 'UV15sec', 'UV20sec', 'UV25sec']

fig = plt.figure(figsize=(10, 8))
plt.rcParams.update({'font.size': 12})
sns.lineplot(x="frame", y="time_variance", hue="Subcategory-02", data=dynamics_metrics,
             palette=sns.color_palette("husl", 14),
             hue_order=conditions, linewidth=1.5, alpha=1)
plt.tight_layout()
plt.title("Dynamics_{0}_variance_{1}".format("intensity", condition))
fig.savefig(os.path.join(output_path, folder, "data_dynamics_intensity_{}_clean.png".format(condition)), format='png',
            transparent=True)
plt.show()

aux = None
for v in np.unique(dynamics_metrics["video_name"]):
    video_data = dynamics_metrics[dynamics_metrics["video_name"] == v].reset_index(drop=True)
    frame_rate = 4
    init_mit = int(25 / frame_rate) #30
    final_mit = int(180 / frame_rate) #80
    alpha = np.max(video_data.iloc[init_mit:final_mit]["time_variance"])
    peak_time = video_data.loc[video_data.iloc[init_mit:final_mit]["time_variance"].idxmax(skipna=True), "frame"]
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
        ratio = alpha / beta
    # ratio = (alpha - beta) / (alpha + beta)
    data += [v, alpha, beta, ratio, peak_time]
    columns += ["video_name", "alpha", "beta", "ratio", "peak_time"]

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
plt.figure(figsize=(10, 5))
sns.set(font_scale=1)
# conditions = ['Control-sync', 'Synchro', 'UV50ms', 'UV100ms', 'UV200ms', 'UV400ms', 'UV800ms', 'UV1000ms']
conditions = ['Control-sync', 'Synchro', 'UV25ms', 'UV50ms', 'UV100ms', 'UV200ms', 'UV400ms', 'UV800ms', 'UV01sec',
              'UV05sec', 'UV10sec', 'UV15sec', 'UV20sec', 'UV25sec']
g = sns.swarmplot(data=aux, x="Subcategory-02", y="ratio", hue="Subcategory-02", order=conditions, palette="dark",
                  legend=None)
plt.ylim([0.1, 50])
plt.yscale("log")
plt.tight_layout()
plt.show()

### POINTS
# conditions = ['Control-sync', 'Synchro', 'UV50ms', 'UV100ms', 'UV200ms', 'UV400ms', 'UV800ms', 'UV1000ms']
conditions = ['Control-sync', 'Synchro', 'UV25ms', 'UV50ms', 'UV100ms', 'UV200ms', 'UV400ms', 'UV800ms', 'UV01sec',
              'UV05sec', 'UV10sec', 'UV15sec', 'UV20sec', 'UV25sec']
sns.set(font_scale=0.9)
g = sns.catplot(data=aux, x="Subcategory-02", y="alpha", hue="Subcategory-00", order=conditions, height=5, aspect=2)
g.set_axis_labels("Exposure times", "Alpha")
g.despine(left=True)
plt.ylim([0.00001, 0.1])
plt.yscale("log")
plt.show()

### POINTS
sns.set(font_scale=0.9)
g = sns.catplot(data=aux, x="Subcategory-02", y="beta", hue="Subcategory-00", order=conditions, height=5, aspect=2)
g.set_axis_labels("Exposure times", "Beta")
g.despine(left=True)
plt.ylim([0.00001, 0.1])
plt.yscale("log")
plt.show()

### POINTS
sns.set(font_scale=0.9)
g = sns.catplot(data=aux, x="Subcategory-02", y="ratio", hue="Subcategory-00", order=conditions, height=5, aspect=2)
g.set_axis_labels("Exposure times", "Ratio = alpha / beta")
g.despine(left=True)
plt.ylim([0.1, 50])
plt.yscale("log")
plt.show()

### BARS
# conditions = ['Control-sync', 'Synchro', 'UV50ms', 'UV100ms', 'UV200ms', 'UV400ms', 'UV800ms', 'UV1000ms']
conditions = ['Control-sync', 'Synchro', 'UV25ms', 'UV50ms', 'UV100ms', 'UV200ms', 'UV400ms', 'UV800ms', 'UV1000ms',
              'UV01sec',
              'UV05sec', 'UV10sec', 'UV15sec', 'UV20sec', 'UV25sec']
g = sns.catplot(
    data=aux, x="Subcategory-02", y="ratio", hue="Subcategory-00", order=conditions, kind="bar",
    height=4, aspect=3)
g.set_axis_labels("", "Ratio = alpha / beta")
# g.set_xticklabels()
g.despine(left=True)
# plt.ylim([0,10])
plt.yscale("log")
sns.set(font_scale=1)
plt.show()

### BARS COLUMNS
# conditions = ['Control-sync', 'Synchro', 'UV50ms', 'UV100ms', 'UV200ms', 'UV400ms', 'UV800ms', 'UV1000ms']
conditions = ['Control-sync', 'Synchro', 'UV25ms', 'UV50ms', 'UV100ms', 'UV200ms', 'UV400ms', 'UV800ms', 'UV1000ms',
              'UV01sec',
              'UV05sec', 'UV10sec', 'UV15sec', 'UV20sec', 'UV25sec']
sns.set(font_scale=0.8)
g = sns.catplot(
    data=aux, x="Subcategory-02", y="ratio", col="Subcategory-00", order=conditions,
    kind="bar", height=5, aspect=2,
)
g.set_axis_labels("", "Ratio = alpha / beta")
# g.set_xticklabels()
g.despine(left=True)
# plt.ylim([0,10])
plt.yscale("log")
plt.show()
#
#
# # aux = aux[aux["Subcategory-00"]=='2022-08-09-night']
# aux1 = dynamics_metrics_data[dynamics_metrics_data["Subcategory-02"]=='UV25sec']
# plt.figure()
# # ax = sns.swarmplot(data=aux1, x="Subcategory-02", y="ratio", hue="video_name", palette="dark")
# ax = sns.lineplot(data=aux1, x="frame", y="time_variance", hue="video_name", palette="dark")
# plt.yscale("log")
# sns.set(font_scale=1)
# # plt.ylim([0,10])
# # plt.yscale("log")
# plt.show()
