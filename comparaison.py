import numpy as np
from scipy import stats
from timeit import default_timer as timer
from sklearn.metrics import mean_squared_error


import ordinaryMC
import QMC
import MLMC


def CI_calc(s_array):
    """
    Calculates 95% confidence interval for the estimation of expected value of a random variable, given a sample.
    
    INPUT:
        s_array (Numpy.ndarray): A one-dimensional array of the sample
    
    OUTPUT:
        (Numpy.ndarray): with shape==(1,2) which has lower and upper bound of the confidence interval
    """
    
    X_bar = np.mean(s_array)
    Upper_b = X_bar + (np.sqrt(np.var(s_array)) * stats.norm.ppf(0.975)) / np.sqrt(len(s_array))
    Lower_b = X_bar - (np.sqrt(np.var(s_array)) * stats.norm.ppf(0.975)) / np.sqrt(len(s_array))
    return np.array([Lower_b, Upper_b])


def CI_length_calc(CI):
    """
    Calculates length of a confidence interval.
    
    INPUT:
        CI (numpy.ndarray): Confidence intervals
    
    OUTPUT:
        (numpy.ndarray): lengths of the confidence intervals
    """
    
    return CI[1:, 1] - CI[1:, 0]



def threshold_finder(CI, tol):
    """
    In an array of confidence intervals in the order of descending lengths,
    returns the index of fist interval shorter than a threshold.
    
    INPUT:
        CI (numpy.ndarray): Confidence intervals
        tol (float): length threshold
    
    OUTPUT:
        (int): the index of fist interval shorter than 'tol'.
    """
    
    CI_length = CI_length_calc(CI)
    for i, length in enumerate(CI_length):
        if length <= tol:
            print(i)
            return i
        
    else:
        return None
    


def CI_length_calc(CI):
    """
    Calculates length of a confidence interval.
    
    INPUT:
        CI (numpy.ndarray): Confidence intervals
    
    OUTPUT:
        (numpy.ndarray): lengths of the confidence intervals
    """
    
    return CI[1:, 1] - CI[1:, 0]
    

    

def CPU(optimal_sample,k, S_0, T, r, sigma, K, alpha, b, *,method):

    assert(method in ['ordinary', 'QMC', 'QMC_random', 'MLMC'])

    time = []

    if method == 'ordinary':
        for i in range(100):
            print(i)
            start = timer()
            present_payoffs = ordinaryMC.ordinary_mc_sim(optimal_sample,k, S_0, T, r, sigma, K, alpha, b)
            mean_pv_payoffs = np.mean(present_payoffs)
            end = timer() 
            time.append(end - start) 

    elif method == 'QMC':
        for i in range(100):
            print(i)
            start = timer()
            present_payoffs = QMC.QMC_mc_sim(optimal_sample, k, S_0, T, r, sigma, K, alpha, b)
            mean_pv_payoffs = np.mean(present_payoffs)
            end = timer() 
            time.append(end - start) 

    elif method == 'QMC_random':
        for i in range(100):
            print(i)
            start = timer()
            present_payoffs = QMC.QMC_mc_sim_random(optimal_sample, k, S_0, T, r, sigma, K, alpha, b)
            mean_pv_payoffs = np.mean(present_payoffs)
            end = timer() 
            time.append(end - start) 

    elif method == 'MLMC':
        for i in range(100):
            print(i)
            start = timer()
            present_payoffs = MLMC.ML_mc_sim(k, S_0, T, r, sigma, K, alpha, b)
            end = timer() 
            time.append(end - start) 

    return np.percentile(time, 50) 



