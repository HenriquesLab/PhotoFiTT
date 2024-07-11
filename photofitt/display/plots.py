import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import os
import pandas as pd
from ast import literal_eval

# Avoid warnings
import warnings
warnings.filterwarnings('ignore')

def smooth_curves(data, y_var, title, output_path, name):
    fig = plt.figure(figsize=(7, 6))
    plt.subplot(2, 1, 1)
    sns.lineplot(x="frame", y=y_var, hue='Subcategory-01', style='Subcategory-02', data=data, palette="tab20",
                 linewidth=1.5, alpha=0.5)
    #plt.legend([])
    # plt.ylabel(y_label)
    # plt.xlabel("Time (min)")
    plt.title(title)

    # Plot the results per category
    ax = plt.subplot(2, 1, 2)
    sns.lineplot(x="frame", y=y_var, hue='Subcategory-00', style='Subcategory-02', data=data, palette="tab20",
                 linewidth=1.5, alpha=0.75)
    # plt.ylabel(y_label)
    plt.xlabel("Time (min)")
    ax.legend(bbox_to_anchor=(0.85, 0.5))
    format_extension = name.split(".")[-1]
    fig.savefig(os.path.join(output_path, name), format=format_extension, transparent=True)
    # plt.show()

def conditions_with_aggregates(data, y_var, title, output_path, name, hue="Subcategory-01", hue_order=None, style="Subcategory-02", ylim = None):
    if hue_order is None:
        hue_order = np.unique(data[hue])
    fig = plt.figure(figsize=(5, 10))
    custom_params = {"axes.spines.right": False, "axes.spines.top": False}
    sns.plotting_context("paper")
    sns.set_theme(style="ticks", rc=custom_params)
    sns.set(font_scale=0.85)
    # plt.rcParams.update({'font.size': 8})
    plt.subplot(2, 1, 1)
    sns.lineplot(x="frame", y=y_var, hue=hue, style=style, data=data, palette=sns.color_palette("husl", 14),
                 hue_order=hue_order, linewidth=1.5, alpha=0.5)
    plt.title(title)

    # Plot the results per category
    ax = plt.subplot(2, 1, 2)
    sns.lineplot(x="frame", y=y_var, style=style, data=data, palette=sns.color_palette("husl", 14),
                 linewidth=1.5, alpha=0.75)
    plt.xlabel("Time (min)")
    if ylim is not None:
        plt.ylim(ylim)
    ax.legend(bbox_to_anchor=(0.85, 0.5))
    plt.tight_layout()
    format_extension = name.split(".")[-1]
    fig.savefig(os.path.join(output_path, name), format=format_extension, transparent=True)
    # plt.show()
    # plt.close(fig)

def conditions(data, y_var, title, condition, output_path, name, style=None,
                    hue_order=None, palette=None, figsize=(7, 4), ylim=None):
    sns.set_style()

    fig = plt.figure(figsize=figsize)

    ## Set style
    custom_params = {"axes.spines.right": False, "axes.spines.top": False}
    sns.plotting_context("paper")
    sns.set(font_scale=0.85)
    sns.set_theme(style="whitegrid", rc=custom_params)

    if palette is None:
        palette = sns.color_palette("husl", 14)

    # Plot the results per category
    if hue_order is None:
        if style is None:
            sns.lineplot(x="frame", y=y_var, hue=condition, data=data,
                         palette=palette, linewidth=1.5, alpha=0.75)
        else:
            sns.lineplot(x="frame", y=y_var, hue=condition, style=style, data=data,
                         palette=palette, linewidth=1.5, alpha=0.75)
    else:
        if style is None:
            sns.lineplot(x="frame", y=y_var, hue=condition, data=data,
                         palette=palette, linewidth=1.5, alpha=0.75, hue_order=hue_order)
        else:
            sns.lineplot(x="frame", y=y_var, hue=condition, style=style, data=data,
                         palette=palette, linewidth=1.5, alpha=0.75, hue_order=hue_order)
    plt.xlabel("Time (min)")
    plt.yscale("linear")
    plt.title(title)
    plt.legend(loc='right')
    if ylim is not None:
        plt.ylim(ylim)
    format_extension = name.split(".")[-1]
    fig.savefig(os.path.join(output_path, name), format=format_extension, transparent=True)
    # plt.show()

