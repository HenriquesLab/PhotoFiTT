import numpy as np
from scipy.optimize import curve_fit, minimize
import pandas as pd
from scipy.special import gammaln
from scipy.stats import poisson
from sklearn.mixture import GaussianMixture

def wl_values(dev):
    WL = []
    for i in dev["unique_name"]:
        wl = i.split("-UV")[-1]
        if wl.__contains__("ms"):
            wl = 0.001 * int(wl.split("ms")[0])
        elif wl.__contains__("sec"):
            wl = int(wl.split("sec")[0])
        else:
            wl = .0
        WL.append(wl)
    dev["exposure time (sec)"] = WL
    return dev

def gaussian_function(x, sigma, mu, a):
    """
    Non normalised gaussian density (area under the curve >1)
    :param x: input value
    :param sigma: standard deviation
    :param mu: mean value
    :param a: scaling factor and the maximum value expected for the non-normalised Gaussian density
    :return: the probability density value of a Gaussian with mean x0, and standard deviation sigma.
    """
    return a * np.exp(-(x - mu) ** 2 / (2 * sigma ** 2))

def gaussian_mixture_function(x, sigma1, sigma2, mu1, mu2, a1, a2, p):
    """
    Non normalised gaussian density (area under the curve >1)
    :param x: input value
    :param sigma: standard deviation
    :param mu: mean value
    :param a: scaling factor and the maximum value expected for the non-normalised Gaussian density
    :return: the probability density value of a Gaussian with mean x0, and standard deviation sigma.
    """
    return p*(gaussian_function(x, sigma1, mu1, a1)) + (1-p)*(gaussian_function(x, sigma2, mu2, a2))

def gaussian_mixture_least_squares(x, y, sigma1, sigma2, mu1, mu2, a1, a2, p):
    """
    least square function for the non-normalised gaussian probability density function
    :param x and y: input pairs for which Gaussian_pdf(x) is expected to be y. x and y are 0 dimensional numbers
    :param mu: mean value
    :param a: scaling factor and the maximum value expected for the non-normalised Gaussian density
    :param sigma: standard deviation
    :return: the probability density value of a Gaussian with mean x0, and standard deviation sigma.
    """
    return sum((y - gaussian_mixture_function(x, sigma1, sigma2, mu1, mu2, a1, a2, p)) ** 2)

def gaussian_least_squares(x, y, sigma, mu, a):
    """
    least square function for the non-normalised gaussian probability density function
    :param x and y: input pairs for which Gaussian_pdf(x) is expected to be y. x and y are 0 dimensional numbers
    :param mu: mean value
    :param a: scaling factor and the maximum value expected for the non-normalised Gaussian density
    :param sigma: standard deviation
    :return: the probability density value of a Gaussian with mean x0, and standard deviation sigma.
    """
    return sum((y - gaussian_function(x, sigma, mu, a)) ** 2)


def poisson_function(k, lamb):
    '''poisson function, parameter lamb is the fit parameter'''
    return poisson.pmf(k, lamb)


def transformation_and_jacobian(x):
    return 1. / x, 1. / x ** 2.


def tfm_poisson_pdf(x, mu):
    y, J = transformation_and_jacobian(x)
    # For numerical stability, compute exp(log(f(x)))
    return np.exp(y * np.log(mu) - mu - gammaln(y + 1.)) * J


