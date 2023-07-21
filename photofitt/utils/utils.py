import numpy  as np

def numerical_dose(data, column_name="Subcategory-02", power=None):
    """

    :param data:
    :param column_name:
    :param power: Laser energy (mW/cm2) or (J/cm2)
    :return:
    """
    data["Exposure time"] = 0.
    if power is not None:
        data["Light dose"] = 0.
    for i in range(len(data)):
        s = data[column_name].iloc[i]
        if s.__contains__("Control"):
            n = -0.001
        elif s.__contains__("Synchro"):
            n = 0.
        else:
            n = float(''.join(filter(str.isdigit, s)))
            if s.__contains__("ms"):
                n = 0.001*n
        if power is not None:
            data.loc[[i], "Light dose"] = n*power
        data.loc[[i], 'Exposure time'] = n
    return data

# '''
# Rounded metrics approximation with an ABSOLUTE proportional error of 0,081081081:
#
# Approximation
# 2,5
# 5
# 10
# 20
# 40
# 80
# 100
# 500
# 1000
# 1500
# 2000
# 2500
#
# '''

def power_conversion(data, dose_column="Light dose", condition_col="Subcategory-02", condition_name="Synchro"):
    ## Generate categorical variables for the light dose
    light_dose = np.unique(data[f'{column_name}'])
    action_metrics[f'{dose_column} cat'] = ''
    for l in light_dose:
        if l > 0:
            cat = np.str(np.round(l, decimals=1)) + " J/cm2"
        else:
            cat = 'non-synchro-0 J/cm2'

        data[f'{dose_column} cat'][data[f'{dose_column}'] == l] = cat
    data[f'{dose_column} cat'][data[f'{condition_col}'] == condition_name] = '0 J/cm2'
    return data

