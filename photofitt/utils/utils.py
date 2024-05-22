import numpy as np


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

    CON = np.unique(data[f'{column_name}'])
    for c in CON:

        if c.__contains__("Control"):
            n = -0.001
        elif c.__contains__("Synchro"):
            n = 0.
        else:
            n = float(''.join(filter(str.isdigit, c)))
            if c.__contains__("ms"):
                n = 0.001 * n
        index_c = data[data[f'{column_name}'] == c].index.to_list()
        if power is not None:
            data.loc[index_c, "Light dose"] = n * power
        data.loc[index_c, 'Exposure time'] = n
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
    """

    :param data:
    :param dose_column:
    :param condition_col:
    :param condition_name:
    :return:
    """
    ## Generate categorical variables for the light dose
    light_dose = np.unique(data[f'{dose_column}'])
    data[f'{dose_column} cat'] = ''
    for l in light_dose:
        if l > 0:
            cat = np.str(np.round(l, decimals=1)) + " J/cm2"
        else:
            cat = 'non-synchro-0 J/cm2'
        l_index = data[data[f'{dose_column}'] == l].index.to_list()
        data.loc[l_index, f'{dose_column} cat'] = cat
    c_index = data[data[f'{condition_col}'] == condition_name].index.to_list()
    data.loc[c_index, f'{dose_column} cat'] = '0 J/cm2'
    return data


def power_wavelength_conversion(data, dose_column="Light dose Wavelength", condition_col="Subcategory-02",
                                condition_name="Synchro"):
    """

    :param data:
    :param dose_column:
    :param condition_col:
    :param condition_name:
    :return:
    """
    ## Generate categorical variables for the light dose
    light_dose = np.unique(data[f'{dose_column}'])
    data[f'{dose_column} cat'] = ''
    for l in light_dose:
        if l > 0:
            cat = np.str(np.round(l, decimals=2)) + " J/cm2 (1/nm)"
        else:
            cat = 'non-synchro-0 J/cm2 (1/nm)'
        l_index = data[data[f'{dose_column}'] == l].index.to_list()
        data.loc[l_index, f'{dose_column} cat'] = cat
    c_index = data[data[f'{condition_col}'] == condition_name].index.to_list()
    data.loc[c_index, f'{dose_column} cat'] = '0 J/cm2 (1/nm)'
    return data


def cell_density_FOV(cell_density=25000., fov_area=660., well_area=80.91):
    """

    :param cell_density: number of cells per ml after washing (~25000)
    :param fov_area: Lateral of the field of view in microns (~660). This will depend on the microscope
    :param well_area: Total area in mm of the well. (~80.91)
    :return:
    """
    fov_mm = (fov_area * 0.001) ** 2  ## Area of the FOV in mm^2
    cell_mm = cell_density / well_area  ## Cell number per mm^2
    cell_fov = cell_mm * fov_mm
    return cell_fov