def one_condition(data, y_var, output_path, name, hue1="unique_name", hue2 = "Subcategory-02", frame_rate=10,
                  palette=None):

    if palette is None:
        palette = sns.color_palette("husl", 14)

    fig = plt.figure(figsize=(6, 6))
    plt.subplot(3, 1, 1)
    sns.lineplot(x="frame", y=y_var, hue=hue1, data=data[data["processing"] == "Raw"],
                 palette=palette, linewidth=1, alpha=0.5)
    plt.legend([])
    plt.title("Raw data")

    plt.subplot(3, 1, 2)
    sns.lineplot(x="frame", y=y_var, hue=hue1, data=data[data["processing"] == "Averaged-kernel5"],
                 palette=palette, linewidth=1.5, alpha=0.5)
    plt.legend([])
    plt.title("Smooth curves")

    # Plot the results per category
    ax = plt.subplot(3, 1, 3)
    sns.lineplot(x="frame", y=y_var, hue=hue2, style="processing", 
                 data=data[np.mod(data.frame, frame_rate) == 0].reset_index(drop=True),
                 palette=palette, linewidth=1, alpha=0.75)
    plt.xlabel("Time (min)")
    ax.legend(bbox_to_anchor=(0.85, 0.5))
    plt.tight_layout()
    format_extension = name.split(".")[-1]
    fig.savefig(os.path.join(output_path, name), format=format_extension)
    # plt.show()

def dual_boxplots(data,output_path, file_name, x_var='Light dose cat',
                  y_var="frame", hue_var=None, x_order=None,
                  hue_order=None,
                  ylabel="Time in min",
                  xlabel="Light dise",
                  palette=None, figsize=(15,5),
                  graph_format="png"):

    fig = plt.figure(figsize=figsize)
    g = sns.boxplot(data=data, x=x_var, y=y_var, hue=hue_var,
                    order=x_order, palette=palette,
                    width=.5, linewidth=0.5, hue_order=hue_order)
    plt.tight_layout()
    loc, labels = plt.xticks()
    g.set_xticklabels(labels, rotation=45)
    g.set(ylabel=ylabel, xlabel=xlabel)
    fig.savefig(os.path.join(output_path, file_name), format=graph_format)


def vertical_distributions(data, y_var, output_path, name,  hue_order, raw="Subcategory-02", hue="Subcategory-02",
                           palette=None, aspect=9, height=0.6, hspace=-0.02, ylabel="Cells", xlabel="Frame (min)",
                           xticks=[0, 25, 50, 100, 150, 200, 300], xlim=[0, 360]):

    ordered_dataset = None
    for h in hue_order:
        aux = data[data[hue] == h].reset_index(drop=True)
        if ordered_dataset is None:
            ordered_dataset = aux
        else:
            ordered_dataset = pd.concat([ordered_dataset, aux])

    if palette is None:
        palette = sns.color_palette("husl", len(hue_order))

    # Initialize the FacetGrid object
    g = sns.FacetGrid(ordered_dataset, row=raw, hue=hue, aspect=aspect, height=height, palette=palette,
                      hue_order=hue_order, sharex=True)

    # Draw the densities in a few steps
    g.map(sns.lineplot, "frame", y_var, hue_order=hue_order, alpha=1, linewidth=2, errorbar="sd")

    # passing color=None to refline() uses the hue mapping
    # g.refline(y=0, linewidth=0.5, linestyle="-", color=None, clip_on=True)

    # Define and use a simple function to label the plot in axes coordinates
    def label(x, color, label):
        ax = plt.gca()
        ax.text(1, 0, label, fontweight="bold", color="k", ha="left", va="center", transform=ax.transAxes)
    g.map(label, y_var)
    # Set the subplots to overlap
    g.figure.subplots_adjust(hspace=hspace)
    # Remove axes details that don't play well with overlap
    g.set_titles("")
    g.set(ylabel=ylabel, xlabel=xlabel, xticks=xticks, xlim=xlim)
    g.despine(bottom=True, left=True)

    ## Set style
    custom_params = {"axes.spines.right": False, "axes.spines.top": False}
    sns.plotting_context("paper")
    sns.set(font_scale=1)
    sns.set_theme(style="whitegrid", rc=custom_params)

    format_extension = name.split(".")[-1]
    g.savefig(os.path.join(output_path, name), format=format_extension, transparent=True, dpi=300)

