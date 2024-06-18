import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


main_path = "/Users/esti/Library/CloudStorage/OneDrive-igc.gulbenkian.pt/Project - PhotoFiTT/SYTOX/SYTOX countings"
path = "/Volumes/OCB-All/Projects/OCB004_Phototoxicity/Analysis/SYTOX/PTX SYTOX/threshold-otsu_z-to-t"


sytox_path = os.path.join(main_path, "SYTOX")
stardist_path = os.path.join(main_path, "STARDIST")



folders = ["sync", "unsync"]

def extract_numbers(path, folders, data_type="stardist"):
    ALL = None
    for f in folders:
        print(f)
        folder_path = os.path.join(path,f)
        groups = [g for g in os.listdir(folder_path) if not g.startswith(".") and not g.endswith(".csv")]
        print(groups)
        for g in groups:
            csv_data = [c for c in os.listdir(os.path.join(folder_path, g)) if not c.startswith(".")]
            for c in csv_data:
                print(c)
                if data_type=="stardist":
                    data = pd.read_csv(os.path.join(folder_path, g, c), header=None)
                    data.columns = ["t_min","total_n"]
                    data["t_min"] = [4 * float(i) for i in data["t_min"]]
                    if f == "sync":
                        c = c.split("cho_sync_unsync_sytox_live_Sync_")[-1]
                    else:
                        c = c.split("cho_sync_unsync_sytox_live_Unsync_")[-1]
                    data["FOV"] = c.split("_Nuclei_number.csv")[0]

                else:
                    data = pd.read_csv(os.path.join(folder_path, g, c), header=1)
                    data = data[1:].reset_index(drop=True)
                    data = data[["Label", "N spots"]]
                    data["Label"] = [4*float(i) for i in data["Label"]]
                    data = data.rename(columns={"N spots": "sytox_n", "Label": "t_min"})
                    data["FOV"] = c.split(".csv")[0]
                data["GROUP"] = g
                data["TYPE"] = f
                if ALL is None:
                    ALL = data
                else:
                    ALL = pd.concat([ALL, data])
    return ALL

def extract_numbers_additive(path, folders):
    ALL = None
    for f in folders:
        print(f)
        folder_path = os.path.join(path,f)
        groups = [g for g in os.listdir(folder_path) if not g.startswith(".") and not g.endswith(".csv")]
        print(groups)
        for g in groups:
            csv_data = [c for c in os.listdir(os.path.join(folder_path, g)) if not c.startswith(".")]
            for c in csv_data:
                print(c)
                csv_files = [c for c in os.listdir(os.path.join(folder_path, g, c)) if c.endswith(".csv")]
                print(csv_files)
                if len(csv_files)>0:
                    if f=="sync" and c == "1s2":
                        data1 = pd.read_csv(os.path.join(folder_path, g, c, csv_files[0]), header=0)
                        print(data1.columns)
                    elif f=="sync" and c == "10s5":
                        print("skipping 10s5")
                    else:

                        data = pd.read_csv(os.path.join(folder_path, g, c, csv_files[0]), header=0)
                        #data = data[1:].reset_index(drop=True)
                        print(data.columns)
                        data = data[["Slice", "Count"]]
                        #print(data)
                        file_name = csv_files[0].split(".csv")[0]
                        data["Label"] = [4*float(i[len(file_name)+1:]) for i in data["Slice"]]
                        data = data.rename(columns={"Count": "sytox_n", "Label": "t_min"})
                        data["FOV"] = c
                        data["GROUP"] = g
                        data["TYPE"] = f
                        if ALL is None:
                            ALL = data
                        else:
                            ALL = pd.concat([ALL, data])
    return ALL

pd_sytox = extract_numbers(sytox_path, folders, data_type="sytox")
pd_stardist = extract_numbers(stardist_path, folders, data_type="stardist")
#pd_sytox = extract_numbers_additive(path, folders)
#pd_sytox.to_csv("/Users/esti/Documents/PROYECTOS/PHX/SYTOX_ADDITIVE/counts.csv")
pd_sytox_additive = pd.read_csv("/Users/esti/Documents/PROYECTOS/PHX/SYTOX_ADDITIVE/counts.csv")

ALL = pd_sytox.merge(pd_stardist, how="inner")
ALL["sytox_ratio"] = ALL["sytox_n"] / ALL["total_n"]

from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
params = {"ytick.color" : "w",
          "xtick.color" : "w",
          "axes.labelcolor" : "w",
          "axes.edgecolor" : "w"}
plt.rcParams.update(params)
params = {"ytick.color" : "k",
          "xtick.color" : "k",
          "axes.labelcolor" : "k",
          "axes.edgecolor" : "k"}
plt.rcParams.update(params)



fig = plt.figure()
plt.subplot(1,2,1)
g = sns.lineplot(data=ALL[ALL["TYPE"]=="sync"],
                 x="t_min", y="sytox_ratio",
                 palette=sns.color_palette("CMRmap_r", 5),
                 linewidth=2.5, hue = "GROUP",
                 hue_order=["C", "100ms", "1s", "10s"])
plt.xlim([0, 180*4])
plt.ylim([0, 0.5])
plt.ylabel("Ratio of Sytox+ cells")
plt.xlabel("Time (min)")
plt.subplot(1,2,2)
g = sns.lineplot(data=ALL[ALL["TYPE"]=="unsync"],
                 x="t_min", y="sytox_ratio",
                 palette=sns.color_palette("CMRmap_r", 5),
                 linewidth=2.5, hue="GROUP",
                 hue_order=["C", "100ms", "1s", "10s"])
plt.ylabel("Ratio of Sytox+ cells")
plt.xlabel("Time (min)")
plt.ylim([0, 0.5])
plt.legend([])
#g2.set_ylabel('Unsyncronised data')
#g.legend(handles=[Rectangle((0,0), 0, 0, color='blue', label='Nontouch device counts'),
#                  Line2D([], [], marker='o', color='orange',
#                label='Detections rate for nontouch devices')], loc=(1.1,0.8))
plt.tight_layout()
#fig.savefig(os.path.join(main_path, "plot.pdf"), format='pdf', transparent=True)
plt.show()


####

new_additive = pd_sytox_additive.merge(pd_stardist, how="inner")
new_additive["sytox_ratio"] = pd_sytox_additive["sytox_n"] / new_additive["total_n"]
new_additive = new_additive[new_additive["TYPE"]=="unsync"]
new_additive["TYPE"]="unsync-additive"
ALL = pd.concat([ALL, new_additive])
ALL = ALL[["t_min", "TYPE", "GROUP", "sytox_ratio"]].reset_index(drop=True)


g = sns.catplot(
    ALL, kind="bar",
    x="t_min", y="sytox_ratio", hue="GROUP",
    col="TYPE",
    height=4, aspect=1.1,
    order=[60, 120, 180, 240, 300, 360, 420],
    hue_order=["C", "1s", "10s"],
    palette=['#C9C9C9', '#99E3D7', '#BC77F8'],
    errorbar=("ci", 95),  capsize=.08, linewidth=0.5,
    col_order=["sync", "unsync", "unsync-additive"], legend=False
)
plt.tight_layout()
g.fig.get_axes()[-1].legend(loc='upper right')
g.set_xticklabels(rotation=30)
g.set_titles("{col_name}")
g.savefig(os.path.join(main_path, "barplots.pdf"), format="pdf", transparent=True)
