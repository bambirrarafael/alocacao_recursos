import numpy as np
import scipy.optimize as opt
import plotly.express as px
import plotly.graph_objects as go

from alocacao_recursos.builders.portfolio_class import Portfolio


def optimize_portfolio(return_data, limite_orcamento, price_data):
    n_assets = len(return_data.columns)
    x0 = np.ones(n_assets)
    bounds = [(0, 1)] * n_assets
    const = {'type': 'eq', 'fun': constraint_sum_percentage_equals_one}
    print("Optimization start")
    result_return = opt.minimize(fo_portfolio_return, x0, return_data, bounds=bounds, constraints=[const])
    print(str(result_return.fun))
    p = Portfolio(result_return.x, return_data)
    p.plot_portfolio_cumulative_returns(return_data["^BVSP"], "^BVSP")
    result_volatility = opt.minimize(fo_portfolio_volatility, x0, return_data, bounds=bounds, constraints=[const])
    print(result_volatility.fun)
    print("\n")
    pass


def build_pareto_volatility_return(return_data):
    n_assets = len(return_data.columns)
    x0 = np.ones(n_assets)
    bounds = [(0, 1)] * n_assets
    const = {'type': 'eq', 'fun': constraint_sum_percentage_equals_one}
    result_list = []



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


def plot_volatility_return(list_portfolios, return_data, horizonte=1):
    n_assets = list_portfolios[0].n_assets
    fig = go.Figure()
    i = 0
    # for asset in return_data:
    #     x = np.zeros(n_assets)
    #     x[i] = 1
    #     i += 1
    #     portfolio_unitario = Portfolio(x, return_data)
    #     fig.add_trace(go.Scatter(x=[portfolio_unitario.volatility],
    #                              y=[portfolio_unitario.expected_return],
    #                              mode='markers',
    #                              name=asset))
    for portfolio in list_portfolios:
        fig.add_trace(go.Scatter(x=[portfolio.volatility],
                                 y=[portfolio.expected_return],
                                 mode='markers',
                                 name=portfolio.nome_portfolio))
    fig.update_layout(xaxis_title="Volatilidade", yaxis_title="Retorno Esperado em " + str(horizonte) + ' dias')
    fig.show()
