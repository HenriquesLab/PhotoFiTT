import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations

def choose_statistical_test(group1, group2):
    """
    Determine the appropriate statistical test based on data characteristics.
    
    Args:
    group1, group2: Arrays of data to compare
    
    Returns:
    String indicating the appropriate test
    """
    # Check for normality using the Shapiro-Wilk test
    _, p1 = stats.shapiro(group1)
    _, p2 = stats.shapiro(group2)
    
    # Check for equal variances using Levene's test
    _, p_var = stats.levene(group1, group2)
    
    if p1 > 0.05 and p2 > 0.05:  # Both groups are normally distributed
        if p_var > 0.05:  # Equal variances
            return "t-test"
        else:  # Unequal variances
            return "Welch's t-test"
    else:  # At least one group is not normally distributed
        return "Kolmogorov-Smirnov"

def perform_statistical_test(group1, group2, test_type):
    """
    Perform the specified statistical test on two groups of data.
    
    Args:
    group1, group2: Arrays of data to compare
    test_type: String indicating which test to perform
    
    Returns:
    Tuple of (test statistic, p-value)
    """

    if test_type == "t-test":
        return stats.ttest_ind(group1, group2)
    elif test_type == "Welch's t-test":
        return stats.ttest_ind(group1, group2, equal_var=False)
    elif test_type == "Kolmogorov-Smirnov":
        return stats.ks_2samp(group1, group2)

def perform_statistical_analysis(df, quantitative_column, subcategory_00, subcategory_01,
                                 test_type="Kolmogorov-Smirnov",choose_test="Manual"):
    """
    Perform pairwise statistical analysis on groups defined by subcategories.
    
    Args:
    df: pandas DataFrame containing the data
    quantitative_column: Name of the column containing the quantitative data to analyze
    subcategory_01: Name of the column defining the subgroups to compare
    subcategory_00: Name of the column defining the main groups
    test_type: 
      - "t-test": When both groups are normally distributed and have equal variances.
      - "Welch's t-test": When both groups are normally distributed and have unequal variances.
      - "Kolmogorov-Smirnov": When at least one of the variables is not normally distributed. 
    choose_test: 
      - "Automatic" if you want to run an automatic testing based on assessed properties of the data distribution. 
      - "Manual" to manually indicate what test to run.
    Returns:
    pandas DataFrame with results of statistical tests
    """
    
    groups_00 = df[subcategory_00].unique()
    results = []
    if choose_test!="Automatic":
        print(f"The statistical test chosen is {test_type}")
        
    for group in groups_00:
        group_data = df[df[subcategory_00] == group]
        subgroups_01 = group_data[subcategory_01].unique()
        
        for subgroup1, subgroup2 in combinations(subgroups_01, 2):
            data1 = group_data[group_data[subcategory_01] == subgroup1][quantitative_column]
            data2 = group_data[group_data[subcategory_01] == subgroup2][quantitative_column]
            if choose_test=="Automatic":
                test_type = choose_statistical_test(data1, data2)
            statistic, p_value = perform_statistical_test(data1, data2, test_type)
            
            results.append({
                'Subcategory-00': group,
                'Subgroup1': subgroup1,
                'Subgroup2': subgroup2,
                'Test': test_type,
                'Statistic': statistic,
                'p-value': p_value
            })
    
    return pd.DataFrame(results)

def plot_data_distributions(df, quantitative_column, subcategory_00, subcategory_01):
    """
    Plot histograms and Q-Q plots for each subgroup to visualize data distributions.
    
    Args:
    df: pandas DataFrame containing the data
    quantitative_column: Name of the column containing the quantitative data to plot
    subcategory_01: Name of the column defining the subgroups
    subcategory_00: Name of the column defining the main groups
    """
    plt.rcParams.update({'font.size': 8})
    groups_00 = df[subcategory_00].unique()
    
    for group in groups_00:
        group_data = df[df[subcategory_00] == group]
        subgroups_01 = group_data[subcategory_01].unique()
        
        fig, axes = plt.subplots(len(subgroups_01), 2, figsize=(6, 2*len(subgroups_01)))
        fig.suptitle(f'Data Distributions for {subcategory_00}: {group}')
        
        for i, subgroup in enumerate(subgroups_01):
            data = group_data[group_data[subcategory_01] == subgroup][quantitative_column]
            
            # Histogram
            sns.histplot(data, kde=True, ax=axes[i, 0])
            axes[i, 0].set_title(f'{subcategory_01}: {subgroup} - Histogram')
            
            # Q-Q plot
            stats.probplot(data, dist="norm", plot=axes[i, 1])
            axes[i, 1].set_title(f'{subcategory_01}: {subgroup} - Q-Q Plot')
        
        plt.tight_layout()
        plt.show()