def violinplots_horizontal(data, y_var, x_var, output_path, name,  hue_order, palette=None, bw=.5, orient="h",
                           ylabel="Exposure time to UV radiation", width=0.7, linewidth=0.5, pad_y=-6):
    if palette is None:
        palette = sns.color_palette("husl", len(hue_order))

    f, ax = plt.subplots(figsize=(4, 5), constrained_layout=True)

    ax.yaxis.set_tick_params(pad=pad_y)
    sns.violinplot(data=data, palette=palette, inner="points", order=hue_order, hue_order=hue_order, bw=bw,
                   orient=orient, y=y_var, x=x_var, width=width, linewidth=linewidth)

    # Tweak the visual presentation
    ax.xaxis.grid(True, color="gray")

    ax.set(ylabel=ylabel)
    ax.set(xlabel=x_var)
    sns.despine(trim=True, left=True)

    ## Set style
    custom_params = {"axes.spines.right": False, "axes.spines.top": False}
    sns.plotting_context("paper")
    sns.set(font_scale=1)
    sns.set_theme(style="whitegrid", rc=custom_params)

    format_extension = name.split(".")[-1]
    f.savefig(os.path.join(output_path, name), format=format_extension, transparent=True, dpi=300)

def regressionfit(data, y_var, x_var, output_path, name, palette=None, spline_order=2, hue=None, hue_order=None,
                  height=4, aspect=1):

    if palette is None:
        if hue_order is None:
            palette = sns.color_palette("husl", 14)
        else:
            palette = sns.color_palette("husl", len(hue_order))
    if hue is not None:
        if hue_order is not None:
            f = sns.catplot(
                data=data, x=x_var, y=y_var,
                hue=hue, hue_order=hue_order, palette=palette,
                native_scale=True, height=height, aspect=aspect
            )
        else:
            f = sns.catplot(
                data=data, x=x_var, y=y_var,
                hue=hue, palette=palette,
                native_scale=True, height=height, aspect=aspect
            )
    else:
        f = sns.catplot(
            data=data, x=x_var, y=y_var, palette=palette,
            native_scale=True, height=height, aspect=aspect
        )

    sns.regplot(data=data, x=x_var, y=y_var, scatter=False, truncate=True, order=spline_order, color="grey")

    ## Set style
    custom_params = {"axes.spines.right": False, "axes.spines.top": False}
    sns.plotting_context("paper")
    sns.set(font_scale=1)
    sns.set_theme(style="whitegrid", rc=custom_params)

    format_extension = name.split(".")[-1]
    f.savefig(os.path.join(output_path, name), format=format_extension, transparent=True, dpi=300)

def cellsize_distributions(data, output_path, file_name, hue_order,condition_var="Subcategory-02",
                           variable = "cell_size", xlim=1200,
                           hue_var="frame", common_norm=True,
                           time_points=[32, 60, 92, 120], time_limit = 120,
                           x_label="Cell size [px2]", palette="coolwarm",
                           density_ylim=0.001, time_colours= ["#BC77F8", "#99E3D7", "#FC9F30", "#FF4126"],
                           figsize=(25, 5), graph_format="png"):

    if time_colours is not None:
        reduced_palette = time_colours
        series = [(i * (1 / (len(time_colours) - 1)), time_colours[i]) for i in range(len(time_colours))]
        cmap = matplotlib.colors.LinearSegmentedColormap.from_list('mycolormap', series, N=256)
        matplotlib.cm.register_cmap("mycolormap", cmap)
        norm = plt.Normalize(data['frame'].min(), data['frame'].max())
        sm = plt.cm.ScalarMappable(cmap="mycolormap", norm=norm)
        sm.set_array([])
    else:
        reduced_palette = palette
        norm = plt.Normalize(data['frame'].min(), data['frame'].max())
        sm = plt.cm.ScalarMappable(cmap=palette, norm=norm)
        sm.set_array([])

    k = 1
    fig = plt.figure(figsize=figsize)
    for g in hue_order:
        data_g = data[data[condition_var] == g]
        # Create the data
        df = pd.DataFrame(dict(variable=data_g[variable], frame=data_g["frame"]))
        if time_points is None:
            df = df.loc[lambda df: df["frame"] < time_limit]
        plt.subplot(1, len(hue_order), k)
        ax = sns.kdeplot(
            data=df, x="variable", hue=hue_var,
            fill=True, common_norm=common_norm, palette=reduced_palette, legend=False,
            alpha=.5, linewidth=0
        )
        plt.xlabel(x_label)
        plt.tight_layout()
        plt.title(g)
        plt.ylim([0, density_ylim])
        plt.xlim([0, xlim])
        k += 1
    plt.colorbar(sm, ax=plt.gca())
    fig.savefig(os.path.join(output_path, file_name), format=graph_format)



