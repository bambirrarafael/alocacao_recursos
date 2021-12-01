import numpy as np
import pandas as pd
import scipy.optimize as opt
import plotly.graph_objects as go

import alocacao_recursos.builders.historico_precos as hprice
import alocacao_recursos.builders.analisador_portfolios as p_analizer

from alocacao_recursos.builders.portfolio_class import Portfolio
from alocacao_recursos.builders.scenario_class import Scenario


def get_return_data(list_tuples_start_finish, timeframe="D1", save_files=False, name_scenario=""):
    return_list_frame = []
    price_list_frame = []
    for frame in list_tuples_start_finish:
        start = frame[0]
        finish = frame[1]
        price_us, price_br, price_index = hprice.create_price_csv(start, finish, save_files, name_scenario)
        price_data = hprice.create_merged_price_df(price_us, price_br, price_index, save_files, name_scenario)
        return_data = hprice.create_return_csv(price_data, save_files, name_scenario)
        merged_return_df = hprice.create_return_pivot_table_csv(return_data, save_files, name_scenario)
        merged_price_df = hprice.create_price_pivot_table_csv(price_data, save_files, name_scenario)
        return_list_frame.append(merged_return_df)
        price_list_frame.append(merged_price_df)
    result_return_data = pd.concat(return_list_frame)
    result_price_data = pd.concat(price_list_frame)
    return result_return_data, result_price_data


def build_scenario(return_data, nome_scenario, limite_orcamento, price_data, horizonte_previsao):
    n_assets = len(return_data.columns)
    x0 = np.ones(n_assets)
    bounds = [(0, 1)] * n_assets
    const = {'type': 'eq', 'fun': p_analizer.constraint_sum_percentage_equals_one}
    print("Optimization start")
    result_optimal_return = opt.minimize(p_analizer.fo_portfolio_return, x0, (return_data, horizonte_previsao),
                                         bounds=bounds, constraints=const)
    result_optimal_volatility = opt.minimize(p_analizer.fo_portfolio_volatility, x0, (return_data, horizonte_previsao),
                                             bounds=bounds, constraints=const)
    p_optimal_return = Portfolio(result_optimal_return.x, return_data, horizonte_previsao)
    p_optimal_return.calc_portfolio_expected_return()
    p_optimal_return.calc_portfolio_volatility()
    p_optimal_volatility = Portfolio(result_optimal_volatility.x, return_data, horizonte_previsao)
    p_optimal_volatility.calc_portfolio_expected_return()
    p_optimal_volatility.calc_portfolio_volatility()
    list_front_portfolios = []
    array_epsilon = np.linspace(p_optimal_volatility.expected_return, p_optimal_return.expected_return)
    for i in array_epsilon:
        const = [{'type': 'eq', 'fun': p_analizer.constraint_sum_percentage_equals_one},
                 {'type': 'ineq', 'fun': p_analizer.constraint_epsilon_return, 'args': (return_data, horizonte_previsao, i)}]
        result_epsilon = opt.minimize(p_analizer.fo_portfolio_volatility, x0, (return_data, horizonte_previsao), bounds=bounds, constraints=const)
        p = Portfolio(result_epsilon.x, return_data, horizonte_previsao)
        p.calc_portfolio_expected_return()
        p.calc_portfolio_volatility()
        list_front_portfolios.append(p)

    list_fos = [p_analizer.fo_portfolio_return, p_analizer.fo_portfolio_volatility]
    list_obj = ['max', 'min']
    list_lambda = [1, 1]
    p_harm = p_analizer.find_harmonious_solution(list_fos, list_obj, list_lambda, return_data, horizonte_previsao)
    p_analizer.plot_portfolio_volatility_return(list_front_portfolios, [p_harm], return_data, horizonte_previsao)
    p_harm.plot_portfolio_cumulative_returns(return_data["^BVSP"], "^BVSP")
    #
    scen = Scenario(return_data, nome_scenario, list_front_portfolios, [p_harm])
    return scen


def plot_scenarios(list_scenarios):
    fig = go.Figure()
    for scenario in list_scenarios:
        vol_front = []
        ret_front = []
        for portfolio in scenario.list_frontier_portfolios:
            vol_front.append(portfolio.volatility)
            ret_front.append(portfolio.expected_return)
        fig.add_trace(go.Scatter(x=vol_front,
                                 y=ret_front,
                                 mode='lines',
                                 name=scenario.scenario_name))
        #
        for portfolio in scenario.list_eval_portfolios:
            if portfolio.expected_return is not None:
                fig.add_trace(go.Scatter(x=[portfolio.volatility],
                                         y=[portfolio.expected_return],
                                         mode='markers',
                                         name=portfolio.nome_portfolio))
    fig.update_layout(xaxis_title="Volatilidade", yaxis_title="Retorno Esperado",
                      title="Risco x Retorno por cenário")
    fig.show()

