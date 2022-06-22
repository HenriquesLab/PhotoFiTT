import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
SCRIPT_DIR = '/Users/esti/Documents/PROYECTOS/PHX/mitosis-mediated-phototoxic'
sys.path.append(SCRIPT_DIR)
from utils.display import plot_smooth_curves
from utils.mitosis_counting import count_mitosis, smooth
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import sys
#main_path = sys.argv[1]
#output_path = sys.argv[2]
#frame_rate = int(sys.argv[3]) # In minutes or "unknown" if unknown and will be taken from the folder name

main_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis-mediated-data-itqb/masks/scaled_1.5709_results/stardist_prob03/"
output_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis-mediated-data-itqb/results/scaled_1.5709_results/stardist_prob03/"
frame_rate = 4

if not os.path.exists(output_path):
    os.mkdir(output_path)
min_roundness = [0.0, 0.5, 0.85, 0.9, 0.95, 0.97]
folders = os.listdir(main_path)
for f in folders:
    path = os.path.join(main_path, f)
    if os.path.isdir(path):
        if frame_rate == "unknown":
            if path.__contains__("damage_merged"):
                frame_rate = 10
            elif path.__contains__("fast"):
                frame_rate = 2
            elif path.__contains__("10"):
                frame_rate = 10
            elif path.__contains__("4"):
                frame_rate = 4
            else:
                print("Unrecognized group of data. Please indicate the frame rate in the code.")
                break
        for r in min_roundness:
            data = count_mitosis(path, stacks=True, frame_rate=frame_rate, min_roundness=r)
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
            if not os.path.exists(os.path.join(output_path, f)):
                os.mkdir(os.path.join(output_path, f))
            title = "Minimum roundness {}".format(r)
            y_var = "mitosis"
            name = "mitosis_roundness-{}.png".format(r)
            plot_smooth_curves(data1, y_var, title, os.path.join(output_path, f), name)
            # Display
            title = "Minimum roundness {}".format(r)
            y_var = "mitosis_normalised"
            name = "normalised_mitosis_roundness-{}.png".format(r)
            plot_smooth_curves(data1, y_var, title, os.path.join(output_path, f), name)


        ## Display roundness
        data2 = data1[data1["Subcategory-02"] == "Raw"]
        roundness_data = None
        r = 0.0
        for i in range(len(data2)):
            cell = data2.iloc[i]
            if cell.roundness_axis != []:
                CS = cell.cell_size
                RA = cell.roundness_axis
                RP = cell.roundness_projected
                t = cell.frame
                S0 = cell["Subcategory-00"]
                S1 = cell["Subcategory-01"]
                aux_data = [[t, CS[f], RA[f], RP[f], S0, S1] for f in range(len(RA)) if RA[f] > r]
                col_names = ["frame", "cell_size", "roundness_axis", "roundness_projected", "Subcategory-00", "Subcategory-01"]
                aux = pd.DataFrame(aux_data, columns=col_names)

                if roundness_data is None:
                    roundness_data = aux
                else:
                    roundness_data = pd.concat([roundness_data, aux]).reset_index(drop=True)

        fig = plt.figure()
        plt.subplot(1, 3, 1)
        sns.scatterplot(x="frame", y="cell_size", hue='Subcategory-00', data=roundness_data,
                        linewidth=0, alpha=.3, palette="tab10")
        plt.ylabel("Cell size (pixels)")
        plt.xlabel("Time (min)")

        plt.subplot(1, 3, 2)
        sns.scatterplot(x="frame", y="roundness_axis", hue='Subcategory-00', data=roundness_data,
                        linewidth=0, alpha=.5, palette="tab10")
        plt.ylabel("Roundness")
        plt.xlabel("Time (min)")
        # plt.xlim([0,120])
        # plt.ylim([0.7, 1])
        #
        plt.subplot(1, 3, 3)
        sns.scatterplot(x="frame", y="roundness_projected", hue='Subcategory-00', data=roundness_data,
                        linewidth=0, alpha=.5, palette="tab10")
        plt.ylabel("Roundness")
        plt.xlabel("Time (min)")
        # plt.xlim([0,120])
        # plt.ylim([0.7, 1])
        fig.savefig(os.path.join(output_path, f, "roundness_scatterplot.png"), format='png')
        # plt.show()