def distributions(df, xlabel, title, output_path, smoothness=.5):
    sns.set_theme(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})
    # Initialize the FacetGrid object
    # pal = sns.cubehelix_palette(len(np.unique(df["frame"])), rot=-.25, light=.7)
    pal = sns.cubehelix_palette(len(np.unique(df["frame"])), start=2.5, rot=0, light=.6, dark=.2)
    g = sns.FacetGrid(df, row="frame", hue="frame", aspect=6, height=.5, palette="coolwarm", xlim=[0, 700])
    # Draw the densities in a few steps
    g.map(sns.kdeplot, "variable",
          bw_adjust=smoothness, clip_on=False,
          fill=True, alpha=1, linewidth=1.5)
    g.map(sns.kdeplot, "variable", clip_on=False, color="w", lw=2, bw_adjust=smoothness)
    # passing color=None to refline() uses the hue mapping
    g.refline(y=0, linewidth=2, linestyle="-", color=None, clip_on=False)

    # Define and use a simple function to label the plot in axes coordinates
    def label(x, color, label):
        ax = plt.gca()
        ax.text(0, .2, label, fontweight="bold", color=color,
                ha="left", va="center", transform=ax.transAxes)
    g.map(label, "variable")
    # Set the subplots to overlap
    g.figure.subplots_adjust(hspace=-.25)
    # Remove axes details that don't play well with overlap
    g.set_titles("")
    g.set(yticks=[], ylabel="")
    g.set(xlabel=xlabel, xlim=[0,700])
    g.despine(bottom=True, left=True)
    g.savefig("{}_facegrid.png".format(output_path))
    g.savefig("{}_facegrid.svg".format(output_path))

    fig = plt.figure()
    sns.set_theme(style="white", rc={"axes.facecolor": (1, 1, 1, 0)})
    sns.histplot(
        data=df, x="variable", hue="frame", stat="proportion",
        fill=True, palette="coolwarm", kde=True,
        alpha=.5, linewidth=0, binwidth=50, binrange=(0, 1000),
    )
    plt.xlabel(xlabel)
    plt.xlim([0,700])
    plt.title(title)
    fig.savefig("{}_histogram.png".format(output_path), format='png')
    fig.savefig("{}_histogram.svg".format(output_path), format='svg')
    # plt.show()

def mitosis(data, output_path, hue_order, y_variable, hue="Subcategory-02", graph_format='png',figsize=(7, 4)):

    fig = plt.figure(figsize=figsize)
    plt.rcParams.update({'font.size': 0.9})
    sns.lineplot(x="frame", y=y_variable, hue=hue, data=data,
                 palette=sns.color_palette("husl", 14),
                 hue_order=hue_order, linewidth=1.5, alpha=1)
    plt.tight_layout()
    plt.title("{0} along time".format(y_variable))
    fig.savefig(os.path.join(output_path, "data_{0}_counting.{1}".format(y_variable, graph_format)), format=graph_format,
                transparent=True)

    for d in np.unique(data["Subcategory-00"]):
        data_folderwise = data[data["Subcategory-00"] == d].reset_index(drop=True)
        fig = plt.figure(figsize=(10, 8))
        plt.rcParams.update({'font.size': 0.9})
        sns.lineplot(x="frame", y=y_variable, hue=hue, data=data_folderwise,
                     palette=sns.color_palette("husl", 14),
                     hue_order=hue_order, linewidth=1.5, alpha=1)
        plt.tight_layout()
        plt.title("{0} - {1} along time".format(y_variable, d))
        fig.savefig(os.path.join(output_path, "data_{0}_counting_{1}.{2}".format(y_variable, d, graph_format)), format=graph_format,
                    transparent=False)
        