# class lsq_minimiser():
#     # Pose the curve fitting as an optimisation method to minimise the least square function
#     # It fits a gaussian curve by default.
#     def __init__(self, x, y, prob_dist="gaussian"):
#         # Store the parameters in the class
#         self.x = np.squeeze(x)
#         self.y = np.squeeze(y)
#         self.prob_dist = prob_dist
#
#     def __least_squares__(self, params):
#         # Define the function to minimise
#         if self.prob_dist == "gaussian":
#             # split input params
#             x0, sigma, a = params
#             return sum((self.y - gaussian_function(self.x, x0, sigma, a)) ** 2)
#
#         elif self.prob_dist == "poisson":
#             L = params
#             return sum((self.y - poisson_function(self.x, L)) ** 2)
#
#         elif self.prob_dist == "poisson_jacobian":
#             mu = params
#             return sum((self.y - tfm_poisson_pdf(self.x, mu)) ** 2)
#
#     def run_minimisation(self, options={}, **kwargs):
#         # Define the starting point for minimisation
#         if self.prob_dist == "gaussian":
#             # Usually the arithmetic mean works
#             # mean = sum(self.x * self.y) / sum(self.y)
#             # The peak of the curves coincide with the mean of a gaussian density function
#             index = np.where(self.y == np.max(self.y))
#             index = np.squeeze(index[0][-1])
#             mean = self.x[index]
#             # sigma = np.sqrt(sum(self.y * (self.x - np.mean(self.x)) ** 2) / sum(self.y))
#
#             # # Start with the theoretical fit
#             # mean = 50
#             sigma = 10
#
#             upper_bound = max(self.y)
#             self.x0 = [mean, sigma, upper_bound]
#
#         elif self.prob_dist == "poisson":
#             # Define the starting point for minimisation
#             self.x0 = [sum(self.x * self.y) / sum(self.y)]
#
#         elif self.prob_dist == "poisson_jacobian":
#             self.x0 = [sum(self.x * self.y) / sum(self.y)]
#
#         return minimize(self.__least_squares__, self.x0, options=options, **kwargs)


class lsq_minimiser():
    def __init__(self, x, y, mean=None, sigma=None, amplitude=None, prob_dist="gaussian"):
        # Store the parameters in the class
        self.x = np.squeeze(x)
        self.y = np.squeeze(y)
        self.mean = mean
        self.sigma = sigma
        self.amplitude = amplitude
        self.prob_dist = prob_dist
    def __least_squares__(self, params):
        # Define the function to minimise
        if self.prob_dist == "gaussian":
            # split input params
            if len(params)==3:
                sigma, mean, a = params
                return sum((self.y - gaussian_function(self.x, sigma, mean, a)) ** 2)
            elif len(params)==2:
                mean, a = params
                return sum((self.y - gaussian_function(self.x, self.sigma, mean, a)) ** 2)
            else:
                a = params
                return sum((self.y - gaussian_function(self.x, self.sigma, self.mean, a)) ** 2)

        elif self.prob_dist == "poisson":
            mean = params
            return sum((self.y - poisson_function(self.x, mean)) ** 2)

        elif self.prob_dist == "poisson_jacobian":
            mean = params
            return sum((self.y - tfm_poisson_pdf(self.x, mean)) ** 2)
        # # Define the function to minimise
        # return sum((self.y - gaussian_function(self.x, self.sigma, self.mean, a)) ** 2)

    def run_minimisation(self, options={}, **kwargs):
        # Define the starting point for minimisation
        if self.sigma is not None:
            if self.mean is not None:
                amplitude = max(self.y)
                self.x0 = [amplitude]
            else:
                amplitude = max(self.y)
                mean_estimate = self.x[list(np.where(self.y == max(self.y))[0])[-1]]
                self.x0 = [mean_estimate, amplitude]
        else:
            # Usually the arithmetic mean works
            # mean = sum(self.x * self.y) / sum(self.y)
            # The peak of the curves coincide with the mean of a gaussian density function
            index = list(np.where(self.y == np.max(self.y))[0])[-1]
            self.mean = self.x[index]
            self.sigma = np.sqrt(sum(self.y * (self.x - np.mean(self.x)) ** 2) / sum(self.y))
            # sigma = 10
            self.amplitude = max(self.y)
            self.x0 = [self.sigma, self.mean, self.amplitude]
        return minimize(self.__least_squares__, self.x0, options=options, **kwargs)