def mse_time(nb_samples, k, S_0, T, r, sigma, K, alpha, b, mean_pv_payoffs_cvg, *,method):

    assert(method in ['ordinary', 'QMC', 'QMC_random', 'MLMC'])

    if method == 'ordinary':
        estimateur_values = []
        for i in range(100):
            present_payoffs = ordinaryMC.ordinary_mc_sim(nb_samples,k, S_0, T, r, sigma, K, alpha, b) 
            mean_pv_payoffs = np.mean(present_payoffs)
            estimateur_values.append(mean_pv_payoffs)
        comparaison = [mean_pv_payoffs_cvg] * len(estimateur_values)
        mse = mean_squared_error(estimateur_values, comparaison)

    elif method == 'QMC':
        estimateur_values = []
        for i in range(100):
            present_payoffs = QMC.QMC_mc_sim(nb_samples,k, S_0, T, r, sigma, K, alpha, b) 
            mean_pv_payoffs = np.mean(present_payoffs)
            estimateur_values.append(mean_pv_payoffs)
        comparaison = [mean_pv_payoffs_cvg] * len(estimateur_values)
        mse = mean_squared_error(estimateur_values, comparaison)

    elif method == 'QMC_random':
        estimateur_values = []
        for i in range(100):
            present_payoffs = QMC.QMC_mc_sim_random(nb_samples,k, S_0, T, r, sigma, K, alpha, b) 
            mean_pv_payoffs = np.mean(present_payoffs)
            estimateur_values.append(mean_pv_payoffs)
        comparaison = [mean_pv_payoffs_cvg] * len(estimateur_values)
        mse = mean_squared_error(estimateur_values, comparaison)

    elif method == 'MLMC':
        estimateur_values = []
        for i in range(100):
            present_payoffs = MLMC.ML_mc_sim(k, S_0, T, r, sigma, K, alpha, b)[0]
            estimateur_values.append(present_payoffs)
        comparaison = [mean_pv_payoffs_cvg] * len(estimateur_values)
        mse = mean_squared_error(estimateur_values, comparaison)

    return mse



def mse_comparaison(max_sample, k, S_0, T, r, sigma, K, alpha, b, mean_pv_payoffs_cvg, *,method):

    assert(method in ['ordinary', 'QMC', 'QMC_random'])

    mse_values = np.zeros(int(max_sample / 10))

    if method == 'ordinary':
        for nb_samples in range(10, max_sample + 1, 10):
            estimateur_values = []
            for i in range(300):
                present_payoffs = ordinaryMC.ordinary_mc_sim(nb_samples,k, S_0, T, r, sigma, K, alpha, b) 
                mean_pv_payoffs = np.mean(present_payoffs)
                estimateur_values.append(mean_pv_payoffs)
            comparaison = [mean_pv_payoffs_cvg] * len(estimateur_values)
            mse_values[int(nb_samples/10) - 1] = mean_squared_error(estimateur_values, comparaison)
            print(nb_samples)

    elif method == 'QMC':
        for nb_samples in range(10, max_sample + 1, 10):
            estimateur_values = []
            for i in range(300):
                present_payoffs = QMC.QMC_mc_sim(nb_samples,k, S_0, T, r, sigma, K, alpha, b) 
                mean_pv_payoffs = np.mean(present_payoffs)
                estimateur_values.append(mean_pv_payoffs)
            comparaison = [mean_pv_payoffs_cvg] * len(estimateur_values)
            mse_values[int(nb_samples/10) - 1] = mean_squared_error(estimateur_values, comparaison)
            print(nb_samples)

    elif method == 'QMC_random':
        for nb_samples in range(10, max_sample + 1, 10):
            estimateur_values = []
            for i in range(300):
                present_payoffs = QMC.QMC_mc_sim_random(nb_samples,k, S_0, T, r, sigma, K, alpha, b) 
                mean_pv_payoffs = np.mean(present_payoffs)
                estimateur_values.append(mean_pv_payoffs)
            comparaison = [mean_pv_payoffs_cvg] * len(estimateur_values)
            mse_values[int(nb_samples/10) - 1] = mean_squared_error(estimateur_values, comparaison)
            print(nb_samples)

    elif method == 'MLMC':
        for nb_samples in range(10, max_sample + 1, 10):
            estimateur_values = []
            for i in range(300):
                present_payoffs = MLMC.ML_mc_sim(k, S_0, T, r, sigma, K, alpha, b)
                estimateur_values.append(mean_pv_payoffs)
            comparaison = [mean_pv_payoffs_cvg] * len(estimateur_values)
            mse_values[int(nb_samples/10) - 1] = mean_squared_error(estimateur_values, comparaison)
            print(nb_samples)

    tpm = min(mse_values)
    tpm_arg = mse_values.argmin()
    tpm2 = [mse_values, tpm, tpm_arg]
    return tpm2