def info_wrt_peak(data, x, x_labels, hue_order, output_path):

    # PEAK TIME
    # fig = plt.figure()
    sns.set(font_scale=0.9)
    g = sns.catplot(data=data, x=x, y="peak_time", hue="Subcategory-00",
                    order=x_labels, hue_order=hue_order, kind="box", height=5,
                    aspect=2, palette="rainbow"
                    )
    g.set_axis_labels("Exposure times", "Time point of maximum peak")
    g.despine(left=True)
    # plt.ylim([-50, 190])
    # plt.yscale("log")
    g.savefig(os.path.join(output_path, "peak_folderwise.png"), format='png')
    # plt.show()

    #
    # fig = plt.figure()
    sns.set(font_scale=0.9)
    g = sns.catplot(data=data, x=x, y="peak_time",
                    order=x_labels, kind="box", height=5, aspect=2, palette="rainbow_r"
                    )
    g.set_axis_labels("Exposure times", "Time point of maximum peak (minutes)")
    g.despine(left=True)
    # plt.ylim([-50, 190])
    # plt.yscale("log")
    g.savefig(os.path.join(output_path, "peak.png"), format='png')
    # plt.show()

    # DELAY W.R.T. SYNCHRO
    # fig = plt.figure()
    sns.set(font_scale=0.9)
    g = sns.catplot(data=data, x=x, y="delay_synchro", hue="Subcategory-00",
                    order=x_labels, hue_order=hue_order, kind="box", height=5, aspect=2, palette="rainbow"
                    )
    g.set_axis_labels("Exposure times", "Delay for the maximum peak (minutes)")
    g.despine(left=True)
    # plt.ylim([-50, 190])
    # plt.yscale("log")
    g.savefig(os.path.join(output_path, "delay_folderwise.png"), format='png')
    # plt.show()
    #
    # fig = plt.figure()
    sns.set(font_scale=0.9)
    g = sns.catplot(data=data, x=x, y="delay_synchro",
                    order=x_labels, kind="box", height=5, aspect=2, palette="rainbow_r"
                    )
    g.set_axis_labels("Exposure times", "Delay for the maximum peak (minutes)")
    g.despine(left=True)
    # plt.ylim([-50, 190])
    # plt.yscale("log")
    g.savefig(os.path.join(output_path, "delay_folderwise.png"), format='png')
    # plt.show()
    #
    # PROPORTIONAL DELAY W.R.T. SYNCHRO
    # fig = plt.figure()
    sns.set(font_scale=0.9)
    g = sns.catplot(data=data, x=x, y="proportional_delay_synchro", hue="Subcategory-00",
                    order=x_labels, hue_order=hue_order, kind="box", height=5, aspect=2, palette="rainbow"
                    )
    g.set_axis_labels("Exposure times", "Delay proportion for the maximum peak (minutes)")
    g.despine(left=True)
    # plt.yscale("log")
    g.savefig(os.path.join(output_path, "proportional_delay_folderwise.png"), format='png')
    # plt.show()
    #
    # fig = plt.figure()
    sns.set(font_scale=0.9)
    g = sns.catplot(data=data, x=x, y="proportional_delay_synchro",
                    order=x_labels, kind="box", height=5, aspect=2, palette="rainbow_r"
                    )
    g.set_axis_labels("Exposure times", "Delay proportion for the maximum peak (minutes)")
    g.despine(left=True)
    # plt.yscale("log")
    g.savefig(os.path.join(output_path, "proportional_delay.png"), format='png')


