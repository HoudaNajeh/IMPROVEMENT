import data.H358.data_container
import common.timemg as timemg
import matplotlib.pyplot as plt
import scipy.stats
import random
import numpy as np
from numpy.random import binomial as binomiale
from numpy.random import poisson as Poisson
from scipy.stats import poisson
import matplotlib.mlab as mlab  # probas
from scipy.optimize import curve_fit
from scipy.misc import factorial
from scipy import stats


from scipy.stats import norm

if __name__ == '__main__':
    h358 = data.H358.data_container.DataContainer(sample_time=60 * 60, starting_stringdatetime='01/01/2016 0:00:00', ending_stringdatetime='31/01/2016 23:59:00')
    raw_variable_full_names = h358.get_raw_variable_full_names()
    selected_variable_full_names = [raw_variable_full_names[4]]
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
        data=[]

        #time_deltas = [epochtimes_in_ms[j] - epochtimes_in_ms[j - 1] for j in range(1, len(epochtimes_in_ms))]
        for k in range(1, len(epochtimes_in_ms)):
            time_delta=epochtimes_in_ms[k] - epochtimes_in_ms[k - 1]
            if time_delta < 2*3600*1000:
                time_deltas.append(epochtimes_in_ms[k] - epochtimes_in_ms[k - 1])
                data=np.array(time_deltas)

        plt.hist(data, 50, normed=True)
        xt = plt.xticks()[0]
        print('xt=', xt)
        print('type_xt=', type(xt))
        print('shape_xt=', np.shape(xt))
        xmin, xmax = min(xt), max(xt)
        lnspc = np.linspace(xmin, xmax, len(data))
        ag, bg, cg = stats.gamma.fit(data)
        pdf_gamma = stats.gamma.pdf(lnspc, ag, bg, cg)
        plt.plot(lnspc, pdf_gamma, label="Gamma")
        plt.xlabel('epochtimes in ms')
        plt.ylabel('Probability')
        plt.title('Probability density of the gamma distribution')
        plt.grid(True)
        plt.show()
