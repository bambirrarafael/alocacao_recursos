import numpy as np


def build_regret_matrix(x):
    """

    :param x:
    :return:
    """
    r = np.zeros(x.shape)
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            r[i, j] = x[i, j] - x.min(axis=0)[j]
    return r


def build_choice_criteria_matrix(x, alpha=0.75):
    """

    :param x: nd_array com os valores de uma matriz payoff
    :param alpha:
    :return:
    """
    f_min = x.min(axis=1)
    f_med = x.mean(axis=1)
    f_max = x.max(axis=1)
    r = build_regret_matrix(x)
    a_max = r.max(axis=1)
    wald = f_max
    laplace = f_med
    savage = a_max
    hurwicz = f_max*alpha + (1-alpha)*f_min

    cc = np.array([wald, laplace, savage, hurwicz])
    cc = cc.transpose()
    return cc


def build_normalized_choice_criteria_matrix(cc, obj="min"):
    """

    :param cc:
    :param obj: {"min", "max"}
    :return:
    """
    ncc = np.zeros(cc.shape)
    if obj == "max":
        for i in range(cc.shape[0]):
            for j in range(cc.shape[1]):
                ncc[i, j] = (cc[i, j] - cc.min(axis=0)[j]) / (cc.max(axis=0)[j] - cc.min(axis=0)[j])
    else:
        for i in range(cc.shape[0]):
            for j in range(cc.shape[1]):
                ncc[i, j] = (cc.max(axis=0)[j] - cc[i, j])/(cc.max(axis=0)[j] - cc.min(axis=0)[j])
    return ncc


def build_agregated_choice_criteria_matrix(list_ncc):
    n_obj = len(list_ncc)
    result = list_ncc[0]
    for o in range(1, n_obj):
        result = np.minimum(result, list_ncc[o])
    return result
