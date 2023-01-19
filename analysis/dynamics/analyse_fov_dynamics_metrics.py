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
# dynamics_metrics_data = dynamics_metrics[dynamics_metrics["Subcategory-00"]=="2022-08-03"]
# dynamics_metrics_video = dynamics_metrics_data[dynamics_metrics_data['video_name']=="CHO_live_-01-Scene-11-P1-A02"]
# index = dynamics_metrics_video.index.to_list()
# dynamics_metrics = dynamics_metrics.drop(index)
# dynamics_metrics.to_csv(os.path.join(output_path, folder, "data_dynamics_intensity_{}_clean.csv".format("UV")))

# dynamics_metrics.to_csv(os.path.join(output_path, folder, "data_dynamics_intensity_{}_clean.csv".format("UV")))

# conditions = ['Control-sync', 'Synchro', 'UV25ms', 'UV50ms', 'UV100ms', 'UV200ms', 'UV400ms', 'UV800ms', 'UV01sec',
#               'UV05sec', 'UV10sec', 'UV15sec', 'UV20sec', 'UV25sec']
#
# fig = plt.figure(figsize=(10, 8))
# plt.rcParams.update({'font.size': 12})
# sns.lineplot(x="frame", y="time_variance", hue="Subcategory-02", data=dynamics_metrics,
#              palette=sns.color_palette("husl", 14),
#              hue_order=conditions, linewidth=1.5, alpha=1)
# plt.tight_layout()
# plt.title("Dynamics_{0}_variance_{1}".format("intensity", condition))
# fig.savefig(os.path.join(output_path, folder, "data_dynamics_intensity_{}_clean.png".format(condition)), format='png',
#             transparent=True)
# plt.show()
# for date in np.unique(dynamics_metrics["Subcategory-00"]):
#     date_dynamics = dynamics_metrics[dynamics_metrics["Subcategory-00"]==date].reset_index(drop=True)
#     fig = plt.figure(figsize=(10, 8))
#     plt.rcParams.update({'font.size': 12})
#     sns.lineplot(x="frame", y="time_variance", hue="Subcategory-02", data=date_dynamics,
#                  palette=sns.color_palette("husl", 14),
#                  hue_order=conditions, linewidth=1.5, alpha=1)
#     plt.tight_layout()
#     plt.title("Dynamics_variance_{0}_{1}".format(condition, date))
#     fig.savefig(os.path.join(output_path, folder, "data_dynamics_intensity_{0}_clean_{1}.png".format(condition, date)), format='png',
#                 transparent=False)
#     plt.show()


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
aux = aux.astype({'ratio': 'float32', 'alpha': 'float32', 'beta': 'float32', 'peak_time': 'float32'})

aux_1 = None
for f in np.unique(aux["Subcategory-00"]):
    folder_wise = aux[aux["Subcategory-00"]==f].reset_index(drop=True)
    s_mean = np.mean(folder_wise[folder_wise["Subcategory-02"] == "Synchro"]["peak_time"])
    folder_wise["delay_synchro"] = (folder_wise["peak_time"] - s_mean)
    folder_wise["proportional_delay_synchro"] = (folder_wise["peak_time"] - s_mean)*(100/s_mean)
    if aux_1 is None:
        aux_1 = folder_wise
    else:
        aux_1 = pd.concat([aux_1, folder_wise]).reset_index(drop=True)
# synchro_data = aux_1[aux_1["Subcategory-02"]=="Synchro"]
# index = synchro_data.index.to_list()
# aux_1 = aux_1.drop(index)
# synchro_data = aux_1[aux_1["Subcategory-02"]=="Control-sync"]
# index = synchro_data.index.to_list()
# aux_1 = aux_1.drop(index)
aux_1 = aux_1.reset_index(drop=True)

### TIME PEAK --------------------------------------------------------------------
### BOXPLOTS TIME POINTS
conditions_folders = ['2022-08-03', '2022-08-03-night', '2022-08-09', '2022-08-09-night',
       '2022-08-10', '2022-09-08-night']

