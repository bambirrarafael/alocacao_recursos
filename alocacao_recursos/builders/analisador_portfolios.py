import numpy as np
import scipy.optimize as opt
import plotly.express as px
import plotly.graph_objects as go

from alocacao_recursos.builders.portfolio_class import Portfolio


def optimize_portfolio(return_data, limite_orcamento, price_data, risk_free_ratio):
    n_assets = len(return_data.columns)
    x0 = np.ones(n_assets)
    bounds = [(0, 1)] * n_assets
    const = {'type': 'eq', 'fun': constraint_sum_percentage_equals_one}
    print("Optimization start")
    result_optimal_return = opt.minimize(fo_portfolio_return, x0, return_data, bounds=bounds, constraints=const)
    p_optimal_return = Portfolio(result_optimal_return.x, return_data)
    p_optimal_return.calc_portfolio_expected_return()
    p_optimal_return.calc_portfolio_volatility()
    list_front_portfolios = []
    array_epsilon = np.linspace(0, -result_optimal_return.fun)
    for i in array_epsilon:
        const = [{'type': 'eq', 'fun': constraint_sum_percentage_equals_one},
                 {'type': 'ineq', 'fun': constraint_epsilon_return, 'args': (return_data, i)}]
        result_epsilon = opt.minimize(fo_portfolio_volatility, x0, return_data, bounds=bounds, constraints=const)
        p = Portfolio(result_epsilon.x, return_data)
        p.calc_portfolio_expected_return()
        p.calc_portfolio_volatility()
        list_front_portfolios.append(p)

    list_fos = [fo_portfolio_return, fo_portfolio_volatility]
    list_obj = ['max', 'min']
    list_lambda = [1, 1]
    p_harm = find_harmonious_solution(list_fos, list_obj, list_lambda, return_data)
    plot_volatility_return(list_front_portfolios, [p_harm], return_data)

    print(str(result_optimal_return.fun))
    p_optimal_return = Portfolio(result_optimal_return.x, return_data)
    p_optimal_return.plot_portfolio_cumulative_returns(return_data["^BVSP"], "^BVSP")
    result_volatility = opt.minimize(fo_portfolio_volatility, x0, return_data, bounds=bounds, constraints=[const])
    print(result_volatility.fun)
    print("\n")



def find_harmonious_solution(list_fos, list_obj, list_lambda, return_data):
    """

    :param list_fos: lista com as funções que vao ser avaliadas
    :param list_obj: lista com os objetivos de cada função: ex ['max', 'min']
    :param list_lambda: lista com os coeficientes de importancia de cada função: ex [0.43, 0.57]
    :param return_data: dataframe com os retornos de cada ativo
    :return:
    """
    n_assets = len(return_data.columns)
    x0 = np.ones(n_assets)
    bounds = [(0, 1)] * n_assets
    const = {'type': 'eq', 'fun': constraint_sum_percentage_equals_one}
    #
    fo_1 = list_fos[0]
    fo_2 = list_fos[1]
    objective_1 = list_obj[0]
    objective_2 = list_obj[1]
    lambda_1 = list_lambda[0]
    lambda_2 = list_lambda[1]
    #
    result_fo1 = opt.minimize(fo_1, x0, return_data, bounds=bounds, constraints=const)
    p_opt_fo_1 = Portfolio(result_fo1.x, return_data)
    p_opt_fo_1.calc_portfolio_expected_return()
    p_opt_fo_1.calc_portfolio_volatility()
    p_opt_fo_1.calc_var_cvar()
    #
    result_fo2 = opt.minimize(fo_2, x0, return_data, bounds=bounds, constraints=const)
    p_opt_fo_2 = Portfolio(result_fo2.x, return_data)
    p_opt_fo_2.calc_portfolio_expected_return()
    p_opt_fo_2.calc_portfolio_volatility()
    p_opt_fo_2.calc_var_cvar()
    #
    max_f1 = p_opt_fo_1.expected_return
    aux_p = Portfolio(result_fo2.x, return_data)
    aux_p.calc_portfolio_expected_return()
    min_f1 = aux_p.expected_return
    #
    min_f2 = p_opt_fo_2.volatility
    aux_p = Portfolio(result_fo1.x, return_data)
    aux_p.calc_portfolio_volatility()
    max_f2 = aux_p.volatility
    #
    n_assets = len(return_data.columns)
    x0 = result_fo1.x
    bounds = [(0, 1)] * n_assets
    const = {'type': 'eq', 'fun': constraint_sum_percentage_equals_one}
    result_max_min = opt.minimize(fo_max_min, x0, (return_data, max_f1, min_f1, max_f2, min_f2, objective_1, objective_2), bounds=bounds, constraints=const)
    p_harmonious = Portfolio(result_max_min.x, return_data, nome_portfolio="harmonious")
    p_harmonious.calc_portfolio_expected_return()
    p_harmonious.calc_portfolio_volatility()
    return p_harmonious


