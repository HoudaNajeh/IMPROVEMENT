# from scipy.stats import beta
# import numpy as np
# import matplotlib.pyplot as plt
# import data.H358.data_container
# import common.timemg as timemg
# import scipy.stats as stats
# import matplotlib.pyplot as plt
# import numpy as np
# import math
# from scipy.stats import t
# import scipy.stats
# def moyenne(tableau):
#     return sum(tableau, 0.0) / len(tableau)
# #La variance est définie comme la moyenne des carrés des écarts à la moyenne
# def variance(tableau):
#     m=moyenne(tableau)
#     return moyenne([(x-m)**2 for x in tableau])
#
# #L'écart-type est défini comme la racine carrée de la variance
# def ecartype(tableau):
#     return variance(tableau)**0.5
# def variance_Yavant_imputation(T):
#     return variance(T)
# #lower, upper, mu, and sigma are four parameters
# lower, upper = -math.inf, math.inf#10000000
# #mu, sigma = 0.6, 0.1
# #mu, sigma = 5, 9
# #instantiate an object X using the above four parameters,
# #X = stats.truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)
#
# #generate 1000 sample data
# # samples = X.rvs(1000)
# # print('type_samples=', type(samples))
# # print('shape_samples=', np.shape(samples))
# if __name__ == '__main__':
#     h358 = data.H358.data_container.DataContainer(sample_time=60 * 60, starting_stringdatetime='01/06/2016 0:00:00', ending_stringdatetime='30/06/2016 23:59:00')
#     raw_variable_full_names = h358.get_raw_variable_full_names()
#     #selected_variable_full_names = [raw_variable_full_names[15]]#outdoor temperature
#     selected_variable_full_names = [raw_variable_full_names[6]]#office CO2
#     print(selected_variable_full_names)
#     raw_variable_names = list()
#     raw_variable_full_name_datetimes = list()
#     faulty_intervals = list()
#     gaps = list()
#     raw_variable_indices = []
#     for variable_name in selected_variable_full_names:
#         epochtimes_in_ms, values = h358.get_raw_measurements_from_variables(variable_name)
#         raw_variable_indices.extend([variable_name for j in range(len(epochtimes_in_ms))])
#         raw_variable_full_name_datetimes.extend(timemg.epochtimems_to_datetime(epochtimes_in_ms[k]) for k in range(len(epochtimes_in_ms)))
#         time_deltas=[]
#         gaps=[]
#         Ts=list()
#         for k in range(1, len(epochtimes_in_ms)-1):
#             T=values[k]
#             Ts.append(T)
#         print('Ts=', Ts)
#         samples = np.array(Ts)
#         mu=variance(samples)
#         sigma=ecartype(samples)
#         plt.hist(samples, bins=50, alpha=0.3, label='histogram')
#         #fig, ax = plt.subplots(1, 1)
#         a, b = 1.22, 3
#         mean, var, skew, kurt = beta.stats(a, b, moments='mvsk')
#         plt.figure(2)
#         # rv = beta(a, b)
#         # plt.plot(samples, rv.pdf(samples), 'k-', lw=2, label='frozen pdf')
#         plt.plot(beta.pdf(samples, a, b), 'r-', lw=5, alpha=0.6, label='beta pdf')
#         #r = beta.rvs(a, b, size=1000)
#         plt.xlabel('door openings')
#         plt.ylabel('probability')
#         plt.legend()
#         plt.title('Test of beta PDF for door openings')
#         plt.show()

        samples = np.array(Ts)
        mu=variance(samples)
        sigma=ecartype(samples)
        plt.hist(samples, bins=50, alpha=0.3, label='histogram')
        #fig, ax = plt.subplots(1, 1)
        a, b = 1.22, 3
        mean, var, skew, kurt = beta.stats(a, b, moments='mvsk')
        plt.figure(2)
        # rv = beta(a, b)
        # plt.plot(samples, rv.pdf(samples), 'k-', lw=2, label='frozen pdf')
        plt.plot(beta.pdf(samples, a, b), 'r-', lw=5, alpha=0.6, label='beta pdf')
        #r = beta.rvs(a, b, size=1000)
        plt.xlabel('door openings')
        plt.ylabel('probability')
        plt.legend()
        plt.title('Test of beta PDF for door openings')
        plt.show()