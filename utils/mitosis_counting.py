import os
from tifffile import imread
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from utils.morphology import roundnessCalculator
from utils.display import plot_smooth_curves


def smooth(y, t_win):
    """
    Smooth a curve by convolving it with a time window of size t_win

    :param y: input 1D signal
    :param t_win: size of the convolution kernel
    :return: smooth curve y_smooth
    """
    t = np.ones(t_win) / t_win
    y_smooth = np.convolve(y, t, mode='same')
    return y_smooth


def extract_info(frame, t, frame_rate, min_roundness, column_data):
    labels = np.unique(frame)
    r_axis = []
    r_pro = []
    count = 0
    for l in labels:
        if l > 0:
            cell = (frame == l).astype(np.uint8)
            r_axis.append(roundnessCalculator(cell, projected=False))
            r_pro.append(roundnessCalculator(cell, projected=True))
            if roundnessCalculator(cell, projected=False) > min_roundness:
                count += 1
    mitosis = count
    t = frame_rate * t
    # initialize list of lists
    data = [[t, mitosis, r_axis, r_pro] + column_data]
    columns = ["Subcategory-{:02d}".format(i) for i in range(len(column_data))]
    aux = pd.DataFrame(data, columns=['frame', 'mitosis', "roundness_axis", "roundness_projected"] + columns)
    return aux


def count_mitosis(path, stacks=False, pd_dataframe=None, column_data=[], frame_rate=10, min_roundness=0.85):
    """
    This function parses all the folders contained in the path and will output a pandas data frame with each category
    and subcategory labelled, the fram, time and number of mitosis detected in the image.
    :param path: path containing the folders
    :param pd_dataframe: usually empty as it will create it. Include an old one if you want to concatenate-
    :param column_data: If you want to add an extra category, fill it. Otherwise, leave it with the default []
    :param frame_rate: Frame rate of the videos. 10 by default. Units should be controlled by the user.
    :return:updated pd_dataframe variable with the information.
    """
    folders = os.listdir(path)
    folders.sort
    print(folders)
    for f in folders:
        if f[0] != '.':
            if not f.__contains__('.'):
                pd_dataframe = count_mitosis(os.path.join(path, f), stacks=stacks, pd_dataframe=pd_dataframe,
                                             column_data=column_data + [f], frame_rate=frame_rate,
                                             min_roundness=min_roundness)
            elif f.__contains__('.tif'):
                print(f)
                im = imread(os.path.join(path, f))
                if stacks == False:
                    t = int(f.split('_')[-1].split('.')[0])  # naming 00_0000.tif'
                    aux = extract_info(im, t, frame_rate, min_roundness, column_data)
                else:
                    aux = None
                    for t in range(len(im)):
                        frame = im[t]
                        aux_t = extract_info(frame, t, frame_rate, min_roundness, column_data + [f.split('.tif')[0]])
                        if aux is None:
                            aux = aux_t
                        else:
                            aux = pd.concat([aux, aux_t]).reset_index(drop=True)
                # Concatenate pandas data frame to the previous one
                if pd_dataframe is None:
                    pd_dataframe = aux
                else:
                    pd_dataframe = pd.concat([pd_dataframe, aux]).reset_index(drop=True)

    return pd_dataframe


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