def fit_probability(t, n, mean=None, sigma=None, optimisation="gauss-least-squares"):
    """

    :param n: 1D numpy array with the counts for the Gaussian distribution
    :param t: 1D numpy array of the same size as n with the instances for the gaussian distribution for the data range
    :param probability_function: probability to fit for a given value t. Gaussian by default
    :return: parameters of the probability function to fit.
    """
    if optimisation == "gaussian_curve":
        # weighted arithmetic mean (corrected - check the section below)
        if sigma is not None:
            if mean is not None:
                parameters, covariance = curve_fit(gaussian_function, t, n, sigma, mean, p0=[max(n)])
            else:
                mean = sum(t * n) / sum(n)
                parameters, covariance = curve_fit(gaussian_function, t, n, sigma, p0=[mean, max(n)])
        else:
            mean = sum(t * n) / sum(n)
            sigma = np.sqrt(sum(n * (t - mean) ** 2) / sum(n))
            parameters, covariance = curve_fit(gaussian_function, t, n, p0=[sigma, mean, max(n)])
    elif optimisation == "gauss-least-squares":
        lsq_gauss = lsq_minimiser(t, n, mean=mean, sigma=sigma)
        lsq_result = lsq_gauss.run_minimisation(method='Nelder-Mead')  # , options={'maxiter': 10000, 'xatol': 0.01})
        parameters = [lsq_result.x, lsq_result.fun]
    # TODO: curve fitting for other type of distributions (i.e., Poisson)
    return parameters


# def fit_probability_amplitude(t, n, mean, sigma, optimisation="gauss-least-squares"):
#     """
#
#     :param sigma:
#     :param mean:
#     :param n: 1D numpy array with the counts for the Gaussian distribution
#     :param t: 1D numpy array of the same size as n with the instances for the gaussian distribution for the data range
#     :param probability_function: probability to fit for a given value t. Gaussian by default
#     :return: parameters of the probability function to fit.
#     """
#     if optimisation == "gaussian_curve":
#         # weighted arithmetic mean (corrected - check the section below)
#         parameters, covariance = curve_fit(gaussian_function, t, n, mean, sigma, p0=[max(n)])
#     elif optimisation == "gauss-least-squares":
#         lsq_gauss = lsq_minimiser_amplitude(t, n, mean, sigma)
#         lsq_result = lsq_gauss.run_minimisation(method='Nelder-Mead')  # , options={'maxiter': 10000, 'xatol': 0.01})
#         parameters = [lsq_result.x, lsq_result.fun]
#     # TODO: curve fitting for other type of distributions (i.e., Poisson)
#     return parameters
#

def run_fitting(data, var0, var1, group_var, probability_function="gauss-least-squares", symmetric2padding=False):
    """
    Fits a probability function to each of the videos in data using the sampling given by var0 and the counts given by var1
    :param data: pandas data frame or a path to a pandas data frame with the information for each video.
                The information for each time_point in a video should be given as one single entry in the data frame.
                The video should be identified with the variable "video_name" in the data_frame.
    :param var0: The variable corresponding to the sampling (x from y = function(x))
    :param var1: The variable for the counts (y from y = f(x))
    :param probability_function: The type of function we want to fit. Gaussian by default.
    :return:
    """
    if isinstance(data, str):
        data = pd.read_csv(data)
    data_param = []

    for f in data[group_var].unique():
        print(f)
        f_data = data[data["unique_name"] == f]
        # f_data = f_data[f_data["processing"] == "Raw"]

        t = np.squeeze(np.array(f_data[var0]))
        n = np.squeeze(np.array(f_data[var1]))

        # if f.__contains__("Control"):
        #     parameters = [np.max(n), sum(t * n) / sum(n), np.inf]
        # else:
        if symmetric2padding:
            index = np.where(n == np.max(n))
            index = np.squeeze(index[0][-1])
            padding = len(n) - index
            t0 = np.zeros(padding + len(t))
            t0[:padding] = (-1) * t[-index:0:-1]
            t0[padding:] += t
            n0 = np.zeros(padding + len(n))
            n0[padding:] = n
            parameters = fit_probability(t0, n0, optimisation=probability_function)
        else:
            parameters = fit_probability(t, n, optimisation=probability_function)
        aux = pd.DataFrame(f_data.iloc[0]).transpose()
        # aux = aux.drop(["frame", "cell_size", "mitosis", "roundness_axis",
        #                 "roundness_projected", "mitosis_normalised", "processing"])
        aux = aux.reset_index()
        aux = aux[['Subcategory-00', 'Subcategory-01', 'Subcategory-02', 'unique_name']]  # , 'video_name'

        aux["dist_type"] = probability_function
        if probability_function.__contains__("least"):
            aux["dist_param"] = [parameters[0]]
            aux["least_squares"] = parameters[1]
            if probability_function.__contains__("gauss"):
                aux["mu"] = parameters[0][0]
                aux["sigma"] = parameters[0][1]
                aux["upper_bound"] = parameters[0][2]
        else:
            aux["dist_param"] = parameters
            if probability_function.__contains__("gauss"):
                aux["mu"] = parameters[0]
                aux["sigma"] = parameters[1]
                aux["upper_bound"] = parameters[2]

        if len(data_param) == 0:
            data_param = aux
        else:
            data_param = pd.concat([data_param, aux]).reset_index(drop=True)

    return data_param


