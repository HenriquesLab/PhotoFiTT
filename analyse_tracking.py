import os
import sys
## Include the following lines to access the code in Python Console
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
SCRIPT_DIR = '/Users/esti/Documents/PROYECTOS/PHX/mitosis-mediated-phototoxic'
sys.path.append(SCRIPT_DIR)
from utils.tracking import tracking_metrics
from utils.display import plot_smooth_curves,  plot_conditions_with_aggregates

## This code will be move to the main scripts

main_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/masks/scaled_1.5709_results/stardist_prob03/"
output_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/results/scaled_1.5709_results/stardist_prob03"
folder = "tracking"
if not os.path.exists(os.path.join(output_path, folder)):
    os.mkdir(os.path.join(output_path, folder))
track_info = tracking_metrics(main_path, frame_rate=4, track_threshold=0.25)
track_info.to_csv(os.path.join(output_path, "data_tracking.csv"))

for c in np.unique(track_info["Subcategory-01"]):
    track_info_group = track_info[track_info["Subcategory-01"]==c].reset_index(drop=True)

    plot_smooth_curves(track_info_group, "mitoses", "Distribution of mitoses_{}".format(c),
                       os.path.join(output_path, folder), "Distribution of mitoses_1_{}.png".format(c))
    plot_conditions_with_aggregates(track_info_group, "mitoses",  "Distribution of mitoses_{}".format(c),
                                    os.path.join(output_path, folder), "Distribution of mitoses_2_{}.png".format(c),
                                    hue="Subcategory-02", style="Subcategory-01")
## Use this code to check what are the trackings being recovered

# file = "2022-09-07-day/WL 475 - high density/Synchro/CHO_day_475_live-01-Scene-74-P10-B01.tif"
# inst_mask = imread(os.path.join(main_path, file))
# average_mask, tracks_3D = fill_gaps(inst_mask, track_threshold=0.25)
# imsave("/Users/esti/Downloads/prueba_tracks_{}.tif".format(file.split("Scene")[-1]), tracks_3D)
# imsave("/Users/esti/Downloads/prueba_average_{}.tif".format(file.split("Scene")[-1]), average_mask)
# imsave("/Users/esti/Downloads/prueba_raw_{}.tif".format(file.split("Scene")[-1]), inst_mask)
# counts = count_tracked_divisions(tracks_3D, average_mask)
# import matplotlib.pyplot as plt
# plt.plot(counts[:, 0], counts[:, 1], '-')
# plt.show()