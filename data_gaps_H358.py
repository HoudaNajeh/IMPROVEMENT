import data.H358.data_container
import common.timemg as timemg
import testunion_intersec
import matplotlib.pyplot as plt
from scipy.special import erf
import math
from math import sqrt
############### moyenne, variance, ecart type #########################
#moyenne
def moyenne(tableau):
    return sum(tableau, 0.0) / len(tableau)

#La variance est définie comme la moyenne des carrés des écarts à la moyenne
def variance(tableau):
    m=moyenne(tableau)
    return moyenne([(x-m)**2 for x in tableau])

#L'écart-type est défini comme la racine carrée de la variance
def ecartype(tableau):
    return variance(tableau)**0.5
#Cette fonction calcule les trous dans les données
def detect_gaps(epochtimesms: list, values: list):
    delta_values = [values[k + 1] - values[k] for k in range(len(values) - 1)]
    sigma = sqrt(variance(delta_values))
    mu = ecartype(delta_values)
    #a et b sont l'intervalle de définition de la loi de distribution
    #le retard suit la loi normale tronqué qui est définie sur R+ ([0, +infini[). Donc a=0 et b=+infini
    a = 0
    b = math.inf
    ################ calcul de th ################
    #D'abord, on calcule f0
    f0=((1/sqrt(2*math.pi))*math.exp(-0.5*(mu**2/sigma**2)))/(sigma*(0.5 * (1 + erf((b - mu) / (sqrt(2) * sigma))) - 0.5 * (1 + erf((a - mu) / (sqrt(2) * sigma)))))
    th= mu+sigma*sqrt((-2 * math.log(f0 + 0.99) -2*math.log(0.5*(1+erf(((b-mu)/(sqrt(2)*sigma)))) - 0.5*(1+erf(((a-mu)/(sqrt(2)*sigma)))))-2 * math.log(1 / sigma)+ 2 * math.log(1 / sqrt(2 * math.pi))))
    print('th=', th)
    for k in range(1, len(values) - 1):
        if (values[k] > th):
            gaps.append([timemg.epochtimems_to_datetime(epochtimesms[k]), timemg.epochtimems_to_datetime(epochtimesms[k + 1])])
    return gaps
if __name__ == '__main__':
    h358 = data.H358.data_container.DataContainer(sample_time=60 * 60, starting_stringdatetime='01/01/2016 0:00:00', ending_stringdatetime='31/03/2016 23:59:00')
    raw_variable_full_names = h358.get_raw_variable_full_names()
    print(raw_variable_full_names)
    #Data gaps pour 1 variable: exemple Toffice wall (voir raw_variable_full_names pour connaitre l'indice de la variable)
    selected_variable_full_names = [raw_variable_full_names[0],raw_variable_full_names[1], raw_variable_full_names[2]] #avec 4 est l'indice de la variable
    # Data gaps pour 2 variable: exemple Toffice wall and Tcorridor
    # selected_variable_full_names = [raw_variable_full_names[0], raw_variable_full_names[1]]
    # Data gaps pour tous les variables
    #selected_variable_full_names =raw_variable_full_names
    print(selected_variable_full_names)
    raw_variable_names = list()
    raw_variable_full_name_datetimes = list()
    faulty_intervals = list()
    gaps = list()
    raw_variable_indices = []
    for variable_name in selected_variable_full_names:
        epochtimes_in_ms, values = h358.get_raw_measurements_from_variables(variable_name)
        print(values)
        raw_variable_indices.extend([variable_name for j in range(len(epochtimes_in_ms))])
        raw_variable_full_name_datetimes.extend(timemg.epochtimems_to_datetime(epochtimes_in_ms[k]) for k in range(len(epochtimes_in_ms)))
        time_deltas=[]
        gaps=[]
        time_deltas = [epochtimes_in_ms[j] - epochtimes_in_ms[j - 1] for j in range(1, len(epochtimes_in_ms))]
        gaps.append(detect_gaps(epochtimes_in_ms, time_deltas))
        print('gaps=', gaps)
    global_gaps = testunion_intersec.union([gaps])
    print('Global :\n', global_gaps)
    fig, ax = plt.subplots()
    ax.plot(raw_variable_full_name_datetimes, raw_variable_indices, '|k')
    plt.xlabel('datetimes', fontsize=15)
    #plt.ylabel('time_deltas', fontsize=15)
    plt.title('Detection of data gaps', fontsize=15)
    ax.grid()
    plt.show()