def size_change_wrt_peak(data, x_labels, y_variable, hue_order, output_path, y_lim=[0, 300], graph_format='png'):
    sns.set(font_scale=0.9)
    g = sns.catplot(data=data, x="Subcategory-02", y=y_variable, kind="box",
                    order=x_labels, height=5, aspect=2, palette="rainbow"
                    )
    g.set_axis_labels("Exposure times", "{}".format(y_variable))
    g.despine(left=True)
    plt.ylim(y_lim)
    # plt.yscale("log")
    g.savefig(os.path.join(output_path, "mitosis_time.{}".format(graph_format)), format=graph_format)
    # plt.show()

    sns.set(font_scale=0.9)
    g = sns.catplot(data=data, x="Subcategory-02", y=y_variable, hue="Subcategory-00",
                    order=x_labels, hue_order=hue_order, height=5, aspect=2, palette="rainbow"
                    )
    g.set_axis_labels("Exposure times", "{}".format(y_variable))
    g.despine(left=True)
    plt.ylim(y_lim)
    # plt.yscale("log")
    g.savefig(os.path.join(output_path, "mitosis_time_folderwise.{}".format(graph_format)), format=graph_format)
    # plt.show()


def unsynchro_tracking(data, condition_var, output_dir, hue_order, palette_colours=None):
    if palette_colours is None:
        palette_colours = ['#C9C9C9', '#FC9F30', '#99E3D7', '#BC77F8']

    fig = plt.figure(figsize=(8, 9))
    sns.set(font_scale=0.9)
    sns.set_theme(style="white")

    plt.subplot(3, 2, 1)
    g = sns.barplot(
        data[data["Division"] == True], y=condition_var, x="Mitosis duration",
        palette=palette_colours, orient="h",
        order=hue_order, errorbar=("ci", 95), capsize=.08
    )
    plt.tight_layout()
    loc, labels = plt.xticks()
    g.set_xticklabels(labels, rotation=45)
    plt.title("Time in mitosis for dividing cells")

    # --
    plt.subplot(3, 2, 2)
    g = sns.barplot(
        data[data["Division"] == False], y=condition_var, x="Mitosis duration",
        palette=palette_colours, orient="h",
        order=hue_order, errorbar=("ci", 95), capsize=.08
    )
    plt.tight_layout()
    loc, labels = plt.xticks()
    g.set_xticklabels(labels, rotation=45)
    plt.title("Time in mitosis for non-dividing cells")
    # --
    plt.subplot(3, 2, 3)
    # Draw a categorical scatterplot to show each observation
    g = sns.swarmplot(data=data, y=condition_var, x="Mitosis duration", orient="h",
                      hue="Division", palette=['#94C9DF', '#FFA500'], order=hue_order)
    plt.tight_layout()
    loc, labels = plt.xticks()
    g.set_xticklabels(labels, rotation=45)

    # --
    plt.subplot(3, 2, 4)
    # Draw a categorical scatterplot to show each observation
    g = sns.swarmplot(data=data, y=condition_var, x="Mitosis duration", orient="h",
                      hue="Division", palette=['#94C9DF', '#FFA500'], order=hue_order)
    plt.tight_layout()
    loc, labels = plt.xticks()
    g.set_xticklabels(labels, rotation=45)
    plt.yscale('log')
    g.set(ylabel="Mitosis duration (log)")
    # --
    plt.subplot(3, 2, 5)

    g = sns.countplot(data, x=condition_var, hue="Division",
                      palette=['#94C9DF', '#FFA500'], order=hue_order)
    plt.tight_layout()
    loc, labels = plt.xticks()
    g.set_xticklabels(labels, rotation=45)

    #
    plt.subplot(3, 2, 6)
    g = sns.barplot(
        data[data["Division"] == True], y=condition_var, x="Division timepoint",
        palette=palette_colours, orient="h",
        order=hue_order, errorbar=("ci", 95), capsize=.08
    )
    plt.tight_layout()
    loc, labels = plt.xticks()
    g.set_xticklabels(labels, rotation=45)
    fig.savefig(os.path.join(output_dir, "mitoses_delays.pdf"), format="pdf", transparent=True)
    fig.savefig(os.path.join(output_dir, "mitoses_delays.png"), format="png", transparent=True)
    plt.show()

