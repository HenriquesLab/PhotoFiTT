import numpy as np
from scipy.optimize import curve_fit, minimize
import pandas as pd
from scipy.special import gammaln
from scipy.stats import poisson


def gaussian_function(x, x0, sigma, a):
    """
    Non normalised gaussian density (area under the curve >1)
    :param x: input value
    :param a: scaling factor and the maximum value expected for the non-normalised Gaussian density
    :param x0: mean value
    :param sigma: standard deviation
    :return: the probability density value of a Gaussian with mean x0, and standard deviation sigma.
    """
    return a * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))


def gaussian_least_squares(x, y, x0, sigma, a):
    """
    least square function for the non-normalised gaussian probability density function
    :param x and y: input pairs for which Gaussian_pdf(x) is expected to be y. x and y are 0 dimensional numbers
    :param a: scaling factor and the maximum value expected for the non-normalised Gaussian density
    :param x0: mean value
    :param sigma: standard deviation
    :return: the probability density value of a Gaussian with mean x0, and standard deviation sigma.
    """
    return sum((y - gaussian_function(x, x0, sigma, a)) ** 2)


def poisson_function(k, lamb):
    '''poisson function, parameter lamb is the fit parameter'''
    return poisson.pmf(k, lamb)


def transformation_and_jacobian(x):
    return 1. / x, 1. / x ** 2.


def tfm_poisson_pdf(x, mu):
    y, J = transformation_and_jacobian(x)
    # For numerical stability, compute exp(log(f(x)))
    return np.exp(y * np.log(mu) - mu - gammaln(y + 1.)) * J


class lsq_minimiser():
    # Pose the curve fitting as an optimisation method to minimise the least square function
    # It fits a gaussian curve by default.
    def __init__(self, x, y, prob_dist="gaussian"):
        # Store the parameters in the class
        self.x = np.squeeze(x)
        self.y = np.squeeze(y)
        self.prob_dist = prob_dist

    def __least_squares__(self, params):
        # Define the function to minimise
        if self.prob_dist == "gaussian":
            # split input params
            x0, sigma, a = params
            return sum((self.y - gaussian_function(self.x, x0, sigma, a)) ** 2)

        elif self.prob_dist == "poisson":
            L = params
            return sum((self.y - poisson_function(self.x, L)) ** 2)

        elif self.prob_dist == "poisson_jacobian":
            mu = params
            return sum((self.y - tfm_poisson_pdf(self.x, mu)) ** 2)

    def run_minimisation(self, options={}, **kwargs):
        # Define the starting point for minimisation
        if self.prob_dist == "gaussian":
            # Usually the arithmetic mean works
            # mean = sum(self.x * self.y) / sum(self.y)
            # The peak of the curves coincide with the mean of a gaussian density function
            index = np.where(self.y == np.max(self.y))
            index = np.squeeze(index[0][-1])
            mean = self.x[index]
            # sigma = np.sqrt(sum(self.y * (self.x - np.mean(self.x)) ** 2) / sum(self.y))

            # # Start with the theoretical fit
            # mean = 50
            sigma = 10

            upper_bound = max(self.y)
            self.x0 = [mean, sigma, upper_bound]

        elif self.prob_dist == "poisson":
            # Define the starting point for minimisation
            self.x0 = [sum(self.x * self.y) / sum(self.y)]

        elif self.prob_dist == "poisson_jacobian":
            self.x0 = [sum(self.x * self.y) / sum(self.y)]

        return minimize(self.__least_squares__, self.x0, options=options, **kwargs)


class lsq_minimiser_amplitude():
    def __init__(self, x, y, mean, sigma):
        # Store the parameters in the class
        self.x = np.squeeze(x)
        self.y = np.squeeze(y)
        self.mean = mean
        self.sigma = sigma

    def __least_squares__(self, a):
        # Define the function to minimise
        return sum((self.y - gaussian_function(self.x, self.mean, self.sigma, a)) ** 2)

    def run_minimisation(self, options={}, **kwargs):
        # Define the starting point for minimisation
        a = max(self.y)
        self.x0 = [a]
        return minimize(self.__least_squares__, self.x0, options=options, **kwargs)


