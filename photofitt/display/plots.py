import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
import pandas as pd
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

def conditions_with_aggregates(data, y_var, title, output_path, name, hue="Subcategory-01", style="Subcategory-02"):
    fig = plt.figure(figsize=(5, 10))
    custom_params = {"axes.spines.right": False, "axes.spines.top": False}
    sns.plotting_context("paper")
    sns.set_theme(style="ticks", rc=custom_params)
    sns.set(font_scale=0.85)
    # plt.rcParams.update({'font.size': 8})
    plt.subplot(2, 1, 1)
    sns.lineplot(x="frame", y=y_var, hue=hue, style=style, data=data, palette=sns.color_palette("husl", 14),
                 linewidth=1.5, alpha=0.5)
    plt.title(title)

    # Plot the results per category
    ax = plt.subplot(2, 1, 2)
    sns.lineplot(x="frame", y=y_var, style=style, data=data, palette=sns.color_palette("husl", 14),
                 linewidth=1.5, alpha=0.75)
    plt.xlabel("Time (min)")
    ax.legend(bbox_to_anchor=(0.85, 0.5))
    plt.tight_layout()
    format_extension = name.split(".")[-1]
    fig.savefig(os.path.join(output_path, name), format=format_extension, transparent=True)
    # plt.show()
    # plt.close(fig)

def conditions(data, y_var, title, condition, output_path, name, style=None,
                    hue_order=None, palette=None, figsize=(7, 4)):
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
    format_extension = name.split(".")[-1]
    fig.savefig(os.path.join(output_path, name), format=format_extension, transparent=True)
    # plt.show()

def one_condition(data, y_var, output_path, name, hue1="unique_name", hue2 = "Subcategory-02", frame_rate=10):
    fig = plt.figure(figsize=(6, 6))
    plt.subplot(3, 1, 1)
    sns.lineplot(x="frame", y=y_var, hue=hue1, data=data[data["processing"] == "Raw"],
                 linewidth=1, alpha=0.5)
    plt.legend([])
    plt.title("Raw data")

    plt.subplot(3, 1, 2)
    sns.lineplot(x="frame", y=y_var, hue=hue1, data=data[data["processing"] == "Averaged-kernel5"],
                 linewidth=1.5, alpha=0.5)
    plt.legend([])
    plt.title("Smooth curves")

    # Plot the results per category
    ax = plt.subplot(3, 1, 3)
    sns.lineplot(x="frame", y=y_var, hue=hue2, style="processing", 
                 data=data[np.mod(data.frame, frame_rate) == 0].reset_index(drop=True),
                 linewidth=1, alpha=0.75)
    plt.xlabel("Time (min)")
    ax.legend(bbox_to_anchor=(0.85, 0.5))
    plt.tight_layout()
    format_extension = name.split(".")[-1]
    fig.savefig(os.path.join(output_path, name), format=format_extension)
    # plt.show()

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
    # g.map(sns.histplot, "variable",
    #       kde=True, clip_on=False, stat="density",
    #       fill=True, alpha=1, linewidth=1.5,
    #       binwidth=50, binrange=(0, 1000))
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

