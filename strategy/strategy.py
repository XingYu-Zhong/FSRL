import json

import dateutil.parser
import numpy as np
import pandas as pd
from pandas import IndexSlice

from backtest.bao_trade_backtest import BaoBackTest
from config.config import ConfigJson
from enum import Enum

class StrategyState(Enum):
    IDLE = 1
    BUY = 2
    HOLD = 3
    SELL = 4

class Strategy:

    def __init__(self,trade_cal, trade_data,max_strategy_step_limit,max_strategy_sell_limit):
        config=ConfigJson()
        config.get_account()
        commission_rate = config.commission_rate
        lowest_commission = config.lowest_commission
        self.bao = BaoBackTest(trade_cal, trade_data, commission_rate, lowest_commission)
        self.max_strategy_step_limit = max_strategy_step_limit
        self.max_strategy_sell_limit = max_strategy_sell_limit


    def twoma_strategy(self,cash,start_date,end_date,code_list):
        """
        双均线策略
        :param cash:
        :param start_date:
        :param end_date:
        :param code_list:
        :return:
        """
        self.strategy_step = 0
        self.strategy_state = StrategyState.IDLE
        self.strategy_sell_count = 0
        self.bao.init_strategy(cash=cash, start_date=start_date, end_date=end_date, code_list=code_list)
        def achievement_strategy(end_flag = False):
            cash = self.bao.cash
            length = len(code_list)
            division_result = 1.0 / float(length)
            max_buy_cash_limit = cash * division_result


            self.strategy_step += 1
            end_flag = end_flag
            hist_data = self.bao.get_pretrade_data(code_list=self.bao.code_list,limit_num=10)
            for code in self.bao.code_list:
                # 选择特定code的数据
                data_by_code = hist_data.loc[IndexSlice[code,:], 'close']

                # 计算5天和10天移动平均值
                ma5 = data_by_code.head(5).mean()
                ma10 = data_by_code.mean()

                if ma5 > ma10 and code not in self.bao.positions:
                    if max_buy_cash_limit > self.bao.cash:
                        continue
                    self.bao.order_value(code, max_buy_cash_limit)
                    self.strategy_state = StrategyState.BUY
                if ma5 < ma10 and code in self.bao.positions:
                    self.bao.order_target_amount(code, 0)  # 买到0股就是全部卖出的意思
                    self.strategy_state = StrategyState.SELL

            if self.strategy_state == StrategyState.SELL:
                self.strategy_state = StrategyState.IDLE
                self.strategy_sell_count += 1
            if self.strategy_sell_count == self.max_strategy_sell_limit:
                end_flag = True
            if self.strategy_step==self.max_strategy_step_limit:
                end_flag = True
            return end_flag
        df = self.bao.run_strategy(achievement_strategy_func=achievement_strategy)
        df['strategy_name'] = 'twoma_strategy'
        return df

    def vwap_strategy(self, cash, start_date, end_date, code_list):
        """
        VWAP策略
        :param cash:
        :param start_date:
        :param end_date:
        :param code_list:
        :return:
        """
        self.strategy_step = 0
        self.strategy_state = StrategyState.IDLE
        self.strategy_sell_count = 0
        self.bao.init_strategy(cash=cash, start_date=start_date, end_date=end_date, code_list=code_list)

        def achievement_strategy(end_flag=False):
            max_buy_cash_limit = self.bao.cash * (1.0 / float(len(code_list)))
            self.strategy_step += 1
            end_flag = end_flag

            # 得到历史价格和成交量数据
            data = self.bao.get_pretrade_data(code_list=self.bao.code_list, limit_num=20, fields=['close', 'volume'])

            for code in self.bao.code_list:
                # 选择特定code的数据
                hist_data = data.loc[IndexSlice[code, :]]

                # 计算VWAP
                vwap = (hist_data['close'] * hist_data['volume']).sum() / hist_data['volume'].sum()

                pos = code in self.bao.positions

                # 交易逻辑与下单
                # 当有持仓，且价格高于VWAP的时候卖出股票。
                if hist_data['close'].values[-1] > vwap:
                    if pos:  # 有持仓就市价卖出股票。
                        # 全部卖出
                        self.bao.order_target_amount(code, 0)  # 买到0股就是全部卖出的意思
                        self.strategy_state = StrategyState.SELL
                # 当没有持仓，且价格低于VWAP的时候买出股票。
                elif hist_data['close'].values[-1] < vwap:
                    if not pos:  # 没有持仓就买入一百股。
                        # 用所有 cash 买入股票
                        self.bao.order_value(code, max_buy_cash_limit)
                        self.strategy_state = StrategyState.BUY

            if self.strategy_state == StrategyState.SELL:
                self.strategy_state = StrategyState.IDLE
                self.strategy_sell_count += 1
            if self.strategy_sell_count == self.max_strategy_sell_limit:
                end_flag = True
            if self.strategy_step == self.max_strategy_step_limit:
                end_flag = True
            return end_flag

        df = self.bao.run_strategy(achievement_strategy_func=achievement_strategy)
        df['strategy_name'] = 'vwap_strategy'
        return df

    def rsi_strategy(self, cash, start_date, end_date, code_list):
        """
        RSI策略
        :param cash:
        :param start_date:
        :param end_date:
        :param code_list:
        :return:
        """
        self.strategy_step = 0
        self.strategy_state = StrategyState.IDLE
        self.strategy_sell_count = 0
        self.bao.init_strategy(cash=cash, start_date=start_date, end_date=end_date, code_list=code_list)

        def achievement_strategy(end_flag=False):
            max_buy_cash_limit = self.bao.cash * (1.0 / float(len(code_list)))
            self.strategy_step += 1
            end_flag = end_flag
            rsi_period = 14  # 计算RSI的参数
            # 得到20日历史价格
            data = self.bao.get_pretrade_data(code_list=self.bao.code_list, limit_num=20)
            for code in self.bao.code_list:
                # 选择特定code的数据
                hist_data = data.loc[IndexSlice[code, :], 'close']

                # 计算RSI
                delta = hist_data.diff()
                dUp, dDown = delta.copy(), delta.copy()
                dUp[dUp < 0] = 0
                dDown[dDown > 0] = 0

                RolUp = dUp.rolling(window=rsi_period).mean()
                RolDown = dDown.rolling(window=rsi_period).mean().abs()

                RS = RolUp / RolDown
                rsi = 100.0 - (100.0 / (1.0 + RS))

                pos = code in self.bao.positions
                # 交易逻辑与下单
                # 当有持仓，且RSI大于70的时候卖出股票。
                if rsi.values[-1] > 70:
                    if pos:  # 有持仓就市价卖出股票。
                        # 全部卖出
                        self.bao.order_target_amount(code, 0)  # 买到0股就是全部卖出的意思
                        self.strategy_state = StrategyState.SELL
                # 当没有持仓，且RSI小于30的时候买出股票。
                elif rsi.values[-1] < 30:
                    if not pos:  # 没有持仓就买入一百股。
                        # 用所有 cash 买入股票
                        self.bao.order_value(code, max_buy_cash_limit)
                        self.strategy_state = StrategyState.BUY
            if self.strategy_state == StrategyState.SELL:
                self.strategy_state = StrategyState.IDLE
                self.strategy_sell_count += 1
            if self.strategy_sell_count == self.max_strategy_sell_limit:
                end_flag = True
            if self.strategy_step == self.max_strategy_step_limit:
                end_flag = True
            return end_flag

        df = self.bao.run_strategy(achievement_strategy_func=achievement_strategy)
        df['strategy_name'] = 'rsi_strategy'
        return df

    def bulin_strategy(self,cash,start_date,end_date,code_list):
        """
        布林回归策略
        :param cash:
        :param start_date:
        :param end_date:
        :param code_list:
        :return:
        """
        self.strategy_step = 0
        self.strategy_state = StrategyState.IDLE
        self.strategy_sell_count = 0
        self.bao.init_strategy(cash=cash, start_date=start_date, end_date=end_date, code_list=code_list)
        def achievement_strategy(end_flag=False):
            max_buy_cash_limit = self.bao.cash * (1.0 / float(len(code_list)))
            self.strategy_step += 1
            end_flag = end_flag
            std_range = 2 # 计算BOLL 上下轨和中轨距离的参数
            ma_period=20 # 计算BOLL布林线中轨的参数
            std_period = 20 # 计算BOLL 标准差的参数
            # 得到60日历史价格
            data = self.bao.get_pretrade_data(code_list=self.bao.code_list, limit_num=20)
            for code in self.bao.code_list:
                # 选择特定code的数据
                hist_data = data.loc[IndexSlice[code,:], 'close']

                # 计算布林带的上下界
                bollUpper = hist_data.rolling(ma_period).mean() + std_range * hist_data.rolling(std_period).std()
                bollBottom = hist_data.rolling(ma_period).mean() - std_range * hist_data.rolling(std_period).std()

                pos = code in self.bao.positions
                # 交易逻辑与下单
                # 当有持仓，且股价穿过BOLL上界的时候卖出股票。
                if hist_data.values[-1] > bollUpper.values[-1] and hist_data.values[-2] < bollUpper.values[
                    -2]:
                    if pos:  # 有持仓就市价卖出股票。
                        # 全部卖出
                        self.bao.order_target_amount(code, 0)  # 买到0股就是全部卖出的意思
                        self.strategy_state = StrategyState.SELL
                # 当没有持仓，且股价穿过BOLL下界的时候买出股票。
                elif hist_data.values[-1] < bollBottom.values[-1] and hist_data.values[-2] > \
                        bollBottom.values[-2]:
                    if not pos:  # 没有持仓就买入一百股。
                        # 用所有 cash 买入股票
                        self.bao.order_value(code, max_buy_cash_limit)
                        self.strategy_state = StrategyState.BUY
            if self.strategy_state == StrategyState.SELL:
                self.strategy_state = StrategyState.IDLE
                self.strategy_sell_count += 1
            if self.strategy_sell_count == self.max_strategy_sell_limit:
                end_flag = True
            if self.strategy_step==self.max_strategy_step_limit:
                end_flag = True
            return end_flag

        df = self.bao.run_strategy(achievement_strategy_func=achievement_strategy)
        df['strategy_name'] = 'bulin_strategy'
        return df

    def empty_strategy(self,cash,start_date,end_date,code_list):
        """
        空盘20天策略
        :param cash:
        :param start_date:
        :param end_date:
        :param code_list:
        :return:
        """
        self.bao.init_strategy(cash=cash, start_date=start_date, end_date=end_date, code_list=code_list)
        self.strategy_step = 0
        def achievement_strategy(end_flag=False):
            max_buy_cash_limit = self.bao.cash * (1.0 / float(len(code_list)))
            self.strategy_step +=1
            if self.strategy_step == 1:
                # 先卖掉全部的
                for code in self.bao.code_list:
                    self.bao.order_target_amount(code, 0)  # 买到0股就是全部卖出的意思
                for code in self.bao.code_list:
                    self.bao.order_value(code, max_buy_cash_limit)
            elif self.strategy_step == self.max_strategy_step_limit:
                end_flag = True
                for code in self.bao.code_list:
                    self.bao.order_target_amount(code, 0)  # 买到0股就是全部卖出的意思
            return end_flag

        def run_strategy(achievement_strategy_func):
            df = pd.DataFrame(columns=['value'])
            last_price = {}
            for dt in self.bao.trade_date_range:
                dt_str = dt.strftime('%Y%m%d')
                current_date = dt
                self.bao.set_current_date(current_date=current_date)
                end_flag = achievement_strategy_func()

                codes = list(self.bao.positions.keys())
                amounts = np.array(list(self.bao.positions.values()))

                # 选择特定日期和代码的数据
                current_data = self.bao.current_trade_data.loc[IndexSlice[codes,dt_str], :]

                # 如果 current_data 是一个 Series 对象，将其转换为 DataFrame
                if isinstance(current_data, pd.Series):
                    current_data = current_data.to_frame().T

                if not current_data.empty:
                    current_prices = current_data.reset_index().set_index('code')['close']
                    last_price.update(current_prices.to_dict())

                prices = np.array([last_price[code] for code in codes])
                value = self.bao.cash + np.sum(prices * amounts)
                profit = self.bao.cash - value
                total_value = self.bao.cash + profit

                df.loc[self.bao.current_date, 'value'] = total_value
                df.loc[self.bao.current_date, 'date'] = self.bao.current_date
                df.loc[self.bao.current_date, 'cash'] = self.bao.cash
                df.loc[self.bao.current_date, 'position'] = json.dumps(self.bao.positions)
                if end_flag:
                    break
            return df
        df = run_strategy(achievement_strategy_func=achievement_strategy)
        df['strategy_name'] = 'empty_strategy'
        return df

    def true_empty_strategy(self,cash,start_date,end_date,code_list):
        """
        空盘20天策略
        :param cash:
        :param start_date:
        :param end_date:
        :param code_list:
        :return:
        """
        self.bao.init_strategy(cash=cash, start_date=start_date, end_date=end_date, code_list=code_list)
        self.strategy_step = 0
        def achievement_strategy(end_flag=False):
            max_buy_cash_limit = self.bao.cash * (1.0 / float(len(code_list)))
            self.strategy_step +=1
            if self.strategy_step == 1:
                # 先卖掉全部的
                for code in self.bao.code_list:
                    self.bao.order_target_amount(code, 0)  # 买到0股就是全部卖出的意思
            elif self.strategy_step == self.max_strategy_step_limit:
                end_flag = True
            return end_flag


        df = self.bao.run_strategy(achievement_strategy_func=achievement_strategy)
        df['strategy_name'] = 'true_empty_strategy'
        return df