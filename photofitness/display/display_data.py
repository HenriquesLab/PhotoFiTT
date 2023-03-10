
from photofitness.display.plots import plot_conditions, plot_one_condition, plot_distributions
import numpy as np
import os
import pandas as pd



def display_data_from_masks(data, output_path, frame_rate=4, roundness=0, graph_format='png', hue_order=None):
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
    for d in density:
        data_d = data[data["Subcategory-01"] == d].reset_index(drop=True)
        for c in classes:
            data_c = data_d[data_d["Subcategory-02"]==c].reset_index(drop=True)
            data_c["unique_name"] = data_c["Subcategory-00"] + data_c["Subcategory-01"] + data_c["Subcategory-02"] +\
                                    data_c["video_name"]

            y_var = "mitosis_normalised"
            name = d + "_" + c + "_" + y_var + "_roundness-{0}.{1}".format(roundness, graph_format)
            plot_one_condition(data_c, y_var, output_path, name, hue1="unique_name", hue2="Subcategory-02",
                               frame_rate=frame_rate, hue_order=hue_order)

            y_var = "mitosis"
            name = d + "_" + c + "_" + y_var + "_roundness-{0}.{1}".format(roundness, graph_format)
            plot_one_condition(data_c, y_var, output_path, name, hue1="unique_name", hue2="Subcategory-02",
                               frame_rate=frame_rate, hue_order=hue_order)

        ## PLOT ALL THE CONDITIONS FOR EACH DENSITY VALUE
        title = "Minimum roundness {}".format(roundness)
        condition = "Subcategory-02"
        y_var = "mitosis"
        name = d + "_" + y_var + "_roundness-{0}.{1}".format(roundness, graph_format)
        plot_conditions(data_d, y_var, title, condition, output_path, name, style_condition="processing", hue_order=hue_order)

        y_var = "mitosis_normalised"
        name = d + "_" + y_var + "_roundness-{0}.{1}".format(roundness, graph_format)
        plot_conditions(data_d, y_var, title, condition, output_path, name, style_condition="processing", hue_order=hue_order)

        # TEMPORAL DISTRIBUTION OF SIZE
        # --------------------------------------------------------------
        ## Obtain cell size
        data_display = None
        for i in range(len(data_d)):
            cell = data_d.iloc[i]
            if cell.cell_size != []:
                CS = cell.cell_size
                RA = cell.roundness_axis
                t = cell.frame
                S0 = cell["Subcategory-01"] # Density
                S1 = cell["Subcategory-02"] # Condition
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
        plot_conditions(data_display, variable, "Cell size (pixels)", "Subcategory-01", output_path,
                        d + "_" + variable + "_roundness-{0}.{1}".format(roundness, graph_format),
                        style_condition="processing", hue_order=hue_order)
        groups = np.unique(data_display["Subcategory-01"])
        for g in groups:
            data_g = data_display[data_display["Subcategory-01"] == g]
            # Create the data
            df = pd.DataFrame(dict(variable=data_g[variable], frame=data_g["frame"]))
            plot_distributions(df, "Cell Size (pixels)", g, os.path.join(output_path, d + "_" + g), smoothness=0.3)
