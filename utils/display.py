import seaborn as sns
import matplotlib.pyplot as plt
import os


def plot_smooth_curves(data, y_var, title, output_path, name):
    fig = plt.figure(figsize=(7,6))
    plt.subplot(2, 1, 1)
    sns.lineplot(x="frame", y=y_var, hue='Subcategory-01', style='Subcategory-02', data=data, palette="tab10",
                 linewidth=1.5, alpha=0.5)
    plt.legend([])
    # plt.ylabel(y_label)
    # plt.xlabel("Time (min)")
    plt.title(title)

    # Plot the results per category
    ax = plt.subplot(2, 1, 2)
    sns.lineplot(x="frame", y=y_var, hue='Subcategory-00', style='Subcategory-02', data=data, palette="tab10",
                 linewidth=1.5, alpha=0.75)
    # plt.ylabel(y_label)
    plt.xlabel("Time (min)")
    ax.legend(bbox_to_anchor=(0.85, 0.5))
    fig.savefig(os.path.join(output_path, name), format='png')
    plt.show()