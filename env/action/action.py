import copy
import math

import numpy as np
import pandas as pd

from env.reward.calculate_reward import CalReward
from logger.logging_config import logger
from collections import deque
class Action:
    def __init__(self,out_strategy,action_strategy_id = "two_bulin_rsi",reward_id = "rank_reward"):
        self.action_strategy_id = action_strategy_id
        self.out_strategy = out_strategy
        self.cap = deque(maxlen=6)  # cap队列，用于存放最近6次的选择
        self.cal_reward = CalReward(reward_id)  # 创建一个奖励计算对象


    def action_strategy(self,strategy_num_choose,choose_action,balance,last_tradedate,train_end_time,code_list,all_result_df):
        if self.action_strategy_id == "two_bulin_rsi_empty_vwap":
            return self.two_bulin_rsi_empty_vwap(strategy_num_choose,choose_action,balance,last_tradedate,train_end_time,code_list,all_result_df)
        elif self.action_strategy_id == "two_bulin_rsi":
            return self.two_bulin_rsi(strategy_num_choose, choose_action, balance, last_tradedate,
                                                   train_end_time, code_list, all_result_df)
        else:
            raise ValueError("action_strategy_id is not exist")

    def two_bulin_rsi(self, strategy_num_choose, choose_action, balance, last_tradedate, train_end_time, code_list,all_result_df):
        one_strategy = strategy_num_choose[0]
        two_strategy = strategy_num_choose[1]
        three_strategy = strategy_num_choose[2]
        bulin_strategy_copy = copy.deepcopy(self.out_strategy)
        rsi_strategy_copy = copy.deepcopy(self.out_strategy)
        twoma_strategy_copy = copy.deepcopy(self.out_strategy)
        # 计算三个策略的结果
        bulin_result = bulin_strategy_copy.bulin_strategy(cash=balance, start_date=last_tradedate,
                                                        end_date=train_end_time,
                                                        code_list=code_list)
        rsi_result = rsi_strategy_copy.rsi_strategy(cash=balance, start_date=last_tradedate,
                                                        end_date=train_end_time,
                                                        code_list=code_list)
        twoma_result = twoma_strategy_copy.twoma_strategy(cash=balance, start_date=last_tradedate,
                                                        end_date=train_end_time,
                                                      code_list=code_list)

        # 根据 choose_action 选择策略
        if choose_action ==0:
            one_strategy += 1
            result_df = bulin_result
            self.out_strategy = bulin_strategy_copy
        elif choose_action ==1:
            two_strategy += 1
            result_df = rsi_result
            self.out_strategy = rsi_strategy_copy
        else:
            three_strategy += 1
            result_df = twoma_result
            self.out_strategy = twoma_strategy_copy

        self.cap.append(choose_action)  # 将当前选择加入到cap队列中
        strategy_num_choose = [one_strategy, two_strategy, three_strategy]
        # 计算策略得分
        scores = [self.cal_reward.composite_strategy_score(result) for result in
                  [bulin_result, rsi_result, twoma_result]]

        # 给策略分配奖励
        reward = self.cal_reward.calculate_reward({"scores": scores, "action": choose_action, "cap": self.cap})


        result_df=result_df[['value','cash','date','strategy_name','position']]
        # print(f"scores:{scores},num_tmp:{num_tmp},best_alternative_score:{best_alternative_score},reward:{reward}")
        all_result_df = pd.concat([all_result_df, result_df])

        return all_result_df, strategy_num_choose, reward,len(result_df)

    def two_bulin_rsi_empty_vwap(self, strategy_num_choose, choose_action, balance, last_tradedate, train_end_time, code_list,all_result_df):
        one_strategy = strategy_num_choose[0]
        two_strategy = strategy_num_choose[1]
        three_strategy = strategy_num_choose[2]
        four_strategy = strategy_num_choose[3]
        five_strategy = strategy_num_choose[4]
        bulin_strategy_copy = copy.deepcopy(self.out_strategy)
        rsi_strategy_copy = copy.deepcopy(self.out_strategy)
        twoma_strategy_copy = copy.deepcopy(self.out_strategy)
        true_empty_strategy_copy = copy.deepcopy(self.out_strategy)
        vwap_strategy_copy = copy.deepcopy(self.out_strategy)
        # 计算三个策略的结果
        bulin_result = bulin_strategy_copy.bulin_strategy(cash=balance, start_date=last_tradedate,
                                                        end_date=train_end_time,
                                                        code_list=code_list)
        rsi_result = rsi_strategy_copy.rsi_strategy(cash=balance, start_date=last_tradedate,
                                                        end_date=train_end_time,
                                                        code_list=code_list)
        twoma_result = twoma_strategy_copy.twoma_strategy(cash=balance, start_date=last_tradedate,
                                                        end_date=train_end_time,
                                                      code_list=code_list)
        true_empty_result = true_empty_strategy_copy.true_empty_strategy(cash=balance, start_date=last_tradedate,
                                                          end_date=train_end_time,
                                                          code_list=code_list)
        vwap_result = vwap_strategy_copy.vwap_strategy(cash=balance, start_date=last_tradedate,
                                                          end_date=train_end_time,
                                                          code_list=code_list)

        # 根据 choose_action 选择策略
        if choose_action ==0:
            one_strategy += 1
            result_df = bulin_result
            self.out_strategy = bulin_strategy_copy
        elif choose_action ==1:
            two_strategy += 1
            result_df = rsi_result
            self.out_strategy = rsi_strategy_copy
        elif choose_action ==2:
            three_strategy += 1
            result_df = twoma_result
            self.out_strategy = twoma_strategy_copy
        elif choose_action ==3:
            four_strategy += 1
            result_df = true_empty_result
            self.out_strategy = true_empty_strategy_copy
        elif choose_action ==4:
            five_strategy += 1
            result_df = vwap_result
            self.out_strategy = vwap_strategy_copy

        self.cap.append(choose_action)  # 将当前选择加入到cap队列中
        strategy_num_choose = [one_strategy, two_strategy, three_strategy,four_strategy,five_strategy]
        # 计算策略得分
        scores = [self.cal_reward.composite_strategy_score(result) for result in
                  [bulin_result, rsi_result, twoma_result,true_empty_result,vwap_result]]

        # 给策略分配奖励
        reward = self.cal_reward.calculate_reward({"scores": scores, "action": choose_action, "cap": self.cap})


        result_df=result_df[['value','cash','date','strategy_name','position']]
        # print(f"scores:{scores},num_tmp:{num_tmp},best_alternative_score:{best_alternative_score},reward:{reward}")
        all_result_df = pd.concat([all_result_df, result_df])

        return all_result_df, strategy_num_choose, reward,len(result_df)






