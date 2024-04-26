"""
Created on 2021
Henriques Lab

This script is meant to run automatically. Results are stored as csv files with the corresponding conditions, dates and
video names so all the results can be fully tracked.
"""
import pandas as pd
import os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from photofitt.utils import numerical_dose, power_conversion, power_wavelength_conversion
import statsmodels.api as sm
from ast import literal_eval


## READ AND PREPARE THE DATA
# -----------------------------------------------------------------
# -----------------------------------------------------------------

pixel_size = (0.5500000*1.5709)

synchro_data = "/Users/esti/Documents/PROYECTOS/PHX/DOCS/MANUSCRIPT/CODE/data/synchro/mitosis_CHO_UV_clean.csv"
synchro_data = pd.read_csv(synchro_data)
u = [c for c in synchro_data.columns if c.__contains__("Unnamed")]
synchro_data = synchro_data.drop(columns=u)

synchro_data_475 = "/Users/esti/Documents/PROYECTOS/PHX/DOCS/MANUSCRIPT/CODE/data/synchro/mitosis_CHO_475_clean.csv"
synchro_data_475 = pd.read_csv(synchro_data_475)
u = [c for c in synchro_data_475.columns if c.__contains__("Unnamed")]
synchro_data_475 = synchro_data_475.drop(columns=u)

synchro_data_630 = "/Users/esti/Documents/PROYECTOS/PHX/DOCS/MANUSCRIPT/CODE/data/synchro/mitosis_CHO_630_clean.csv"
synchro_data_630 = pd.read_csv(synchro_data_630)
u = [c for c in synchro_data_630.columns if c.__contains__("Unnamed")]
synchro_data_630 = synchro_data_630.drop(columns=u)

synchro_data = pd.concat([synchro_data, synchro_data_475, synchro_data_630]).reset_index(drop=True)
synchro_data = synchro_data[synchro_data["processing"]=="Raw"].reset_index(drop=True)

## Estimate the ligth dose
light_power = 6.255662
data = numerical_dose(synchro_data, column_name="Subcategory-02", power=light_power)
data = power_conversion(synchro_data)

if pd.api.types.is_string_dtype(synchro_data["cell_size"].dtype):
    synchro_data["cell_size"] = synchro_data["cell_size"].apply(literal_eval)
synchro_data = synchro_data.explode("cell_size")
synchro_data["cell_size"] = (pixel_size * pixel_size) * synchro_data["cell_size"]


## LOWESS for one condition
# -----------------------------------------------------------------
# -----------------------------------------------------------------
#
# lowess = sm.nonparametric.lowess
# color_palette = [(0.2, 0.2, 0.2), (0.5, 0.5, 0.5)] + sns.color_palette("CMRmap_r", 15)
# hue_order = ['non-synchro-0 J/cm2', '0 J/cm2', '0.2 J/cm2',
#              '0.3 J/cm2', '0.6 J/cm2', '1.3 J/cm2', '2.5 J/cm2',
#              '5.0 J/cm2', '6.3 J/cm2', '31.3 J/cm2',
#              '62.6 J/cm2', '93.8 J/cm2', '125.1 J/cm2', '156.4 J/cm2']
# hue = "Light dose cat"# plt.figure(figsize=(8,7))
# for i in range(len(hue_order)):
#     s = hue_order[i]
#     aux = synchro_data[synchro_data[hue] == s].reset_index(drop=True)
#     x = np.array(aux["frame"])
#     y = np.array(aux["cell_size"])
#     z = lowess(y, x, it=5, frac=0.2)
#     if i == 0:
#         c = 'k'
#         sns.lineplot(x=z[:, 0], y=z[:, 1], color=c, dashes=(2, 2), markers=True, legend=False, estimator=None)
#     else:
#         c = color_palette[i]
#         sns.lineplot(x=z[:,0], y=z[:,1], color=c, legend=False, estimator=None)
#     #sns.regplot(data=aux, x="frame", y="cell_size", scatter=False, lowess=True, color=color_palette[i])
# plt.legend(hue_order)
# plt.ylim([150, 450])
# #plt.yscale('log')
# plt.show()

# plt.figure(figsize=(8,7))
# sns.lineplot(data=synchro_data.dropna(), x="frame", y="cell_size",
#              hue=hue, hue_order=hue_order,
#              palette=color_palette)
# plt.ylim([150, 450])
# plt.yscale('log')
# plt.tight_layout()
# plt.ylabel("Cell size in microns")
# plt.show()



