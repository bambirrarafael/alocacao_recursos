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
        #
        self._assets_expected_returns = self.return_data.mean()
        self.n_assets = len(self._assets_expected_returns)
        self._alpha_var = alpha_var
        #
        self.expected_return_by_frame = np.sum(return_data * x, axis=1)
        self.cumulative_returns = (1 + self.expected_return_by_frame).cumprod()
        #
        self.expected_return = np.sum(self._assets_expected_returns * self.x)
        self.volatility = np.sqrt(np.dot(self.x.T, np.dot(self.cov_matrix, self.x))) * np.sqrt(period)
        #
        self.var, self.cvar = self.calc_var_cvar()
        self.drawdown = None    # todo, calc drawdown
        self.sharpe_ratio = None     # todo, calc sharpe

    def calc_var_cvar(self):
        total_frames = len(self.expected_return_by_frame)
        cut_position = int(np.round(total_frames * self._alpha_var, 0))
        if cut_position == 0:
            cut_position = 1
        sorted_returns = np.array(self.expected_return_by_frame)
        sorted_returns.sort()
        var = sorted_returns[cut_position]
        cvar = np.mean(sorted_returns[:cut_position])
        return var, cvar

    def plot_histogram_portfolio_returns(self):
        fig = px.histogram(self.expected_return_by_frame)
        fig.update_layout(xaxis_title="Retorno diário (%)", yaxis_title="Frequência")
        fig.show()

    def plot_portfolio_cumulative_returns(self):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.cumulative_returns.index,
                                 y=self.cumulative_returns,
                                 mode='lines',
                                 name='Retorno cumulativo do Portfolio'))
        fig.update_layout(xaxis_title="Tempo", yaxis_title="Retorno (X capital inicial)")
        fig.show()

    def print_asset_allocation(self):
        i = 0
        for asset in self.return_data:
            print(str(asset) + " :  " + str(self.x[i]) + " %")
            i += 1
