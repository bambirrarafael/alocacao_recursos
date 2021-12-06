import numpy as np

from alocacao_recursos.builders.portfolio_class import Portfolio


def build_payoff_matrix_return_volatility(list_scenarios):
    n_scen = len(list_scenarios)
    payoff_return = np.zeros([n_scen, n_scen])
    payoff_volatility = np.zeros([n_scen, n_scen])
    j = 0
    for scen in list_scenarios:
        return_data_of_scen = scen.return_data
        for i in range(len(list_scenarios)):
            p = Portfolio(list_scenarios[i].list_eval_portfolios[0].x, return_data_of_scen, scen.horizonte_analise)
            p.calc_portfolio_expected_return()
            p.calc_portfolio_volatility()
            payoff_return[i, j] = p.expected_return
            payoff_volatility[i, j] = p.volatility
        j += 1
    return payoff_return, payoff_volatility
