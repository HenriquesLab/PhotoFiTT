import numpy as np
from scipy.optimize import curve_fit, minimize
import pandas as pd
from scipy.special import gammaln
from scipy.stats import poisson


def gaussian_function(x, a, x0, sigma):
    """
    Non normalised gaussian density (area under the curve >1)
    :param x: input value
    :param a: scaling factor and the maximum value expected for the non-normalised Gaussian density
    :param x0: mean value
    :param sigma: standard deviation
    :return: the probability density value of a Gaussian with mean x0, and standard deviation sigma.
    """
    return a * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))

def gaussian_least_squares(x, y, a, x0, sigma):
    """
    least square function for the non-normalised gaussian probability density function
    :param x and y: input pairs for which Gaussian_pdf(x) is expected to be y. x and y are 0 dimensional numbers
    :param a: scaling factor and the maximum value expected for the non-normalised Gaussian density
    :param x0: mean value
    :param sigma: standard deviation
    :return: the probability density value of a Gaussian with mean x0, and standard deviation sigma.
    """
    return sum((y - gaussian_function(x, a, x0, sigma))**2)

def poisson_function(k, lamb):
    '''poisson function, parameter lamb is the fit parameter'''
    return poisson.pmf(k, lamb)

def transformation_and_jacobian(x):
    return 1./x, 1./x**2.

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
            a, x0, sigma = params
            return sum((self.y - gaussian_function(self.x, a, x0, sigma))**2)

        elif self.prob_dist == "poisson":
            L = params
            return sum((self.y - poisson_function(self.x, L)) ** 2)

        elif self.prob_dist == "poisson_jacobian":
            mu = params
            return sum((self.y - tfm_poisson_pdf(self.x, mu)) ** 2)

    def run_minimisation(self, **kwargs):
        # Define the starting point for minimisation
        if self.prob_dist == "gaussian":
            # Usually the arithmetic mean works
            # mean = sum(self.x * self.y) / sum(self.y)
            # The peak of the curves coincide with the mean of a gaussian density function
            # index = np.where(self.y == np.max(self.y))
            # index = np.squeeze(index[0][-1])
            # mean = self.x.iloc[index]
            # sigma = np.sqrt(sum(self.y * (self.x - mean) ** 2) / sum(self.y))

            # Start with the theoretical fit
            mean = 50
            sigma = 10
            upper_bound = max(self.y)
            self.x0 = [upper_bound, mean, sigma]

        elif self.prob_dist == "poisson":
            # Define the starting point for minimisation
            self.x0 = [sum(self.x * self.y) / sum(self.y)]

        elif self.prob_dist == "poisson_jacobian":
            self.x0 = [sum(self.x * self.y) / sum(self.y)]

        return minimize(self.__least_squares__, self.x0, **kwargs)

def fit_probability(n, t, optimisation="gaussian_curve"):
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
        parameters, covariance = curve_fit(gaussian_function, t, n, p0=[max(n), mean, sigma])
    elif optimisation == "gauss-least-squares":
        lsq_gauss = lsq_minimiser(t, n)
        lsq_result = lsq_gauss.run_minimisation(method='Nelder-Mead', maxiter=1000)
        parameters = [lsq_result.x, lsq_result.fun]
    # TODO: curve fitting for other type of distributions (i.e., Poisson)
    return parameters

def run_fitting(data, var0, var1, group_var, probability_function="gauss-least-squares", symmetric2padding=False, **kwargs):
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
        f_data = f_data[f_data["processing"] == "Raw"]

        t = f_data[var0]
        n = f_data[var1]

        # if f.__contains__("Control"):
        #     parameters = [np.max(n), sum(t * n) / sum(n), np.inf]
        # else:
        if symmetric2padding:
            index = np.where(n == np.max(n))
            print(index)
            index = np.squeeze(index[0][-1])
            padding = len(n)-index
            t0 = np.zeros(padding + len(t))
            t0[:padding] = (-1)*t[-index:0:-1]
            t0[padding:] += t
            n0 = np.zeros(padding + len(n))
            n0[padding:] = n
            parameters = fit_probability(n0, t0, optimisation=probability_function)
        else:
            parameters = fit_probability(n, t, optimisation=probability_function)
        aux = pd.DataFrame(f_data.iloc[0]).transpose()
        # aux = aux.drop(["frame", "cell_size", "mitosis", "roundness_axis",
        #                 "roundness_projected", "mitosis_normalised", "processing"])
        aux = aux.reset_index()
        aux = aux[['Subcategory-00', 'Subcategory-01', 'Subcategory-02', 'video_name','unique_name']]

        aux["dist_type"] = probability_function
        if probability_function.__contains__("least"):
            aux["dist_param"] = [parameters[0]]
            aux["least_squares"] = parameters[1]
            if probability_function.__contains__("gauss"):
                aux["upper_bound"] = parameters[0][0]
                aux["mu"] = parameters[0][1]
                aux["sigma"] = parameters[0][2]
        else:
            aux["dist_param"] = parameters
            if probability_function.__contains__("gauss"):
                aux["upper_bound"] = parameters[0]
                aux["mu"] = parameters[1]
                aux["sigma"] = parameters[2]

        if len(data_param) == 0:
            data_param = aux
        else:
            data_param = pd.concat([data_param, aux]).reset_index(drop=True)

    return data_param
