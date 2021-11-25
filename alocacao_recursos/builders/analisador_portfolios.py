import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from alocacao_recursos.builders.portfolio_class import Portfolio


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
    fig.update_layout(xaxis_title="Volatilidade", yaxis_title="Retorno Esperado em " + horizonte + ' dias')
    fig.show()