# REORGANISE
# -----------------------------------------------------------------
# -----------------------------------------------------------------
synchro_data_both = pd.concat(
    [synchro_data[synchro_data["Subcategory-02"] == 'Synchro'],
     synchro_data[synchro_data["Subcategory-02"] == 'Control-sync']])
index = synchro_data_both.index.to_list()
# remove control
synchro_data = synchro_data.drop(index)
# Add a new variable
synchro_data["Illumination"] = synchro_data["Subcategory-01"]
synchro_data_both["Illumination"] = synchro_data_both["Subcategory-02"]
# Concatenate
synchro_data = pd.concat([synchro_data, synchro_data_both])


hue_order = ['Control-sync', 'Synchro', 'WL 630 - high density',
             'WL 475 - high density', 'WL UV - high density']

plt.figure(figsize=(8,7))
sns.lineplot(data=synchro_data.dropna(), x="frame", y="cell_size",
             hue="Illumination", hue_order=hue_order, style="Subcategory-01",
             palette=[(0.5, 0.5, 0.5)] + sns.color_palette("husl", 5)[1:],
             )
plt.ylim([150, 450])
plt.yscale('log')
plt.show()

synchro_data["Light dose Wavelength"] = 0
for wl in np.unique(synchro_data["Subcategory-01"]):
    if wl.__contains__("UV"):
        w_lambda = 385
    elif wl.__contains__("475"):
        w_lambda = 475
    elif wl.__contains__("630"):
        w_lambda = 630
    index = synchro_data[synchro_data["Subcategory-01"]==wl].index.to_list()
    synchro_data.loc[index, "Light dose Wavelength"] = (1/w_lambda) * synchro_data.loc[index, "Light dose"]

synchro_data = power_wavelength_conversion(synchro_data, dose_column="Light dose Wavelength")
hue_order = ['non-synchro-0 J/cm2 (1/nm)', '0 J/cm2 (1/nm)', '0.0 J/cm2 (1/nm)', '0.01 J/cm2 (1/nm)',
       '0.02 J/cm2 (1/nm)', '0.05 J/cm2 (1/nm)', '0.07 J/cm2 (1/nm)',
       '0.08 J/cm2 (1/nm)', '0.1 J/cm2 (1/nm)', '0.13 J/cm2 (1/nm)',
       '0.15 J/cm2 (1/nm)', '0.16 J/cm2 (1/nm)', '0.2 J/cm2 (1/nm)',
       '0.24 J/cm2 (1/nm)', '0.25 J/cm2 (1/nm)', '0.26 J/cm2 (1/nm)',
       '0.3 J/cm2 (1/nm)', '0.32 J/cm2 (1/nm)', '0.33 J/cm2 (1/nm)',
       '0.4 J/cm2 (1/nm)', '0.41 J/cm2 (1/nm)']

# #### COLORBAR
#
# colorbar_data = np.unique(synchro_data["Light dose Wavelength"])
# colorbar_data = colorbar_data[colorbar_data>=0]
# colorbar_data = pd.DataFrame(colorbar_data,
#                              columns=["Light dose wavelength"])
# fig = plt.figure(figsize=(5, 5))
# sns.heatmap(colorbar_data, robust=True,
#             cmap=sns.color_palette("CMRmap_r", 25))
# plt.tight_layout()
# fig.savefig("/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/CHO/results/scaled_1.5709_results/new_data/activity_clahe-intensity/manual/weightedpower_colorbar_25.pdf",
#             format="pdf", transparent=True)
# plt.show()
#
#
# fig = plt.figure(figsize=(5, 5))
# sns.heatmap(colorbar_data, robust=True,
#             cmap=sns.color_palette("CMRmap_r", 100))
# plt.tight_layout()
# fig.savefig("/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/CHO/results/scaled_1.5709_results/new_data/activity_clahe-intensity/manual/weightedpower_colorbar.pdf",
#             format="pdf", transparent=True)
# plt.show()



plt.figure(figsize=(8,7))
sns.lineplot(data=synchro_data.dropna(), x="frame", y="cell_size",
             hue='Light dose Wavelength cat', hue_order=hue_order, style="Illumination",
             palette=[(0.2, 0.2, 0.2), (0.5, 0.5, 0.5)] + sns.color_palette("CMRmap_r", 25),
             )
