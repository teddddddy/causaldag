import statsmodels.api as sm


class RobustLinearTest():
    """
    Class that implements the Robust Linear Regression test using the Statsmodels API
    """
    def __init__(self, alpha=0.05):
        self.alpha = alpha
        
    def fit(self, x, y, z, data, categorical_outcome=False):
        """
        Attributes
            x (list of str): list of treatment variables
            y (str): outcome variable
            z (str): conditioned variables
            categorical_outcome (bool): flag the outcome variable as categorical or not
        """
        self.x = x
        self.y = y
        self.z = z
        self.data = data
        
        if categorical_outcome:
            family = sm.families.Binomial()
        else:
            family = sm.families.Gaussian()
            
        self.model = sm.RLM(data[y], data[x+z], family=family).fit()
        self.coef = self.model.params[x][0]
        confidence_interval = self.model.conf_int(alpha=self.alpha)
        self.lower, self.upper = confidence_interval.loc[x, 0][0], confidence_interval.loc[x, 1][0]

    def is_independent(self):
        if self.coef > 0 and self.lower > 0:
            return False
        elif self.coef < 0 and self.upper < 0:
            return False
        else:
            return True