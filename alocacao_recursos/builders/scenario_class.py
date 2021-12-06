import plotly.graph_objects as go


class Scenario(object):

    def __init__(self, return_data, horizonte_analise, scenario_name=None, list_frontier_portfolios=None, list_eval_portfolios=None):
        self.return_data = return_data
        self.list_frontier_portfolios = list_frontier_portfolios
        self.list_eval_portfolios = list_eval_portfolios
        self.scenario_name = scenario_name
        self.horizonte_analise = horizonte_analise