plt.ylim([150, 450])
plt.yscale('log')
plt.tight_layout()
plt.show()

fig=plt.figure(figsize=(8,7))
sns.set_style()
## Set style
custom_params = {"axes.spines.right": False, "axes.spines.top": False}
sns.plotting_context("paper")
sns.set(font_scale=0.4)
sns.set_theme(style="whitegrid", rc=custom_params)
sns.lineplot(data=synchro_data.dropna(), x="frame", y="cell_size",
             hue='Light dose Wavelength cat', hue_order=hue_order,
             palette=[(0.2, 0.2, 0.2), (0.5, 0.5, 0.5)] + sns.color_palette("CMRmap_r", 25),
             )
plt.ylim([150, 450])
plt.yscale('log')
plt.tight_layout()
fig.savefig("/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/CHO/results/scaled_1.5709_results/new_data/activity_clahe-intensity/manual/cellsize-weightedpower.pdf",
            format="pdf", transparent=True)
plt.show()

wl = ['WL 630 - high density', 'WL 475 - high density', 'WL UV - high density']
plt.figure(figsize=(5,8))
for i in range(len(wl)):
    plt.subplot(3,1,i+1)
    aux = synchro_data[synchro_data["Subcategory-01"]==wl[i]].reset_index(drop=True)
    sns.lineplot(data=aux.dropna(), x="frame", y="cell_size",
                 hue='Light dose Wavelength cat', hue_order=hue_order,
                 palette=[(0.2, 0.2, 0.2), (0.5, 0.5, 0.5)] + sns.color_palette("CMRmap_r", 25),
                 legend=False
                 )
    plt.ylim([150, 450])
    plt.yscale('log')
    plt.title(f"{wl[i]}")
#plt.legend(hue_order)
plt.tight_layout()
plt.show()

wl = ['WL 630 - high density', 'WL 475 - high density', 'WL UV - high density']
hue_order = ['non-synchro-0 J/cm2', '0 J/cm2', '0.2 J/cm2',
             '0.3 J/cm2', '0.6 J/cm2', '1.3 J/cm2', '2.5 J/cm2',
             '5.0 J/cm2', '6.3 J/cm2', '31.3 J/cm2',
             '62.6 J/cm2', '93.8 J/cm2', '125.1 J/cm2', '156.4 J/cm2']
hue = "Light dose cat"
plt.figure(figsize=(5,8))
for i in range(len(wl)):
    plt.subplot(3,1,i+1)
    aux = synchro_data[synchro_data["Subcategory-01"]==wl[i]].reset_index(drop=True)
    sns.lineplot(data=aux.dropna(), x="frame", y="cell_size",
                 hue=hue, hue_order=hue_order,
                 palette=[(0.2, 0.2, 0.2), (0.5, 0.5, 0.5)] + sns.color_palette("CMRmap_r", 15),
                 legend=False
                 )

    plt.ylim([150, 450])
    plt.yscale('log')
    plt.title(f"{wl[i]}")
#plt.legend(hue_order)
plt.tight_layout()
plt.show()


# wl475 = synchro_data[synchro_data["Subcategory-00"]=='20230503_475_night']
# index = wl475.index.to_list()
# synchro_data = synchro_data.drop(index)
#
# wl475 = synchro_data[synchro_data["Subcategory-00"]=='20220929_night']
# index = wl475.index.to_list()
# synchro_data = synchro_data.drop(index)

## LOWESS for wavelengths



lowess = sm.nonparametric.lowess
color_palette = [(0.5, 0.5, 0.5)] + sns.color_palette("husl", 5)[1:] # [(0, 0, 0)] + sns.color_palette("CMRmap_r", 17)[1:]
L_all = None
hue = 'Light dose Wavelength cat'
hue_order = ['non-synchro-0 J/cm2 (1/nm)', '0 J/cm2 (1/nm)', '0.0 J/cm2 (1/nm)', '0.01 J/cm2 (1/nm)',
       '0.02 J/cm2 (1/nm)', '0.05 J/cm2 (1/nm)', '0.07 J/cm2 (1/nm)',
       '0.08 J/cm2 (1/nm)', '0.1 J/cm2 (1/nm)', '0.13 J/cm2 (1/nm)',
       '0.15 J/cm2 (1/nm)', '0.16 J/cm2 (1/nm)', '0.2 J/cm2 (1/nm)',
       '0.24 J/cm2 (1/nm)', '0.25 J/cm2 (1/nm)', '0.26 J/cm2 (1/nm)',
       '0.3 J/cm2 (1/nm)', '0.32 J/cm2 (1/nm)', '0.33 J/cm2 (1/nm)',
       '0.4 J/cm2 (1/nm)', '0.41 J/cm2 (1/nm)']