class data_statistics():

    def __init__(self, data, var0, var1, group_var, probability_function="gauss-least-squares",
                 ref_mu=None, ref_sigma=None, ref_group=None):
        self.ref_group = ref_group
        self.data = data
        self.var0 = var0
        self.var1 = var1
        self.group_var = group_var
        self.probability_function = probability_function
        self.ref_mu = ref_mu
        self.ref_sigma = ref_sigma

    def __decompose_function__(self, data, ref_lim_var0=None, fixed_peak=True):
        fitted_groups = pd.DataFrame()
        dev = pd.DataFrame()
        for g in data[self.group_var].unique():
            print(g)
            g_indexes = list(np.where(data[self.group_var] == g)[0])
            g_data = data[[self.var0, self.var1, self.group_var]].iloc[g_indexes]
            # declare the type to store it later
            g_data["type"] = "input"
            # estimate the amplitude
            x = np.squeeze(np.array(g_data[self.var0]))
            y = np.squeeze(np.array(g_data[self.var1]))

            if ref_lim_var0 is not None:
                lim_indexes = list(np.where(x < ref_lim_var0)[0])
                x = x[lim_indexes]
                y = y[lim_indexes]
            if fixed_peak:
                # params = fit_probability_amplitude(x, y, mu=self.ref_mu, sigma=self.ref_sigma,
                #                                         optimisation=self.probability_function)
                params = fit_probability(x, y, mean=self.ref_mu, sigma=self.ref_sigma,
                                              optimisation=self.probability_function)
            else:
                # params = fit_probability_amplitude(x, y, sigma=self.ref_sigma,
                #                                         optimisation=self.probability_function)
                params = fit_probability(x, y, sigma=self.ref_sigma,
                                              optimisation=self.probability_function)

            if self.probability_function.__contains__("least"):
                if self.probability_function.__contains__("gauss"):
                    if not fixed_peak:
                        mean_g = params[0][0]
                        amplitude_g = params[0][1]
                    else:
                        amplitude_g = params[0][0]
                        mean_g = self.ref_mu
            else:
                if self.probability_function.__contains__("gauss"):
                    amplitude_g = params[0]
            # fit the reference gaussian with a new amplitude and store it
            ref_fit_g = g_data.copy()
            ref_fit_g[self.var1] = gaussian_function(ref_fit_g[self.var0], self.ref_sigma, mean_g, amplitude_g)
            ref_fit_g["type"] = "reference distribution"
            # estimate the bias/deviation caused by the estimulation
            bias_fit_g = g_data.copy()
            bias_fit_g[self.var1] = bias_fit_g[self.var1] - ref_fit_g[self.var1]
            bias_fit_g["type"] = "bias"
            fitted_groups = pd.concat([fitted_groups, g_data, ref_fit_g, bias_fit_g]).reset_index(drop=True)

            ##AREA CALCULATION
            # total area under the curve
            averages = []
            g_data.sort_values(self.var0)
            x = g_data[self.var0].unique()
            for t in x:
                index = list(np.where(g_data[self.var0] == t)[0])
                averages.append(np.mean(g_data[self.var1].iloc[index]))
            auc_g = np.trapz(averages, dx=x[1])
            auc_ref_g = np.trapz(gaussian_function(x, self.ref_sigma, mean_g, amplitude_g),
                                 dx=x[1])
            d = {self.group_var: [g], "auc": [auc_g], "synchronised cells": [auc_ref_g/auc_g],
                 "deviation": [1-(auc_ref_g/auc_g)], "peak": [mean_g]}
            dev = pd.concat([dev,
                             pd.DataFrame(data=d)]).reset_index(drop=True)
        return fitted_groups, dev

    def __reference_fit__(self, ref_data, ref_lim_var0=None):
        # fit a gaussian curve to a specific group of data
        ref_data = ref_data.sort_values(self.var0)
        if ref_lim_var0 is not None:
            lim_indexes = list(np.where(ref_data[self.var0] < ref_lim_var0)[0])
            ref_data = ref_data.iloc[lim_indexes]
        x = np.squeeze(np.array(ref_data[self.var0]))
        y = np.squeeze(np.array(ref_data[self.var1]))
        parameters = fit_probability(x, y, optimisation=self.probability_function)
        # extract the parameters according to the optimisation procedure
        if self.probability_function.__contains__("least"):
            if self.probability_function.__contains__("gauss"):
                ref_sigma = parameters[0][0]
                ref_mu = parameters[0][1]
                ref_amplitude = parameters[0][2]
        else:
            if self.probability_function.__contains__("gauss"):
                ref_sigma = parameters[0]
                ref_mu = parameters[1]
                ref_amplitude = parameters[2]
        return ref_sigma, ref_mu, ref_amplitude

    def estimate_deviation(self, ref_lim_var0=None, fixed_peak=True):

        if self.ref_group is not None:
            ref_indexes = list(np.where(self.data[self.group_var] == self.ref_group)[0])
            ref_data = self.data[[self.var0, self.var1]].iloc[ref_indexes]
            self.ref_sigma, self.ref_mu, self.ref_amplitude = self.__reference_fit__(ref_data,
                                                                                     ref_lim_var0=ref_lim_var0)
            # Subtract the reference gaussian to the data
            self.data_no_ref = self.data.drop(self.data.index[ref_indexes], axis=0)
            fitted_groups, dev = self.__decompose_function__(self.data_no_ref, ref_lim_var0=ref_lim_var0,
                                                             fixed_peak=fixed_peak)
        else:
            fitted_groups, dev = self.__decompose_function__(self.data, ref_lim_var0=ref_lim_var0,
                                                             fixed_peak=fixed_peak)
        dev = wl_values(dev)
        return fitted_groups, dev

        # # total area under the curve
        # auc_g = np.trapz(y, dx=x[1])
        # x_max = x[np.where(y == np.max(y))[0][-1]]
        # y_max = np.max(y)
        # y_reduction = y - ref_fit_g
        # auc_ref_g = np.trapz(ref_fit_g, dx=x[1])/auc_g

