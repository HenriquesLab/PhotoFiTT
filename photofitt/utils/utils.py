

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