def fit_probability(t, n, optimisation="gauss-least-squares"):
    """

    :param n: 1D numpy array with the counts for the Gaussian distribution
    :param t: 1D numpy array of the same size as n with the instances for the gaussian distribution for the data range
    :param probability_function: probability to fit for a given value t. Gaussian by default
    :return: parameters of the probability function to fit.
    """
    if optimisation == "gaussian_curve":
        # weighted arithmetic mean (corrected - check the section below)
        mean = sum(t * n) / sum(n)
        sigma = np.sqrt(sum(n * (t - mean) ** 2) / sum(n))
        parameters, covariance = curve_fit(gaussian_function, t, n, p0=[mean, sigma, max(n)])
    elif optimisation == "gauss-least-squares":
        lsq_gauss = lsq_minimiser(t, n)
        lsq_result = lsq_gauss.run_minimisation(method='Nelder-Mead')  # , options={'maxiter': 10000, 'xatol': 0.01})
        parameters = [lsq_result.x, lsq_result.fun]
    # TODO: curve fitting for other type of distributions (i.e., Poisson)
    return parameters


def fit_probability_amplitude(t, n, mean, sigma, optimisation="gauss-least-squares"):
    """

    :param sigma:
    :param mean:
    :param n: 1D numpy array with the counts for the Gaussian distribution
    :param t: 1D numpy array of the same size as n with the instances for the gaussian distribution for the data range
    :param probability_function: probability to fit for a given value t. Gaussian by default
    :return: parameters of the probability function to fit.
    """
    if optimisation == "gaussian_curve":
        # weighted arithmetic mean (corrected - check the section below)
        parameters, covariance = curve_fit(gaussian_function, t, n, mean, sigma, p0=[max(n)])
    elif optimisation == "gauss-least-squares":
        lsq_gauss = lsq_minimiser_amplitude(t, n, mean, sigma)
        lsq_result = lsq_gauss.run_minimisation(method='Nelder-Mead')  # , options={'maxiter': 10000, 'xatol': 0.01})
        parameters = [lsq_result.x, lsq_result.fun]
    # TODO: curve fitting for other type of distributions (i.e., Poisson)
    return parameters


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

    def __decompose_function__(self, data, ref_lim_var0=None):
        fitted_groups = pd.DataFrame()
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
                amplitude_g = fit_probability_amplitude(x[lim_indexes], y[lim_indexes], self.ref_mu, self.ref_sigma,
                                                    optimisation=self.probability_function)
            else:
                amplitude_g = fit_probability_amplitude(x, y, self.ref_mu, self.ref_sigma,
                                                        optimisation=self.probability_function)
            if self.probability_function.__contains__("least"):
                if self.probability_function.__contains__("gauss"):
                    amplitude_g = amplitude_g[0][0]
            else:
                if self.probability_function.__contains__("gauss"):
                    amplitude_g = amplitude_g[0]
            # fit the reference gaussian with a new amplitude and store it
            ref_fit_g = g_data.copy()

            ref_fit_g[self.var1] = gaussian_function(x, self.ref_mu, self.ref_sigma, amplitude_g)
            ref_fit_g["type"] = "reference distribution"
            # estimate the bias/deviation caused by the estimulation
            bias_fit_g = g_data.copy()
            bias_fit_g[self.var1] = y - ref_fit_g[self.var1]
            bias_fit_g["type"] = "bias"
            fitted_groups = pd.concat([fitted_groups, g_data, ref_fit_g, bias_fit_g]).reset_index(drop=True)
        return fitted_groups

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
                ref_mu = parameters[0][0]
                ref_sigma = parameters[0][1]
                ref_amplitude = parameters[0][2]
        else:
            if self.probability_function.__contains__("gauss"):
                ref_mu = parameters[0]
                ref_sigma = parameters[1]
                ref_amplitude = parameters[2]
        return ref_mu, ref_sigma, ref_amplitude

    def estimate_deviation(self, ref_lim_var0=None):

        if self.ref_group is not None:
            ref_indexes = list(np.where(self.data[self.group_var] == self.ref_group)[0])
            ref_data = self.data[[self.var0, self.var1]].iloc[ref_indexes]
            self.ref_mu, self.ref_sigma, self.ref_amplitude = self.__reference_fit__(ref_data, ref_lim_var0=ref_lim_var0)
            # Subtract the reference gaussian to the data
            self.data_no_ref = self.data.drop(self.data.index[ref_indexes], axis=0)
            fitted_groups = self.__decompose_function__(self.data_no_ref, ref_lim_var0=ref_lim_var0)
        else:
            fitted_groups = self.__decompose_function__(self.data, ref_lim_var0=ref_lim_var0)
        return fitted_groups

        # # total area under the curve
        # auc_g = np.trapz(y, dx=x[1])
        # x_max = x[np.where(y == np.max(y))[0][-1]]
        # y_max = np.max(y)
        # y_reduction = y - ref_fit_g
        # auc_ref_g = np.trapz(ref_fit_g, dx=x[1])/auc_g
