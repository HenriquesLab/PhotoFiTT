from photofitt.display import conditions, one_condition, distributions, dual_boxplots, cellsize_distributions
from photofitt.utils import power_conversion, numerical_dose
import numpy as np
import os
import pandas as pd
from ast import literal_eval


def display_data_from_masks(data, output_path, roundness=0, graph_format='png',
                            hue_order=None, reduced_hue=None, palette=None, time_limit=120,
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
    if palette is None:
        palette = "coolwarm"

    for d in density:
        print(d)
        data_d = data[data["Subcategory-01"] == d].reset_index(drop=True)

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

        # Classify cells according to their size
        data_display["cell-class"]="mother"
        data_display.loc[data_display["cell_size"]<350, "cell-class"]="daughter"
        
        aux = data_display.loc[data_display["frame"]<180]
        aux = aux.reset_index(drop=True)

        dual_boxplots(aux, output_path, f"{d}_cellclass_time.{graph_format}",
                      x_var='Light dose cat', y_var="frame", hue_var="cell-class", x_order=hue_order,
                      hue_order=["mother", "daughter"],
                      ylabel="Time in min", palette=['#C9C9C9', '#FFA500'], fig_size=(15, 5), graph_format="png")

        if reduced_hue is not None:
            dual_boxplots(aux, output_path, f"{d}_cellclass_time_reduced.{graph_format}",
                          x_var='Light dose cat', y_var="frame", hue_var="cell-class", x_order=reduced_hue,
                          hue_order=["mother", "daughter"],
                          ylabel="Time in min", palette=['#C9C9C9', '#FFA500'], fig_size=(6, 5), graph_format="png")

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

        cellsize_distributions(data_display, output_path, f"{d}_cellsize_reduced.{graph_format}", reduced_hue,
                               variable=variable,
                               xlim=xlim,
                               hue_var="frame",
                               common_norm=common_norm,
                               time_points=None,
                               time_limit=time_limit,
                               x_label="Cell size [px2]",
                               palette=palette,
                               density_ylim=density_ylim,
                               time_colours=time_colours,
                               figsize=(25, 5),
                               graph_format=graph_format)
