import json

import dateutil.parser
import numpy as np
import pandas as pd
from pandas import IndexSlice

from logger.logging_config import logger
import datetime

class BaoBackTest:

    def __init__(self,trade_cal,trade_data,commission_rate,commission_low_position_price):
        self.trade_cal = trade_cal #交易日历

        self.trade_data = trade_data.set_index(['code', 'date']) #trade data
        self.positions = {}  # positions
        self.commission_rate = commission_rate #券商佣金
        self.commission_low_position_price = commission_low_position_price #券商最低佣金
        self.current_trade_data = self.trade_data


    def set_positions(self):
        self.positions = {}  # positions

    def set_cash(self,cash):
        self.cash = cash  # cash

    def set_current_date(self,current_date):
        self.current_date = current_date  # dateutil.parser.parse(start_date) # ToDo:start_Date后一个交易日

    def get_pretrade_data(self,code_list,limit_num,fields=('open','close','high','low','volume')):

        end_date = (self.current_date - datetime.timedelta(days=1)).strftime('%Y%m%d')
        try:
            start_date = str(
                self.trade_cal[(self.trade_cal['is_open'] == 1) & (self.trade_cal['cal_date'] <= end_date)][limit_num:].iloc[0, :]['cal_date'].strftime('%Y%m%d'))
        except IndexError:
            logger.error(f"plase set GetData() start_date early,end_date:{end_date},limit_num:{limit_num},have_num:{len(self.trade_cal[(self.trade_cal['is_open'] == 1) & (self.trade_cal['cal_date'] <= end_date)])}")
            raise IndexError(f"plase set GetData() start_date early,end_date:{end_date}")

        # 创建一个布尔掩码，用于根据 code_list 和日期范围筛选数据
        code_mask = self.current_trade_data.index.isin(code_list, level=0)
        date_mask = (self.current_trade_data.index.get_level_values(1) >= start_date) & (
                    self.current_trade_data.index.get_level_values(1) <= end_date)

        # 将两个掩码组合起来
        mask = code_mask & date_mask

        # 使用掩码筛选数据
        trade_data = self.current_trade_data.loc[mask]
        trade_data = trade_data[list(fields)]
        trade_data = trade_data.apply(pd.to_numeric, errors='ignore')
        if len(trade_data)==0:

            logger.error(f"get_pretrade_data trade_data is empty,start_date:{start_date},end_date:{end_date}")
        return trade_data

    def get_current_data(self,code):
        current_date = self.current_date.strftime('%Y%m%d')
        trade_data = self.current_trade_data
        # Check if trade_data contains current_date
        if current_date not in  trade_data.index.get_level_values('date'):
            # If not, return trade_data as a one-row dataframe
            logger.error(f"this code:{code} can not trade in current_date:{current_date}")
            return pd.DataFrame(columns=trade_data.columns)

        data = trade_data.loc[IndexSlice[code, current_date], :]
        data = data.apply(pd.to_numeric, errors='ignore')
        # data = data.to_frame().T
        return data

    def _order(self,current_data,code,amount):
        p = current_data['close']
        if len(current_data) == 0:
            logger.error(f"this code:{code} can not trade today")
            return
        if self.cash - amount * p <0:
            amount = int(self.cash/p) #cash is not enough
        if amount % 100 != 0:
            if amount != -self.positions.get(code, 0):
                amount = int(amount / 100) * 100 #不是100的倍数
        if self.positions.get(code, 0) < -amount:
            amount = -self.positions.get(code, 0) #卖出股票不能超过持仓的数量

        self.positions[code] = self.positions.get(code, 0) + amount
        commission = amount * p * 0.001 * self.commission_rate
        if (commission < self.commission_low_position_price) & (amount * p > 0):
            commission = self.commission_low_position_price
        self.cash -= amount * p
        self.cash -= commission if amount > 0 else (commission - amount * p * 0.001)#如果是卖出需要扣千分之一的印花税
        if self.positions[code] == 0:
            del self.positions[code]

    def order_amount(self,code,amount):
        """
        买卖多少数量
        :param code:股票代码
        :param amount: 数量
        :return:
        """
        current_data = self.get_current_data(code)
        self._order(current_data=current_data, code=code, amount=amount)

    def order_value(self,code,value):
        """
        买卖多少钱
        :param code:股票代码
        :param value: 金额
        :return:
        """
        current_data = self.get_current_data(code)
        amount = int(value / current_data['close'])
        self._order(current_data=current_data, code=code, amount=amount)

    def order_target_value(self,code,value):
        """
        买卖到多少钱
        :param code:股票代码
        :param value: 金额
        :return:
        """
        current_data = self.get_current_data(code)
        if value < 0:
            value = 0
            logger.error("value cannot be negative")
        hold_value = self.positions.get(code, 0) * current_data['open']
        delta_value = value - hold_value
        amount = int(delta_value / current_data['close'])
        self._order(current_data=current_data, code=code, amount=amount)

    def order_target_amount(self,code,amount):
        """
        买到目标数量
        :param code:股票代码
        :param amount: 数量
        :return:
        """
        if amount<0:
            amount =0
            logger.error("amount cannot be negative")
        current_data = self.get_current_data(code)
        hold_amount = self.positions.get(code,0)
        trade_amount = amount - hold_amount
        self._order(current_data=current_data,code=code,amount=trade_amount)


    #策略
    def init_strategy(self,cash,start_date,end_date,code_list):
        self.init_balance = cash
        self.trade_date_range = pd.to_datetime(self.trade_cal[(self.trade_cal['is_open'] == 1) & (self.trade_cal['cal_date'] >= start_date) & (self.trade_cal['cal_date'] <= end_date)]['cal_date'].sort_values().values)
        # self.set_positions()
        self.strategy_step = 0
        self.code_list = code_list
        # 根据 code_list 筛选数据
        mask = self.trade_data.index.isin(code_list, level=0)
        filtered_data = self.trade_data.loc[mask]

        # 将筛选后的数据赋值给 self.current_trade_data
        self.current_trade_data = filtered_data
        if len(self.positions) == 0:
            self.init_cash = cash
        else:
            dt = self.trade_date_range[0]
            dt_str = dt.strftime('%Y%m%d')
            self.set_current_date(current_date=dt)
            sub_cash = 0
            for code,vol in self.positions.items():
                current_data = self.current_trade_data.loc[pd.IndexSlice[code, dt_str], :]

                # Ensure current_data is a DataFrame
                if isinstance(current_data, pd.Series):
                    current_data = current_data.to_frame().T


                current_prices = current_data.loc[pd.IndexSlice[code, dt_str],'close']
                sub_cash += vol*current_prices
            self.init_cash = cash-sub_cash
        self.set_cash(self.init_cash)




    def achievement_strategy(self,end_flag=True):
        end_flag = end_flag
        return end_flag

    def run_strategy(self,achievement_strategy_func):
        df = pd.DataFrame(columns=['value'])
        last_price = {}
        for dt in self.trade_date_range:
            dt_str = dt.strftime('%Y%m%d')
            self.set_current_date(current_date=dt)
            end_flag = achievement_strategy_func()

            codes = list(self.positions.keys())
            amounts = np.array(list(self.positions.values()))

            current_data = self.current_trade_data.loc[pd.IndexSlice[codes,dt_str], :]

            # Ensure current_data is a DataFrame
            if isinstance(current_data, pd.Series):
                current_data = current_data.to_frame().T



            if not current_data.empty:
                current_prices = current_data.reset_index().set_index('code')['close']
                last_price.update(current_prices.to_dict())

            prices = np.array([last_price[code] for code in codes])
            value = self.cash + np.sum(prices * amounts)
            df.loc[self.current_date, 'value'] = value
            df.loc[self.current_date, 'cash'] = self.cash
            df.loc[self.current_date, 'date'] = self.current_date
            df.loc[self.current_date, 'position'] = json.dumps(self.positions)

            if (end_flag):
                break

        return df