#hue = 'Light dose cat'
for wl in np.unique(synchro_data["Subcategory-01"]):  # wavelengths

    aux_wl = synchro_data[synchro_data["Subcategory-01"] == wl].reset_index(drop=True)
    L = None
    for s in np.unique(aux_wl[hue]):
        aux = aux_wl[aux_wl[hue] == s].reset_index(drop=True)
        x = np.array(aux["frame"])
        y = np.array(aux["cell_size"])
        z = lowess(y, x, it=5, frac=0.2)
        for i in np.unique(z[:,0]):
            z_new = z
        aux1 = pd.DataFrame(z, columns=['frame', 'cell_size'])
        aux1 = (
            aux1.groupby(["frame"]).agg(['mean'])
        )
        aux1 = aux1.droplevel(axis=1, level=0).reset_index()
        aux1 = aux1.rename(columns={"mean": "cell_size"})
        aux1["Subcategory-01"] = wl
        aux1[hue] = s
        aux1["Illumination"] = aux["Illumination"].iloc[0]

        if L is None:
            L = aux1
        else:
            L = pd.concat([L, aux1]).reset_index(drop=True)

    if L_all is None:
        L_all = L
    else:
        L_all = pd.concat([L_all, L])


    # plt.figure(figsize=(8, 7))
    # sns.lineplot(data = L_all, x = "frame", y="cell_size", hue=hue,
    #              hue_order=hue_order,
    #              palette=[(0.2, 0.2, 0.2), (0.5, 0.5, 0.5)] + sns.color_palette("CMRmap_r", 15))
    # plt.legend(hue_order)
    # plt.ylim([200, 500])
    # plt.title(f"LOWESS all powers by wavelengths")
    # plt.ylabel("Cell size in microns")
    # plt.yscale('log')
    # plt.show()



wl = ['WL 630 - high density', 'WL 475 - high density', 'WL UV - high density']
# hue_order = ['non-synchro-0 J/cm2', '0 J/cm2', '0.2 J/cm2',
#              '0.3 J/cm2', '0.6 J/cm2', '1.3 J/cm2', '2.5 J/cm2',
#              '5.0 J/cm2', '6.3 J/cm2', '31.3 J/cm2',
#              '62.6 J/cm2', '93.8 J/cm2', '125.1 J/cm2', '156.4 J/cm2']
# hue = "Light dose cat"
# color_palette = [(0.2, 0.2, 0.2), (0.5, 0.5, 0.5)] + sns.color_palette("CMRmap_r", 15)

hue = 'Light dose Wavelength cat'
hue_order = ['non-synchro-0 J/cm2 (1/nm)', '0 J/cm2 (1/nm)', '0.0 J/cm2 (1/nm)', '0.01 J/cm2 (1/nm)',
       '0.02 J/cm2 (1/nm)', '0.05 J/cm2 (1/nm)', '0.07 J/cm2 (1/nm)',
       '0.08 J/cm2 (1/nm)', '0.1 J/cm2 (1/nm)', '0.13 J/cm2 (1/nm)',
       '0.15 J/cm2 (1/nm)', '0.16 J/cm2 (1/nm)', '0.2 J/cm2 (1/nm)',
       '0.24 J/cm2 (1/nm)', '0.25 J/cm2 (1/nm)', '0.26 J/cm2 (1/nm)',
       '0.3 J/cm2 (1/nm)', '0.32 J/cm2 (1/nm)', '0.33 J/cm2 (1/nm)',
       '0.4 J/cm2 (1/nm)', '0.41 J/cm2 (1/nm)']

color_palette = [(0.2, 0.2, 0.2), (0.5, 0.5, 0.5)] + sns.color_palette("CMRmap_r", 25)

