from photofitt.display import conditions, one_condition, distributions
from photofitt.utils import power_conversion, numerical_dose
import numpy as np
import os
import pandas as pd
import seaborn as sns
from ast import literal_eval
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

def display_data_from_masks_old(data, plotting_var, output_path, frame_rate=4, roundness=0, graph_format='png',
                            hue="Subcategory-02", hue_order=None, palette=None):
    """
    PLOT THE RESULTS FOR EACH CONDITION SEPARATELY:
    Subcategory-02 filters out the different experimental condition such as control, synch, uv10sec or uv 30sec
    (last level of the folder organisation)
    :param data:
    :param output_path:
    :param frame_rate:
    :param roundness:
    :return:
    """

    density = np.unique(data['Subcategory-01'])
    classes = np.unique(data['Subcategory-02'])
    if palette is None:
        palette = sns.color_palette("husl", 17)

    for d in density:
        print(d)
        data_d = data[data["Subcategory-01"] == d].reset_index(drop=True)
        for c in classes:
            data_c = data_d[data_d["Subcategory-02"] == c].reset_index(drop=True)
            if len(data_c) > 0:
                data_c["unique_name"] = data_c["Subcategory-00"] + data_c["Subcategory-01"] + data_c["Subcategory-02"] + \
                                        data_c["video_name"]
                y_var = f"{plotting_var}"
                name = d + "_" + c + "_" + y_var + "_roundness-{0}.{1}".format(roundness, graph_format)
                one_condition(data_c, y_var, output_path, name, hue1="unique_name", hue2="Subcategory-02",
                              palette=palette, frame_rate=frame_rate)

        ## PLOT ALL THE CONDITIONS FOR EACH DENSITY VALUE
        title = "Minimum roundness {}".format(roundness)
        y_var = f"{plotting_var}"
        name = d + "_" + y_var + "_roundness-{0}.{1}".format(roundness, graph_format)
        conditions(data_d, y_var, title, hue, output_path, name, style="processing", palette=palette,
                   hue_order=hue_order)

        # TEMPORAL DISTRIBUTION OF SIZE
        # --------------------------------------------------------------
        ## Obtain cell size
        data_display = None
        if pd.api.types.is_string_dtype(data_d["cell_size"].dtype):
            data_d["cell_size"] = data_d["cell_size"].apply(literal_eval)

        if pd.api.types.is_string_dtype(data_d["roundness_axis"].dtype):
            data_d["roundness_axis"] = data_d["roundness_axis"].apply(literal_eval)

        for i in range(len(data_d)):
            cell = data_d.iloc[i]
            if cell.cell_size != []:
                CS = cell["cell_size"]
                RA = cell["roundness_axis"]
                t = cell["frame"]
                S0 = cell["Subcategory-01"]  # Density
                S1 = cell["Subcategory-02"]  # Condition
                aux_data = [[t, CS[f], RA[f], S0, S1] for f in range(len(RA)) if RA[f] > roundness]
                col_names = ["frame", "cell_size", "roundness_axis", "Subcategory-00", "Subcategory-01"]
                aux = pd.DataFrame(aux_data, columns=col_names)
                if data_display is None:
                    data_display = aux
                else:
                    data_display = pd.concat([data_display, aux]).reset_index(drop=True)

        # variable = "roundness_axis"
        variable = "cell_size"
        data_display["processing"] = "raw"
        conditions(data_display, variable, "Cell size (pixels)", "Subcategory-01", output_path,
                   d + "_" + variable + "_roundness-{0}.{1}".format(roundness, graph_format),
                   style="processing", palette=palette, hue_order=hue_order)
        groups = np.unique(data_display["Subcategory-01"])
        for g in groups:
            data_g = data_display[data_display["Subcategory-01"] == g]
            # Create the data
            df = pd.DataFrame(dict(variable=data_g[variable], frame=data_g["frame"]))
            distributions(df, "Cell Size (pixels)", g, os.path.join(output_path, d + "_" + g), smoothness=0.3)



