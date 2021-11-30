import numpy as np
import plotly.express as px
import plotly.graph_objects as go

class Portfolio(object):

    def __init__(self, x, return_data, period=252, alpha_var=0.05, nome_portfolio=None):
        """

        :param x: ndarray
        :param return_data: DataFrame
        """
        self.x = x
        self.return_data = return_data
        self.cov_matrix = return_data.cov()
        self.nome_portfolio = nome_portfolio
        self.period = period
        #

        self._alpha_var = alpha_var
        #
        self.expected_return_by_frame = np.sum(return_data * x, axis=1)
        #
        self.expected_return = None
        self.volatility = None
        self.var = None
        self.cvar = None
        #
        # self.drawdown = None    # todo, calc drawdown
        # self.sharpe_ratio = None     # todo, calc sharpe

    def calc_portfolio_expected_return(self):
        assets_expected_returns = self.return_data.mean()
        self.expected_return = np.sum(assets_expected_returns * self.x) * self.period

    def calc_portfolio_volatility(self):
        self.volatility = np.sqrt(np.dot(self.x.T, np.dot(self.cov_matrix, self.x))) * np.sqrt(self.period)

    def calc_var_cvar(self):
        total_frames = len(self.expected_return_by_frame)
        cut_position = int(np.round(total_frames * self._alpha_var, 0))
        if cut_position == 0:
            cut_position = 1
        sorted_returns = np.array(self.expected_return_by_frame)
        sorted_returns.sort()
        self.var = sorted_returns[cut_position]
        self.cvar = np.mean(sorted_returns[:cut_position])

    def plot_histogram_portfolio_returns(self):
        fig = px.histogram(self.expected_return_by_frame)
        fig.update_layout(xaxis_title="Retorno diário (%)", yaxis_title="Frequência")
        fig.show()

    def plot_portfolio_cumulative_returns(self, comparacao_df, nome_indice):
        cumulative_returns = (1 + self.expected_return_by_frame).cumprod()
        comparacao_cumulative_returns = (1 + comparacao_df).cumprod()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=cumulative_returns.index,
                                 y=cumulative_returns,
                                 mode='lines',
                                 name='Retorno cumulativo do Portfolio'))
        fig.add_trace(go.Scatter(x=comparacao_cumulative_returns.index,
                                 y=comparacao_cumulative_returns,
                                 mode='lines',
                                 name=nome_indice))
        fig.update_layout(xaxis_title="Tempo", yaxis_title="Retorno (X capital inicial)")
        fig.show()

    def print_asset_allocation(self):
        i = 0
        for asset in self.return_data:
            print(str(asset) + " :  " + str(self.x[i]) + " %")
            i += 1