def normalize_min_volatility(x, return_data, f_max, f_min, fo_lambda=1):
    num = f_max - fo_portfolio_volatility(x, return_data)
    den = f_max - f_min
    return (num/den) ** fo_lambda


def normalize_max_return(x, return_data, f_max, f_min, fo_lambda=1):
    num = -fo_portfolio_return(x, return_data) - f_min
    den = f_max - f_min
    return (num/den) ** fo_lambda


def fo_max_min(x, return_data, f1_max, f1_min, f2_max, f2_min, f1_obj, f2_obj, f1_lambda=1, f2_lambda=1):
    result_f1 = normalize_max_return(x, return_data, f1_max, f1_min, f1_lambda)
    result_f2 = normalize_min_volatility(x, return_data, f2_max, f2_min, f2_lambda)
    return -np.min([result_f1, result_f2])


def fo_portfolio_return(x, return_data):
    p1 = Portfolio(x, return_data)
    p1.calc_portfolio_expected_return()
    return -p1.expected_return


def fo_portfolio_volatility(x, return_data):
    p1 = Portfolio(x, return_data)
    p1.calc_portfolio_volatility()
    return p1.volatility


def fo_portfolio_cvar(x, return_data):
    p1 = Portfolio(x, return_data)
    p1.calc_var_cvar()
    return -p1.cvar


def constraint_sum_percentage_equals_one(x):
    return 1 - np.sum(x)


def constraint_epsilon_return(x, return_data, epsilon):
    p1 = Portfolio(x, return_data)
    p1.calc_portfolio_expected_return()
    return p1.expected_return - epsilon


def plot_volatility_return(list_frontier_portfolios, list_eval_portfolios, return_data, horizonte=252):
    n_assets = len(return_data.columns)
    fig = go.Figure()
    vol_front = []
    ret_front = []
    for portfolio in list_frontier_portfolios:
        vol_front.append(portfolio.volatility)
        ret_front.append(portfolio.expected_return)
    fig.add_trace(go.Scatter(x=vol_front,
                             y=ret_front,
                             mode='lines',
                             name="Frontier"))
    #
    if n_assets <= 5:
        i = 0
        for asset in return_data:
            x = np.zeros(n_assets)
            x[i] = 1
            i += 1
            portfolio_unitario = Portfolio(x, return_data)
            portfolio_unitario.calc_portfolio_expected_return()
            portfolio_unitario.calc_portfolio_volatility()
            fig.add_trace(go.Scatter(x=[portfolio_unitario.volatility],
                                     y=[portfolio_unitario.expected_return],
                                     mode='markers',
                                     name=asset))
    #
    for portfolio in list_eval_portfolios:
        if portfolio.expected_return is not None:
            fig.add_trace(go.Scatter(x=[portfolio.volatility],
                                     y=[portfolio.expected_return],
                                     mode='markers',
                                     name=portfolio.nome_portfolio))
    fig.update_layout(xaxis_title="Volatilidade", yaxis_title="Retorno Esperado", title="Risco x Retorno em " + str(horizonte) + " dias")
    fig.show()
