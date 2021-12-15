import os
from tifffile import imread
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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

def count_mitosis(path, pd_dataframe=None, column_data=[], frame_rate = 10):
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
            if not f.__contains__('.tif'):
                pd_dataframe = count_mitosis(os.path.join(path,f), pd_dataframe=pd_dataframe, column_data=column_data + [f])
            else:
                im = imread(os.path.join(path,f))
                labels = np.unique(im)
                mitosis = len(labels)-1
                t = frame_rate * (int(f.split('_')[-1].split('.')[0])) # naming 00_0000.tif'
                # initialize list of lists
                data = [[t, mitosis] + column_data]
                columns = ["Subcategory-{:02d}".format(i) for i in range(len(column_data))]
                # Create the pandas DataFrame
                aux = pd.DataFrame(data, columns=['frame', 'mitosis']+columns)
                # Concatenate pandas data frame to the previous one
                if pd_dataframe is None:
                    pd_dataframe = aux
                else:
                    pd_dataframe = pd.concat([pd_dataframe, aux]).reset_index(drop=True)


    return pd_dataframe

# Extract measures
path = '/Volumes/OCB-All/Projects/OCB004_Phototoxicity/Analysis/StarDist/results'
data = count_mitosis(path)

# Smooth curves
data['Subcategory-02'] = 'raw'
t_win = 15
videos = np.unique(data['Subcategory-01'])
for i in videos:
    video = data[data['Subcategory-01']==i]
    video = video.sort_values('frame')
    y = smooth(video['mitosis'], t_win)
    video['Subcategory-02'] = 'Averaged'
    video['mitosis'] = y
    data = pd.concat([data, video]).reset_index(drop=True)

# Plot the results per category
plt.figure()
sns.lineplot(x="frame", y="mitosis", hue='Subcategory-01', style='Subcategory-02', data=data, palette="tab10", linewidth=1.5)
plt.ylabel("# Mitosis")
plt.xlabel("Time (min)")
plt.show()

