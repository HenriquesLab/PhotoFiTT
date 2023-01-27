"""
Created on 2023
Henriques Lab

This scripts extracts analyses the motility metrics extracted with `extract_fov_motility`.

The script is not meant to run automatically. It has sections to clean the data or concatenate it.
"""
import pandas as pd
import os

output_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/CHO/results/scaled_1.5709_results/stardist_prob03/"
folder = "dynamics_clahe"
condition = "475"
# dynamics_metrics = pd.read_csv(os.path.join(output_path, folder, "data_dynamics_intensity_{}.csv".format(condition)))
dynamics_metrics = pd.read_csv(
    os.path.join(output_path, folder, "data_dynamics_intensity_{}.csv".format(condition)))




# # # EXAMPLE OF HOW TO CLEAN DATA
### ---------------------------------------
## ---------- 475 -----------------
# dynamics_metrics = pd.read_csv(
#     os.path.join(output_path, folder, "data_dynamics_intensity_{}.csv".format("475")))
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

# # Storing the UV data only
## ---------- UV -----------------
# dynamics_metrics_data = dynamics_metrics[dynamics_metrics['Subcategory-01']=='WL UV - high density']
# dynamics_metrics_data = dynamics_metrics_data.reset_index(drop=True)
# dynamics_metrics_data.to_csv(os.path.join(output_path, folder, "data_dynamics_intensity_{}.csv".format("UV")))
#

## # CLEANING UV DATA
### ---------------------------------------
# dynamics_metrics_data = dynamics_metrics[dynamics_metrics["Subcategory-00"]=='2022-09-08-night']
# dynamics_metrics_video = dynamics_metrics_data[dynamics_metrics_data['video_name']=="CHO_live_UV_live-01-Scene-52-P10-B03"]
# index = dynamics_metrics_video.index.to_list()
# dynamics_metrics = dynamics_metrics.drop(index)
# # dynamics_metrics.to_csv(os.path.join(output_path, folder, "data_dynamics_intensity_{}_clean.csv".format("UV")))
# #
# dynamics_metrics_data = dynamics_metrics[dynamics_metrics["Subcategory-00"]=='2022-08-09']
# dynamics_metrics_video = dynamics_metrics_data[dynamics_metrics_data['video_name']=="CHO_live-01-Scene-47-P8-B04"]
# index = dynamics_metrics_video.index.to_list()
# dynamics_metrics = dynamics_metrics.drop(index)
# #
# dynamics_metrics_data = dynamics_metrics[dynamics_metrics["Subcategory-00"]=='2022-09-08-night']
# dynamics_metrics_video = dynamics_metrics_data[dynamics_metrics_data['video_name']=="CHO_live_UV_live-01-Scene-48-P10-B04"]
# index = dynamics_metrics_video.index.to_list()
# dynamics_metrics = dynamics_metrics.drop(index)
#
# dynamics_metrics_data = dynamics_metrics[dynamics_metrics["Subcategory-00"]=='2022-08-09']
# dynamics_metrics_video = dynamics_metrics_data[dynamics_metrics_data['video_name']=="CHO_live-01-Scene-58-P9-B03"]
# index = dynamics_metrics_video.index.to_list()
# dynamics_metrics = dynamics_metrics.drop(index)
#
# dynamics_metrics_data = dynamics_metrics[dynamics_metrics["Subcategory-00"]=='2022-09-08-night']
# dynamics_metrics_video = dynamics_metrics_data[dynamics_metrics_data['video_name']=="CHO_live_UV_live-01-Scene-50-P6-B04"]
# index = dynamics_metrics_video.index.to_list()
# dynamics_metrics = dynamics_metrics.drop(index)
#
# dynamics_metrics_data = dynamics_metrics[dynamics_metrics["Subcategory-00"]=='2022-09-08-night']
# dynamics_metrics_video = dynamics_metrics_data[dynamics_metrics_data['video_name']=="CHO_live_UV_live-01-Scene-29-P3-A03"]
# index = dynamics_metrics_video.index.to_list()
# dynamics_metrics = dynamics_metrics.drop(index)
# #
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
# #
# dynamics_metrics_data = dynamics_metrics[dynamics_metrics["Subcategory-00"]=="2022-08-03"]
# dynamics_metrics_video = dynamics_metrics_data[dynamics_metrics_data['video_name']=="CHO_live_-01-Scene-11-P1-A02"]
# index = dynamics_metrics_video.index.to_list()
# dynamics_metrics = dynamics_metrics.drop(index)
#
# dynamics_metrics.to_csv(os.path.join(output_path, folder, "data_dynamics_intensity_{}_clean.csv".format("UV")))

#