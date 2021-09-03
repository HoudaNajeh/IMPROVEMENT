################################## test de Loi Normale Tronqué   ###########################################
#load libraries
import data.H358.data_container
import common.timemg as timemg
import scipy.stats as stats
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.stats import t
#from pylab import *
def moyenne(tableau):
    return sum(tableau, 0.0) / len(tableau)
#La variance est définie comme la moyenne des carrés des écarts à la moyenne
def variance(tableau):
    m=moyenne(tableau)
    return moyenne([(x-m)**2 for x in tableau])

#L'écart-type est défini comme la racine carrée de la variance
def ecartype(tableau):
    return variance(tableau)**0.5
def variance_Yavant_imputation(T):
    return variance(T)
#lower, upper, mu, and sigma are four parameters
lower, upper = -math.inf, math.inf#10000000
#mu, sigma = 0.6, 0.1
#mu, sigma = 5, 9
#instantiate an object X using the above four parameters,
#X = stats.truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)

#generate 1000 sample data
# samples = X.rvs(1000)
# print('type_samples=', type(samples))
# print('shape_samples=', np.shape(samples))
if __name__ == '__main__':
    h358 = data.H358.data_container.DataContainer(sample_time=60 * 60, starting_stringdatetime='01/06/2016 0:00:00', ending_stringdatetime='30/06/2016 23:59:00')
    raw_variable_full_names = h358.get_raw_variable_full_names()
    print(raw_variable_full_names)
    selected_variable_full_names = [raw_variable_full_names[5]]
    print(selected_variable_full_names)
    raw_variable_names = list()
    raw_variable_full_name_datetimes = list()
    faulty_intervals = list()
    gaps = list()
    raw_variable_indices = []
    for variable_name in selected_variable_full_names:
        epochtimes_in_ms, values = h358.get_raw_measurements_from_variables(variable_name)
        raw_variable_indices.extend([variable_name for j in range(len(epochtimes_in_ms))])
        raw_variable_full_name_datetimes.extend(timemg.epochtimems_to_datetime(epochtimes_in_ms[k]) for k in range(len(epochtimes_in_ms)))
        time_deltas=[]
        gaps=[]
        Ts=list()
        #time_deltas = [epochtimes_in_ms[j] - epochtimes_in_ms[j - 1] for j in range(1, len(epochtimes_in_ms))]
        for k in range(1, len(epochtimes_in_ms)):
            T=values[k]
            Ts.append(T)
        print('Ts=', Ts)
        samples = np.array(Ts)
        mu=variance(samples)
        sigma=ecartype(samples)
        print('sigma_data=', sigma)
        print('mu_data=', mu)
        df = 0.2
        plt.hist(samples, bins=50, alpha=0.3, label='histogram')
        plt.ylabel('% of Dataset in Bin')
        plt.xlabel('outdoor temperature')
        plt.title('Histogram representation for outdoor temperature')
        plt.legend()
        mean, var, skew, kurt = t.stats(df, moments='mvsk')
        plt.figure(2)
        plt.plot(samples, t.pdf(samples, df),'r',  alpha=0.3, label=' pdf')
        rv = t(df)
        plt.legend(loc='best', frameon=False)
        plt.xlabel('outdoor temperature')
        plt.ylabel('probability')
        plt.title('Test of student PDF for outdoor temperature')
        plt.show()
        ######
        # plt.hist(samples, bins=50, alpha=0.3, label='histogram')
        # plt.ylabel('% of Dataset in Bin')
        # plt.xlabel('door openings')
        # plt.title('Histogram representation for door openings')
        # plt.legend()
        # mean, var, skew, kurt = t.stats(df, moments='mvsk')
        # plt.figure(2)
        # plt.plot(samples, t.pdf(samples, df), 'r', alpha=0.3, label=' pdf')
        # rv = t(df)
        # plt.legend(loc='best', frameon=False)
        # #plt.xlabel('CO2 concentration')
        # plt.ylabel('probability')
        # plt.title('Test of student PDF for door openings')
        # plt.show()


        # time_delta=epochtimes_in_ms[k] - epochtimes_in_ms[k - 1]
            # if time_delta < 2*3600*1000:
            #     time_deltas.append(epochtimes_in_ms[k] - epochtimes_in_ms[k - 1])
            #     #print(time_deltas)

        # samples = np.array(time_deltas)
        #     # compute the PDF of the sample data
        # pdf_probs = stats.truncnorm.pdf(samples, (lower - mu) / sigma, (upper - mu) / sigma, mu, sigma)
        #
        #     # compute the CDF of the sample data
        # cdf_probs = stats.truncnorm.cdf(samples, (lower - mu) / sigma, (upper - mu) / sigma, mu, sigma)
        #
        #     # make a histogram for the samples
        # plt.hist(samples, bins=5, alpha=0.3, label='histogram')
        #
        #     # # plot the PDF curves
        # plt.plot(samples[samples.argsort()], pdf_probs[samples.argsort()], linewidth=2.3, label='PDF curve')
        #     #
        #     # # plot CDF curve
        # #plt.plot(samples[samples.argsort()], cdf_probs[samples.argsort()], linewidth=2.3, label='CDF curve')
        #
        #     # legend
        # # plt.legend(loc='best')
        # # plt.xlabel('epochtimes in ms')
        # # plt.ylabel('probability')
        # # plt.title('Probability density of the truncated normal distribution')
        # plt.show()
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