def GaussianMixtureTime(data, variable_name, random_state=0):
    """
    The function will fit a gaussian mixture model with two gaussian distributions for each time point.
    :param data:
    :param variable_name:
    :param random_state:
    :return:
    """
    mean_t = []
    for t in np.unique(data["frame"]):
        data_t = data[data["frame"]==t][variable_name]
        data_t = np.array(data_t).flatten()
        if len(data_t) > 1:
            gmm_t = GaussianMixture(n_components=2, random_state=random_state).fit(data_t.reshape(-1, 1))

            index = np.where(gmm_t.means_ == np.min(gmm_t.means_))
            mean_0 = gmm_t.means_[index].flatten()
            mean_0 = mean_0[0]
            cov_0 = gmm_t.covariances_[index].flatten()
            cov_0 = cov_0[0]

            index = np.where(gmm_t.means_ == np.max(gmm_t.means_))
            mean_1 = gmm_t.means_[index].flatten()
            mean_1 = mean_1[0]
            cov_1 = gmm_t.covariances_[index].flatten()
            cov_1 = cov_1[0]
        else:
            mean_0 = np.mean(data_t)
            cov_0 = 0
            mean_1 = np.mean(data_t)
            cov_1 = 0

        mean_t.append([t] + [np.mean(data_t)] + [np.var(data_t)] + [mean_0] + [mean_1] + [cov_0] + [cov_1])
    output_data = pd.DataFrame(mean_t, columns=['frame', 'average', 'variance', 'GaussianMixtureMean_0', 'GaussianMixtureMean_1',
                                         'GaussianMixtureCovariance_0', 'GaussianMixtureCovariance_1'])

    output_data["derivative-average"] = np.concatenate([[0],np.diff(output_data["average"])])
    return output_data

