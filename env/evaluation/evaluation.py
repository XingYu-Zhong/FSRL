import os

import numpy as np
from empyrical import *

from logger.logging_config import logger


class Evaluation:
    def __init__(self,sr_risk):
        self.sr_risk=sr_risk

    def standard_evaluation(self,df):
        # 计算收益率
        df['return'] = df['value'].pct_change()

        # 年化收益率和年化波动率
        annualized_return = np.mean(df['return']) * 252
        annualized_volatility = np.std(df['return']) * np.sqrt(252)
        if annualized_volatility==0:
            return 0,0,0,0,0,0,0

        # 计算夏普比率
        sharpe_ratio = (annualized_return - self.sr_risk) / annualized_volatility

        sharpe_ratio_no_risk=(annualized_return - 0) / annualized_volatility

        # 计算最大回撤
        df['cummax'] = df['value'].cummax()
        df['drawdown'] = df['value'] / df['cummax'] - 1
        max_drawdown = df['drawdown'].min()

        # 计算总收益率
        total_return = (df['value'].iloc[-1] / df['value'].iloc[0]) - 1


        total_profits = df.iloc[-1]['value'] - df.iloc[0]['value']
        # logger.info(f'sharpe_ratio:{sharperatio_no_risk}')
        # logger.info(f'sharpe_ratio(0.02):{sharperatio_risk}')
        # logger.info(f'max_drawdown:{maxdrawdown}')
        # logger.info(f'annual_return:{annualreturn}')
        # logger.info(f'annual_volatility:{annualvolatility}')
        # logger.info(f'Total profits:{total_profits}')
        return sharpe_ratio_no_risk, sharpe_ratio, max_drawdown, annualized_return, annualized_volatility,total_return,total_profits
