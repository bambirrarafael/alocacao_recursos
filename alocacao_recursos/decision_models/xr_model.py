"""
Discrete decision making:
XR models Package - Build by bambirrarafael
"""
#
# Import
import numpy as np
import matplotlib.pyplot as plt


def check_non_strict_dominance(x1, y1, x2, y2, obj):
    """
    Function that differs two membership functions by its best values - if the first share points in the top of the
    trapezium with the second
    :param x1: x axis points of 1° membership function
    :param y1: y axis points of 1° membership function
    :param x2: x axis points of 2° membership function
    :param y2: y axis points of 2° membership function
    :param obj: string in {min, max} witch represents the objective of optimization
    :return: {True, False}
    """
    #
    # Check if x_i and y_i has the same size
    if len(x1) != len(y1):
        print('Error - Missing data for membership function 1')
    if len(x2) != len(y2):
        print('Error - Missing data for membership function 2')
    #
    # tell if 1 non-strict dominates 2
    if np.amax(y1) == np.amax(y2):
        top_of_function_1 = y1 == np.amax(y1)
        top_of_function_2 = y2 == np.amax(y2)
        values = []
        for i in range(len(x1)):
            if top_of_function_1[i]:
                values.append(x1[i])
        if obj == 'min':
            for i in range(len(x2)):
                if top_of_function_2[i]:
                    if x2[i] >= np.amin(values):
                        return True
            return False
        elif obj == 'max':
            for i in range(len(x2)):
                if top_of_function_2[i]:
                    if x2[i] <= np.amax(values):
                        return True
            return False
        else:
            print('Error - Wrong definition of objective')
    else:
        return False


def intersection_point(x1, y1, x2, y2):
    """
    Function that returns the intersection point between two membership functions
    :param x1: x axis points of 1° membership function
    :param y1: y axis points of 1° membership function
    :param x2: x axis points of 2° membership function
    :param y2: y axis points of 2° membership function
    :return: float that represents value of non-strict dominance
    """
    #
    # define intersection point
    k = 0
    mu = 0
    while k < len(x2) - 1:
        for i in range(len(x1) - 1):
            line1 = [[x1[i], y1[i]], [x1[i + 1], y1[i + 1]]]
            line2 = [[x2[k], y2[k]], [x2[k + 1], y2[k + 1]]]
            xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
            ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

            def det(a, b):
                return a[0] * b[1] - a[1] * b[0]

            div = det(xdiff, ydiff)
            if div == 0:
                mu = 0
                continue

            d = (det(*line1), det(*line2))
            x = det(d, xdiff) / div
            y = det(d, ydiff) / div
            if np.amin([x1[i], x2[k]]) < x < np.amax([x1[i + 1], x2[k + 1]]) and np.amin([[y1[i]], [y2[k]]]) < y < \
                    np.amax([y1[i + 1], y2[k + 1]]):
                mu = y
                return mu
        k += 1
    return mu


def build_relation_matrix(x, y, obj):
    """
    Function that build non-strict preference relation matrix from membership functions
    :param x: array of lists where each list is a point in the x axis
    :param y: array of lists where each list is a point in the y axis
    :param obj: string in {min, max} witch represents the objective of optimization
    :return: numpy array that contains non-strict preference relation matrix
    """
    #
    # check length of inputs
    if len(x) != len(y):
        print('Error - Missing data for membership functions')
    n = len(x)
    #
    # Build relation matrix
    r = np.zeros([n, n])
    for i in range(n):
        for j in range(n):
            if i == j:
                r[i, j] = np.amax(y[i])
            elif check_non_strict_dominance(x[i], y[i], x[j], y[j], obj):
                r[i, j] = np.amax(y[i])
            else:
                r[i, j] = intersection_point(x[i], y[i], x[j], y[j])
    # print(r)
    return r


def plot_membership_functions(x, y, names):
    """
    Function that plots membership functions
    :param x: array of lists where each list is a point in the x axis
    :param y: array of lists where each list is a point in the y axis
    :param names: list with the names of the functions
    :return: image
    """
    #
    # Check x and y lists
    if len(x) != len(y):
        print('Error - Missing data for membership functions')
    for i in range(len(x)):
        if len(x[i]) != len(y[i]):
            print('Error - Wrong declaration of membership function ' + str(i + 1))
    #
    # Build plot
    for i in range(len(x)):
        plt.plot(x[i], y[i], label=names[i])
    plt.legend()
    plt.show()


def evaluate_on_xr_model(x):
    """
    Function of evaluate non-strict preference relation matrix in <X, R> model
    :param x: nd-array square matrix of any size witch has the non-strict preference relation
    :return: non dominance score of alternatives
    """

    #
    # Evaluate ir matrix is square
    n = np.shape(x)
    if n[0] != n[1]:
        print('Error - Matrix is not square!')
    #
    # Print relation matrix
    print('\n')
    print(' ---- Relation Matrix ---- ')
    print(x)
    #
    # Build preference matrix
    p = np.zeros(n)
    for i in range(n[0]):
        for j in range(n[1]):
            if i == j:
                p[i, j] = 0
            if x[i, j] - x[j, i] < 0:
                p[i, j] = 0
            else:
                p[i, j] = x[i, j] - x[j, i]
    #
    # Print preference matrix
    print('\n')
    print(' ---- Preference Matrix ---- ')
    print(p)
    #
    # Build alternative's non dominance matrix
    nd = 1 - np.amax(p, 0)
    #
    # Print non dominance matrix
    print('\n')
    print(' ---- Non Dominance Matrix ---- ')
    print(nd)
    return nd
