from photofitt.display import conditions, one_condition, distributions
import numpy as np
import os
import pandas as pd
import seaborn as sns
from ast import literal_eval


def display_data_from_masks(data, plotting_var, output_path, frame_rate=4, roundness=0, graph_format='png',
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