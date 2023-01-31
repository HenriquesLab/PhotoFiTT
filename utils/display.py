import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
from skimage.measure import regionprops
from tifffile import imread, imsave
from utils.morphology import roundnessCalculator

def plot_smooth_curves(data, y_var, title, output_path, name):
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
    fig.savefig(os.path.join(output_path, name), format='png', transparent=True)
    # plt.show()

def plot_conditions_with_aggregates(data, y_var, title, output_path, name, hue="Subcategory-01", style="Subcategory-02"):
    fig = plt.figure(figsize=(5, 10))
    plt.rcParams.update({'font.size': 8})
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
    fig.savefig(os.path.join(output_path, name), format='png', transparent=True)
    # plt.show()
    # plt.close(fig)

def plot_conditions(data, y_var, title, condition, output_path, name, style_condition="processing", hue_order=None):
    fig = plt.figure(figsize=(12, 8))
    # Plot the results per category
    sns.set(font_scale=0.9)
    if hue_order is None:
        sns.lineplot(x="frame", y=y_var, hue=condition, style=style_condition, data=data,
                     palette=sns.color_palette("husl", 14), linewidth=1.5, alpha=0.75)
    else:
        sns.lineplot(x="frame", y=y_var, hue=condition, style=style_condition, data=data,
                     palette=sns.color_palette("husl", 14), linewidth=1.5, alpha=0.75, hue_order=hue_order)
    # plt.ylabel(y_label)
    plt.xlabel("Time (min)")
    plt.title(title)
    # plt.legend(bbox_to_anchor=(0.85, 0.5))
    fig.savefig(os.path.join(output_path, name), format='png', transparent=True)
    # plt.show()

def plot_one_condition(data, y_var, output_path, name, hue1="unique_name", hue2 = "Subcategory-02", frame_rate=10):
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
    fig.savefig(os.path.join(output_path, name), format='png')
    # plt.show()

def mosaic(stack_im, path2original, min_roundness=0.5):
    """
    :param stack_im: instance mask image.
    :param path2original: path to the original image. stack_im is the instance mask of the original image.
    :param min_roundness: not used yet. It could serve to filter out unrounded objects.
    :return: mosaic image
    """
    BBOX = []
    max_cell = 0
    # Store the bounding box information for each detected cell in the image. We need to know beforehand what's the
    # maximum number of cells detected on each frame so we can calculate the optimal size of the mosaic.
    for t in range(len(stack_im)):
        labels = np.unique(stack_im[t])
        total = 0
        for l in labels:
            if l > 0:
                cell = (stack_im[t] == l).astype(np.uint8)
                if np.sum(cell) > 0:
                    if roundnessCalculator(cell, projected=False) > min_roundness:
                        props = regionprops(cell)
                        cell_info = [t] + [i for i in props[0].bbox]
                        cell_info = cell_info + [cell_info[3] - cell_info[1],
                                                 cell_info[4] - cell_info[
                                                     2]]  # [t, min row, min col, max row, max col, height, width]
                        BBOX.append(cell_info)
                        total += 1
        max_cell = np.max((max_cell, total))
    if len(BBOX) > 0:
        BBOX = np.array(BBOX)
        if len(BBOX.shape) == 1:
            BBOX = np.expand_dims(BBOX, axis=0)
        # Try to make a squared mosaic with same number of cells in rows and columns
        count_x = int(np.floor(np.sqrt(max_cell))) + 1
        count_y = int(np.ceil(max_cell / count_x))
        H = int(np.max(BBOX[:, 5])) + 3  # Add some pixels to visualise the entire cells
        W = int(np.max(BBOX[:, 6])) + 3  # Add some pixels to visualise the entire cells
        # Create the empty mosaic image
        mosaic_stack = np.zeros([stack_im.shape[0], count_y * H, count_x * W], dtype=np.uint16)
        print(mosaic_stack.shape)
        # count_x = np.floor(stack_im.shape[2] / W)
        # # count_y = np.floor(stack_im.shape[1]/H)
        stack_im = imread(path2original)
        # for each detected image, extract the original information.
        for t in range(np.max(BBOX[:, 0])):
            cells = BBOX[BBOX[:, 0] == t]
            X = 0
            Y = 0
            for c in cells:
                h = c[5]
                y = np.max((0, c[1] - int(np.floor((H - h) / 2))))
                w = c[6]
                x = np.max((0, c[2] - int(np.floor((W - w) / 2))))
                aux = stack_im[t,
                      y:np.min((stack_im.shape[1], y + H)),
                      x:np.min((stack_im.shape[2], x + W))]
                mosaic_stack[t, Y * H:Y * H + aux.shape[0], X * W:X * W + aux.shape[1]] = aux
                X += 1
                if X >= (count_x):
                    X = 0
                    Y += 1
    else:
        mosaic_stack = 0
    return mosaic_stack

def build_mosaics(path, path2original, output_path, min_roundness=0.85):
    """"""
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    folders = os.listdir(path)
    folders.sort
    print(folders)
    for f in folders:
        if f[0] != '.':
            if not f.__contains__('.'):
                build_mosaics(os.path.join(path, f), os.path.join(path2original, f),
                              os.path.join(output_path, f), min_roundness=min_roundness)
            elif f.__contains__('.tif'):
                print(f)
                im = imread(os.path.join(path, f))
                mosaic_stack = mosaic(im, os.path.join(path2original, f), min_roundness=min_roundness)
                if np.sum(mosaic_stack) > 0:
                    imsave(os.path.join(output_path, f), mosaic_stack)

# Define and use a simple function to label the plot in axes coordinates
def label(x, color, label):
    ax = plt.gca()
    ax.text(0, .2, label, fontweight="bold", color=color,
            ha="left", va="center", transform=ax.transAxes)

def plot_distributions(df, xlabel, title, output_path, smoothness=.5):
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

def plot_mitosis(data, output_path, hue_order, y_variable):

    fig = plt.figure(figsize=(10, 8))
    plt.rcParams.update({'font.size': 0.9})
    sns.lineplot(x="frame", y=y_variable, hue="Subcategory-02", data=data,
                 palette=sns.color_palette("husl", 14),
                 hue_order=hue_order, linewidth=1.5, alpha=1)
    plt.tight_layout()
    plt.title("{0} along time".format(y_variable))
    fig.savefig(os.path.join(output_path, "data_{}_counting.png".format(y_variable)), format='png',
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
        fig.savefig(os.path.join(output_path, "data_{0}_counting_{1}.png".format(y_variable, d)), format='png',
                    transparent=False)

def plot_info_wrt_peak(data, x_labels, hue_order, output_path):

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