sns.set(font_scale=0.9)
g = sns.catplot(data=aux, x="Subcategory-02", y="peak_time", hue="Subcategory-00",
                order=conditions, hue_order=conditions_folders, kind="box", height=5, aspect=2, palette="rainbow"
                )
g.set_axis_labels("Exposure times", "Time point of maximum peak")
g.despine(left=True)
plt.ylim([-50, 190])
# plt.yscale("log")
plt.show()

# BOXPLOTS TIME POINTS
sns.set(font_scale=0.9)
g = sns.catplot(data=aux, x="Subcategory-02", y="peak_time",
                order=conditions, kind="box", height=5, aspect=2, palette="rainbow_r"
                )
g.set_axis_labels("Exposure times", "Time point of maximum peak (minutes)")
g.despine(left=True)
plt.ylim([-50, 190])
# plt.yscale("log")
plt.show()

# BOXPLOTS TIME POINTS
sns.set(font_scale=0.9)
g = sns.catplot(data=aux_1, x="Subcategory-02", y="delay_synchro", hue="Subcategory-00",
                order=conditions, hue_order=conditions_folders,  kind="box", height=5, aspect=2, palette="rainbow"
                )
g.set_axis_labels("Exposure times", "Delay for the maximum peak (minutes)")
g.despine(left=True)
plt.ylim([-50, 190])
# plt.yscale("log")
plt.show()

# BOXPLOTS TIME POINTS
sns.set(font_scale=0.9)
g = sns.catplot(data=aux_1, x="Subcategory-02", y="delay_synchro",
                order=conditions, kind="box", height=5, aspect=2, palette="rainbow_r"
                )
g.set_axis_labels("Exposure times", "Delay for the maximum peak (minutes)")
g.despine(left=True)
plt.ylim([-50, 190])
# plt.yscale("log")
plt.show()

# BOXPLOTS TIME POINTS
sns.set(font_scale=0.9)
g = sns.catplot(data=aux_1, x="Subcategory-02", y="proportional_delay_synchro", hue="Subcategory-00",
                order=conditions, hue_order=conditions_folders,  kind="box", height=5, aspect=2, palette="rainbow"
                )
g.set_axis_labels("Exposure times", "Delay proportion for the maximum peak (minutes)")
g.despine(left=True)
# plt.yscale("log")
plt.show()

# BOXPLOTS TIME POINTS
sns.set(font_scale=0.9)
g = sns.catplot(data=aux_1, x="Subcategory-02", y="proportional_delay_synchro",
                order=conditions, kind="box", height=5, aspect=2, palette="rainbow_r"
                )
g.set_axis_labels("Exposure times", "Delay proportion for the maximum peak (minutes)")
g.despine(left=True)
# plt.yscale("log")
plt.show()

###



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


#
#
# sns.set_theme(style="dark")
#
# # Plot each year's time series in its own facet
# g = sns.relplot(
#     data=dynamics_metrics,
#     x="frame", y="time_variance", col="Subcategory-02", hue="Subcategory-00",
#     kind="line", palette="crest", linewidth=4, zorder=5,
#     col_wrap=3, height=2, aspect=1.5, legend=False,
# )
#
# # Iterate over each subplot to customize further
# for year, ax in g.axes_dict.items():
#
#     # Add the title as an annotation within the plot
#     ax.text(.8, .85, year, transform=ax.transAxes, fontweight="bold")
#
#     # Plot every year's time series in the background
#     sns.lineplot(
#         data=dynamics_metrics, x="frame", y="time_variance", units="Subcategory-02",
#         estimator=None, color=".7", linewidth=1, ax=ax,
#     )
#
# # Reduce the frequency of the x axis ticks
# ax.set_xticks(ax.get_xticks()[::2])
#
# # Tweak the supporting aspects of the plot
# g.set_titles("")
# g.set_axis_labels("", "Passengers")
# g.tight_layout()