def mitosis(data, output_path, hue_order, y_variable, graph_format='png'):

    fig = plt.figure(figsize=(10, 8))
    plt.rcParams.update({'font.size': 0.9})
    sns.lineplot(x="frame", y=y_variable, hue="Subcategory-02", data=data,
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
        sns.lineplot(x="frame", y=y_variable, hue="Subcategory-02", data=data_folderwise,
                     palette=sns.color_palette("husl", 14),
                     hue_order=hue_order, linewidth=1.5, alpha=1)
        plt.tight_layout()
        plt.title("{0} - {1} along time".format(y_variable, d))
        fig.savefig(os.path.join(output_path, "data_{0}_counting_{1}.{2}".format(y_variable, d, graph_format)), format=graph_format,
                    transparent=False)

def info_wrt_peak(data, x_labels, hue_order, output_path):

    # PEAK TIME
    # fig = plt.figure()
    sns.set(font_scale=0.9)
    g = sns.catplot(data=data, x="Subcategory-02", y="peak_time", hue="Subcategory-00",
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
    g = sns.catplot(data=data, x="Subcategory-02", y="peak_time",
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
    g = sns.catplot(data=data, x="Subcategory-02", y="delay_synchro", hue="Subcategory-00",
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
    g = sns.catplot(data=data, x="Subcategory-02", y="delay_synchro",
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
    g = sns.catplot(data=data, x="Subcategory-02", y="proportional_delay_synchro", hue="Subcategory-00",
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
    g = sns.catplot(data=data, x="Subcategory-02", y="proportional_delay_synchro",
                    order=x_labels, kind="box", height=5, aspect=2, palette="rainbow_r"
                    )
    g.set_axis_labels("Exposure times", "Delay proportion for the maximum peak (minutes)")
    g.despine(left=True)
    # plt.yscale("log")
    g.savefig(os.path.join(output_path, "proportional_delay.png"), format='png')
    # plt.show()

    # # PLOTS WITH INDIVIDUAL POINTS
    # ### points
    # plt.figure(figsize=(10, 5))
    # sns.set(font_scale=1)
    # g = sns.swarmplot(data=data, x="Subcategory-02", y="ratio", hue="Subcategory-02",
    #                   order=x_labels, palette="dark",
    #                   legend=None)
    # plt.ylim([0.1, 50])
    # plt.yscale("log")
    # plt.tight_layout()
    # plt.show()
    #
    # plt.figure(figsize=(10, 5))
    # sns.set(font_scale=0.9)
    # g = sns.catplot(data=data, x="Subcategory-02", y="alpha", hue="Subcategory-00",
    #                 order=x_labels, height=5, aspect=2)
    # g.set_axis_labels("Exposure times", "Alpha")
    # g.despine(left=True)
    # plt.ylim([0.00001, 0.1])
    # plt.yscale("log")
    # plt.show()
    #
    # plt.figure(figsize=(10, 5))
    # sns.set(font_scale=0.9)
    # g = sns.catplot(data=data, x="Subcategory-02", y="beta", hue="Subcategory-00",
    #                 order=x_labels, height=5, aspect=2)
    # g.set_axis_labels("Exposure times", "Beta")
    # g.despine(left=True)
    # plt.ylim([0.00001, 0.1])
    # plt.yscale("log")
    # plt.show()
    #
    # plt.figure(figsize=(10, 5))
    # sns.set(font_scale=0.9)
    # g = sns.catplot(data=data, x="Subcategory-02", y="ratio", hue="Subcategory-00",
    #                 order=x_labels, height=5, aspect=2)
    # g.set_axis_labels("Exposure times", "Ratio = alpha / beta")
    # g.despine(left=True)
    # plt.ylim([0.1, 50])
    # plt.yscale("log")
    # plt.show()
    ### BARS
    # plt.figure()
    # g = sns.catplot(
    #     data=data, x="Subcategory-02", y="ratio", hue="Subcategory-00", order=x_labels, kind="bar",
    #     height=4, aspect=3)
    # g.set_axis_labels("", "Ratio = alpha / beta")
    # # g.set_xticklabels()
    # g.despine(left=True)
    # # plt.ylim([0,10])
    # plt.yscale("log")
    # sns.set(font_scale=1)
    # plt.show()
    #
    # ### BARS COLUMNS
    # # conditions = ['Control-sync', 'Synchro', 'UV50ms', 'UV100ms', 'UV200ms', 'UV400ms', 'UV800ms', 'UV1000ms']
    # plt.figure()
    # sns.set(font_scale=0.8)
    # g = sns.catplot(
    #     data=data, x="Subcategory-02", y="ratio", col="Subcategory-00", order=x_labels,
    #     kind="bar", height=5, aspect=2,
    # )
    # g.set_axis_labels("", "Ratio = alpha / beta")
    # # g.set_xticklabels()
    # g.despine(left=True)
    # # plt.ylim([0,10])
    # plt.yscale("log")
    # plt.show()

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