fig = plt.figure(figsize=(5,8))
sns.set_style()
## Set style
custom_params = {"axes.spines.right": False, "axes.spines.top": False}
sns.plotting_context("paper")
sns.set(font_scale=0.4)
sns.set_theme(style="whitegrid", rc=custom_params)
for i in range(len(wl)):
    plt.subplot(3,1,i+1)
    aux = L_all[L_all["Subcategory-01"]==wl[i]].reset_index(drop=True)
    sns.lineplot(data=aux.dropna(), x="frame", y="cell_size",
                 hue=hue, hue_order=hue_order,
                 palette=color_palette,
                 legend=False
                 )

    plt.ylim([150, 450])
    plt.ylabel("Cell size in microns")
    plt.yscale('log')
    plt.title(f"{wl[i]}")
#plt.legend(hue_order)
plt.tight_layout()
fig.savefig("/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/CHO/results/scaled_1.5709_results/new_data/activity_clahe-intensity/manual/cellsize-lowess-subplots-weightedpower-wl.pdf",
            format="pdf", transparent=True)
plt.show()



wavelengths = ['Control-sync', 'Synchro', 'WL 630 - high density', 'WL 475 - high density',
                        'WL UV - high density']
hue_order = ['non-synchro-0 J/cm2', '0 J/cm2', '0.2 J/cm2',
             '0.3 J/cm2', '0.6 J/cm2', '1.3 J/cm2', '2.5 J/cm2',
             '5.0 J/cm2', '6.3 J/cm2', '31.3 J/cm2',
             '62.6 J/cm2', '93.8 J/cm2', '125.1 J/cm2', '156.4 J/cm2']
hue = "Light dose cat"

hue = 'Light dose Wavelength cat'
hue_order = ['non-synchro-0 J/cm2 (1/nm)', '0 J/cm2 (1/nm)', '0.0 J/cm2 (1/nm)', '0.01 J/cm2 (1/nm)',
       '0.02 J/cm2 (1/nm)', '0.05 J/cm2 (1/nm)', '0.07 J/cm2 (1/nm)',
       '0.08 J/cm2 (1/nm)', '0.1 J/cm2 (1/nm)', '0.13 J/cm2 (1/nm)',
       '0.15 J/cm2 (1/nm)', '0.16 J/cm2 (1/nm)', '0.2 J/cm2 (1/nm)',
       '0.24 J/cm2 (1/nm)', '0.25 J/cm2 (1/nm)', '0.26 J/cm2 (1/nm)',
       '0.3 J/cm2 (1/nm)', '0.32 J/cm2 (1/nm)', '0.33 J/cm2 (1/nm)',
       '0.4 J/cm2 (1/nm)', '0.41 J/cm2 (1/nm)']

color_palette = [(0.2, 0.2, 0.2), (0.5, 0.5, 0.5)] + sns.color_palette("CMRmap_r", 25)

fig = plt.figure(figsize=(8, 10))
sns.set_style()
## Set style
custom_params = {"axes.spines.right": False, "axes.spines.top": False}
sns.plotting_context("paper")
sns.set(font_scale=0.4)
sns.set_theme(style="whitegrid", rc=custom_params)

plt.subplot(2,1,1)
sns.lineplot(data = L_all, x = "frame", y="cell_size",
             hue=hue,
             hue_order=hue_order,
             legend=False,
             palette=color_palette)
plt.ylim([150, 500])
plt.title(f"LOWESS for all light dose")
plt.ylabel("Cell size in microns")
#plt.yscale('log')
plt.subplot(2,1,2)
sns.lineplot(data = L_all, x = "frame", y="cell_size",
             hue="Illumination",
             hue_order=wavelengths,
             legend=True,
             palette=[(0.5, 0.5, 0.5)] + sns.color_palette("husl", 5)[1:])
plt.ylim([150, 500])
plt.title(f"LOWESS for wavelengths")
plt.ylabel("Cell size in microns")
#plt.yscale('log')
# fig.savefig("/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_3/CHO/results/scaled_1.5709_results/new_data/activity_clahe-intensity/manual/Figure_lowess.pdf",
#             format="pdf", transparent=True)
plt.tight_layout()
plt.show()



##### 475
plt.figure()
aux = synchro_data[synchro_data["Subcategory-01"]=='WL 475 - high density']
aux = aux[aux["Illumination"]=='Synchro']
sns.lineplot(data=aux.dropna(), x="frame", y="cell_size",
             hue="Subcategory-00",
             palette=[(0.5, 0.5, 0.5)] + sns.color_palette("husl", 8)[1:],
             )