def cell_size_dynamics(data, output_path,
                        condition_var="Subcategory-02",
                        x_label = "Light dose [J/cm2]",
                        roundness=0, graph_format='png',
                          hue_order=None,
                          reduced_hue=None,
                          palette="coolwarm",
                          time_limit=120,
                          time_points=None,
                          time_colours=["#BC77F8", "#99E3D7", "#FC9F30", "#FF4126"],
                          xlim=1200,
                          density_ylim=0.00030,
                          common_norm=False,
                          orient="h",
                          pixel_size=0.8633995):
    """
    PLOT THE RESULTS FOR EACH CONDITION SEPARATELY:
    Subcategory-02 filters out the different experimental condition such as control, synch, uv10sec or uv 30sec
    (last level of the folder organisation)
    :param graph_format:
    :param data:
    :param output_path:
    :param frame_rate:
    :param roundness:
    :return:
    """

    density = np.unique(data['Subcategory-01'])

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
                S0 = cell["Subcategory-00"]  # Density
                S1 = cell["Subcategory-01"]  # Condition
                S2 = cell["Subcategory-02"]
                if not condition_var.__contains__("Subcategory"):
                    V = cell[condition_var]
                    aux_data = [[t, CS[f], RA[f], S0, S1, S2, V] for f in range(len(RA)) if RA[f] > roundness]
                    col_names = ["frame", "cell_size", "roundness_axis", "Subcategory-00", "Subcategory-01",
                                 "Subcategory-02", condition_var]
                else:
                    aux_data = [[t, CS[f], RA[f], S0, S1, S2] for f in range(len(RA)) if RA[f] > roundness]
                    col_names = ["frame", "cell_size", "roundness_axis", "Subcategory-00", "Subcategory-01", "Subcategory-02"]
                aux = pd.DataFrame(aux_data, columns=col_names)
                if data_display is None:
                    data_display = aux
                else:
                    data_display = pd.concat([data_display, aux]).reset_index(drop=True)

        # Estimate the ligth dose
        # light_power = 6.255662  # fixed power value according to our microscope
        # data_display = numerical_dose(data_display, column_name="Subcategory-01", power=light_power)
        # data_display = power_conversion(data_display, dose_column="Light dose", condition_col="Subcategory-01",
        #                                 condition_name="Synchro")
        data_display["diameter [um]"] = 2 * (np.sqrt(data_display["cell_size"] / np.pi)) * pixel_size
        variable = "diameter [um]"


        # Classify cells according to their size
        data_display["cell-class"] = "mother"
        data_display.loc[data_display["cell_size"] < 350, "cell-class"] = "daughter"
        data_display.to_csv(os.path.join(output_path, f"data_display_cellsize_{d}.csv"))
        aux = data_display.loc[data_display["frame"] < 180]
        aux = aux.reset_index(drop=True)

        if orient=="v":
            x_var = condition_var
            y_var = "frame"
            ylabel = "Time [min]"
            xlabel = x_label
            figsize = (7, 5)
        else:
            y_var = condition_var
            x_var = "frame"
            ylabel = x_label
            xlabel = "Time [min]"
            figsize = (5, 7)

        dual_boxplots(aux, output_path, f"{d}_cellclass_time.{graph_format}",
                      x_var=x_var, y_var=y_var, hue_var="cell-class", x_order=hue_order,
                      hue_order=["mother", "daughter"],
                      ylabel=ylabel, xlabel=xlabel, palette=['#C9C9C9', '#FFA500'], figsize=figsize, graph_format=graph_format)

        if reduced_hue is not None:
            dual_boxplots(aux, output_path, f"{d}_cellclass_time_reduced.{graph_format}",
                          x_var=x_var, y_var=y_var, hue_var="cell-class", x_order=reduced_hue,
                          hue_order=["mother", "daughter"],
                          ylabel=ylabel, xlabel=xlabel, palette=['#C9C9C9', '#FFA500'], figsize=figsize, graph_format=graph_format)

        if time_points is not None:
            aux = None
            for t in time_points:
                new_data = data_display.loc[lambda data_display: data_display["frame"] == t]
                if aux is None:
                    aux = new_data
                else:
                    aux = pd.concat([aux, new_data]).reset_index(drop=True)
            data_display = aux
            del aux

        cellsize_distributions(data_display, output_path, f"{d}_cellsize_reduced.{graph_format}", reduced_hue,
                               condition_var=condition_var,
                               variable=variable,
                               xlim=xlim,
                               hue_var="frame",
                               common_norm=common_norm,
                               time_points=time_points,
                               time_limit=time_limit,
                               x_label="Cell diameter [um]",
                               palette=palette,
                               density_ylim=density_ylim,
                               time_colours=time_colours,
                               figsize=(25, 5),
                               graph_format=graph_format)