def display_data_from_masks(data, plotting_var, output_path, frame_rate=4, roundness=0, graph_format='png',
                            hue="Subcategory-02", hue_order=None, reduced_hue=None, palette=None, time_limit=120, 
                            time_points=None, time_colours=None, xlim=1200, density_ylim=0.00030, common_norm=True):
    """
    PLOT THE RESULTS FOR EACH CONDITION SEPARATELY:
    Subcategory-02 filters out the different experimental condition such as control, synch, uv10sec or uv 30sec
    (last level of the folder organisation)
    :param data:
    :param output_path:
    :param frame_rate:
    :param roundness:
    :return:
    """

    density = np.unique(data['Subcategory-01'])
    classes = np.unique(data['Subcategory-02'])
    if palette is None:
        palette = "coolwarm"

    for d in density:
        print(d)
        data_d = data[data["Subcategory-01"] == d].reset_index(drop=True)
        for c in classes:
            data_c = data_d[data_d["Subcategory-02"] == c].reset_index(drop=True)
            if len(data_c) > 0:
                data_c["unique_name"] = data_c["Subcategory-00"] + data_c["Subcategory-01"] + data_c["Subcategory-02"] + \
                                        data_c["video_name"]
                y_var = f"{plotting_var}"
                name = d + "_" + c + "_" + y_var + "_roundness-{0}.{1}".format(roundness, graph_format)
                #one_condition(data_c, y_var, output_path, name, hue1="unique_name", hue2="Subcategory-02",
                #              palette=palette, frame_rate=frame_rate)

        ## PLOT ALL THE CONDITIONS FOR EACH DENSITY VALUE
        title = "Minimum roundness {}".format(roundness)
        y_var = f"{plotting_var}"
        name = d + "_" + y_var + "_roundness-{0}.{1}".format(roundness, graph_format)
        #conditions(data_d, y_var, title, hue, output_path, name, style="processing", palette=palette,
        #           hue_order=hue_order)

        # TEMPORAL DISTRIBUTION OF SIZE
        # --------------------------------------------------------------
        ## Obtain cell size
        data_display = None
        if pd.api.types.is_string_dtype(data_d["cell_size"].dtype):
            data_d["cell_size"] = data_d["cell_size"].apply(literal_eval)

        if pd.api.types.is_string_dtype(data_d["roundness_axis"].dtype):
            data_d["roundness_axis"] = data_d["roundness_axis"].apply(literal_eval)

        for i in range(len(data_d)):
            cell = data_d.iloc[i]
            if cell.cell_size != []:
                CS = cell["cell_size"]
                RA = cell["roundness_axis"]
                t = cell["frame"]
                S0 = cell["Subcategory-01"]  # Density
                S1 = cell["Subcategory-02"]  # Condition
                aux_data = [[t, CS[f], RA[f], S0, S1] for f in range(len(RA)) if RA[f] > roundness]
                col_names = ["frame", "cell_size", "roundness_axis", "Subcategory-00", "Subcategory-01"]
                aux = pd.DataFrame(aux_data, columns=col_names)
                if data_display is None:
                    data_display = aux
                else:
                    data_display = pd.concat([data_display, aux]).reset_index(drop=True)

        # Estimate the ligth dose
        light_power = 6.255662 # fixed power value according to our microscope
        data_display = numerical_dose(data_display, column_name="Subcategory-01", power=light_power)
        data_display = power_conversion(data_display, dose_column="Light dose", condition_col="Subcategory-01", condition_name="Synchro")
        data_display.to_csv(os.path.join(output_path, f"data_display_cellsize_{d}.csv"))
        variable = "cell_size"
        data_display["processing"] = "raw"
        groups = np.unique(data_display["Light dose cat"])

        # Classify cells according to their size
        data_display["cell-class"]="mother"
        data_display.loc[data_display["cell_size"]<350, "cell-class"]="daughter"
        
        aux = data_display.loc[data_display["frame"]<180]
        aux = aux.reset_index(drop=True)
        fig = plt.figure(figsize=(15, 5))
        #g = sns.swarmplot(data=aux, x='Light dose cat', y="frame", hue="cell-class", order=hue_order)
        g = sns.boxplot(data=aux, x='Light dose cat', y="frame", hue="cell-class",
                          order=hue_order, palette=['#C9C9C9', '#FFA500'], 
                          width=.5, linewidth=0.5, hue_order=["mother", "daughter"])
        plt.tight_layout()
        loc, labels = plt.xticks()
        g.set_xticklabels(labels, rotation=45)
        #plt.yscale('log')
        g.set(ylabel="Time in min")
        fig.savefig(os.path.join(output_path, f"{d}_cellclass_time.{graph_format}"), format=graph_format)
        plt.show()
        
        if reduced_hue is not None:
            fig = plt.figure(figsize=(6, 5))
            g = sns.boxplot(data=aux, x='Light dose cat', y="frame", hue="cell-class",
                              order=reduced_hue, palette=['#C9C9C9', '#FFA500'], 
                              width=.5, linewidth=0.5, hue_order=["mother", "daughter"])
            plt.tight_layout()
            loc, labels = plt.xticks()
            g.set_xticklabels(labels, rotation=45)
            #plt.yscale('log')
            g.set(ylabel="Time in min")
            fig.savefig(os.path.join(output_path, f"{d}_cellclass_time_reduced.{graph_format}"), format=graph_format)
            plt.show()


        if time_points is not None:
            aux = None
            for t in time_points:
                new_data = data_display.loc[lambda data_display: data_display["frame"]==t]
                if aux is None:
                    aux = new_data
                else:
                    aux = pd.concat([aux, new_data]).reset_index(drop=True)
            data_display = aux
            del aux

        
        k=1
        fig = plt.figure(figsize=(25,10))
        for g in hue_order[:-1]:
            data_g = data_display[data_display["Light dose cat"] == g]
            # Create the data
            df = pd.DataFrame(dict(variable=data_g[variable], frame=data_g["frame"]))
            if time_points is None:
                df = df.loc[lambda df: df["frame"]<time_limit]
            plt.subplot(2,7,k)
            ax = sns.kdeplot(
               data=df, x="variable", hue="frame",
               fill=True, common_norm=common_norm, palette=palette,legend=False,
               alpha=.3, linewidth=0,
            )
            plt.xlabel("Cell size")
            plt.tight_layout()
            plt.ylim([0, density_ylim])
            plt.xlim([0, xlim])
            plt.title(g)
            k+=1
            norm = plt.Normalize(df['frame'].min(), df['frame'].max())
            sm = plt.cm.ScalarMappable(cmap=palette, norm=norm)
            sm.set_array([])
        cbar = plt.colorbar(sm, ax = plt.gca())
        fig.savefig(os.path.join(output_path, f"{d}_cellsize.{graph_format}"), format=graph_format)
        plt.show()
        
        if time_colours is not None:
            reduced_palette = time_colours
            series = [(i*(1/(len(time_colours)-1)), time_colours[i]) for i in range(len(time_colours))]
            cmap = matplotlib.colors.LinearSegmentedColormap.from_list('mycolormap', series, N=256)
            matplotlib.cm.register_cmap("mycolormap", cmap)
            norm = plt.Normalize(data_display['frame'].min(), data_display['frame'].max())
            sm = plt.cm.ScalarMappable(cmap="mycolormap", norm=norm)
            sm.set_array([])
        else:
            reduced_palette=palette
            norm = plt.Normalize(data_display['frame'].min(), data_display['frame'].max())
            sm = plt.cm.ScalarMappable(cmap=palette, norm=norm)
            sm.set_array([])
            
            
        if reduced_hue is not None:
            k=1
            fig = plt.figure(figsize=(25,5))
            for g in reduced_hue:
                data_g = data_display[data_display["Light dose cat"] == g]
                # Create the data
                df = pd.DataFrame(dict(variable=data_g[variable], frame=data_g["frame"]))
                if time_points is None:
                    df = df.loc[lambda df: df["frame"]<time_limit]
                plt.subplot(1,len(reduced_hue),k)
                ax = sns.kdeplot(
                   data=df, x="variable", hue="frame",
                   fill=True, common_norm=common_norm, palette=reduced_palette,legend=False,
                   alpha=.5, linewidth=0
                )
                plt.xlabel("Cell size")
                plt.tight_layout()
                plt.title(g)
                plt.ylim([0, density_ylim])
                plt.xlim([0, xlim])
                k+=1
            plt.colorbar(sm, ax = plt.gca())
            fig.savefig(os.path.join(output_path, f"{d}_cellsize_reduced.{graph_format}"), format=graph_format)
            plt.show()
        else:
            k=1
            fig = plt.figure(figsize=(30,5))            
            for g in hue_order[:-7]:
                data_g = data_display[data_display["Light dose cat"] == g]
                # Create the data
                df = pd.DataFrame(dict(variable=data_g[variable], frame=data_g["frame"]))
                df = df.loc[lambda df: df["frame"]<time_limit]
                plt.subplot(1,8,k)
                ax = sns.kdeplot(
                   data=df, x="variable", hue="frame",
                   fill=True, common_norm=common_norm, palette=reduced_palette,legend=False,
                   alpha=.5, linewidth=0,
                )
                plt.xlabel("Cell size")
                plt.tight_layout()
                plt.title(g)
                plt.ylim([0, density_ylim])
                plt.xlim([0, xlim])
                k+=1
            cbar = plt.colorbar(sm, ax = plt.gca())
            fig.savefig(os.path.join(output_path, f"{d}_cellsize_reduced.{graph_format}"), format=graph_format)
            plt.show()