def extract_gaussian_params(data, variable):
    """
    It will run the gaussian mixture model fit considering the condition of each experiment
    :param data:
    :param variable:
    :return:
    """
    distribution_data = None
    data = data[data[variable] != "[]"].reset_index(drop=True)
    for f in np.unique(data["Subcategory-00"]):
        print(f)
        data_f = data[data["Subcategory-00"] == f].reset_index(drop=True)
        for c in np.unique(data_f["Subcategory-01"]):
            print(c)
            data_c = data_f[data_f["Subcategory-01"] == c].reset_index(drop=True)
            for g in np.unique(data_c["Subcategory-02"]):
                print(g)
                data_g = data_c[data_c["Subcategory-02"] == g].reset_index(drop=True)
                data_r = None
                for r in range(len(data_g)):
                    values = data_g.iloc[r][variable][1:-1].split(",")
                    aux = pd.DataFrame([[np.float32(k), data_g.iloc[r].frame] for k in values],
                                       columns=[variable, "frame"])
                    if data_r is None:
                        data_r = aux
                    else:
                        data_r = pd.concat([data_r, aux]).reset_index(drop=True)
                # Create the data
                if data_r is not None:
                    v_dist = GaussianMixtureTime(data_r, variable)
                    v_dist["Subcategory-00"] = f
                    v_dist["Subcategory-01"] = c
                    v_dist["Subcategory-02"] = g
                    if distribution_data is None:
                        distribution_data = v_dist
                    else:
                        distribution_data = pd.concat([distribution_data, v_dist]).reset_index(drop=True)
    return distribution_data


def extract_gaussian_params_videowise(data, variable):
    """
    It will run the gaussian mixture model fit considering the condition of each experiment
    :param data:
    :param variable:
    :return:
    """
    # TODO: These loops could be optimised and be more general. Note that a folder + video name defines a unique file
    distribution_data = None
    data = data[data[variable] != "[]"].reset_index(drop=True)
    for f in np.unique(data["Subcategory-00"]):
        print(f)
        data_f = data[data["Subcategory-00"] == f].reset_index(drop=True)
        for c in np.unique(data_f["Subcategory-01"]):
            print(c)
            data_c = data_f[data_f["Subcategory-01"] == c].reset_index(drop=True)
            for g in np.unique(data_c["Subcategory-02"]):
                print(g)
                data_g = data_c[data_c["Subcategory-02"] == g].reset_index(drop=True)
                for v in np.unique(data_g["video_name"]):
                    data_v = data_g[data_g["video_name"] == v].reset_index(drop=True)
                    data_r = None
                    for r in range(len(data_v)):
                        values = data_v.iloc[r][variable][1:-1].split(",")
                        aux = pd.DataFrame([[np.float32(k), data_g.iloc[r].frame] for k in values],
                                           columns=[variable, "frame"])
                        if data_r is None:
                            data_r = aux
                        else:
                            data_r = pd.concat([data_r, aux]).reset_index(drop=True)
                    # Create the data
                    if data_r is not None:
                        v_dist = GaussianMixtureTime(data_r, variable)
                        v_dist["Subcategory-00"] = f
                        v_dist["Subcategory-01"] = c
                        v_dist["Subcategory-02"] = g
                        v_dist["video_name"] = v
                        if distribution_data is None:
                            distribution_data = v_dist
                        else:
                            distribution_data = pd.concat([distribution_data, v_dist]).reset_index(drop=True)
    return distribution_data