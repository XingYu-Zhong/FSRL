import numpy as np
import pandas as pd
from data.get_data import GetData
from env.observation.observation import Observation
from env.action.action import Action
from strategy.strategy import Strategy
class EnvStrategyLlm:
    def __init__(self,trade_env_parameters) -> None:
        country = trade_env_parameters['marketCountry'] if 'marketCountry' in trade_env_parameters else 'zh'
        train_start_time = trade_env_parameters['tradeStartTime']
        train_end_time = trade_env_parameters['tradeEndTime']
        code_list = trade_env_parameters['codeList']
        balance = trade_env_parameters['balance'] if 'balance' in trade_env_parameters else 100000.0
        task_name = trade_env_parameters['taskName'] if 'taskName' in trade_env_parameters else 'nontaskName'
        strategy_num = trade_env_parameters['strategyNum']
        strategy_init_day = trade_env_parameters['strategyInitDay'] if 'strategyInitDay' in trade_env_parameters else 35
        max_strategy_step_limit = trade_env_parameters[
            'maxStrategyStepLimit'] if 'maxStrategyStepLimit' in trade_env_parameters else 60
        max_strategy_sell_limit = trade_env_parameters[
            'maxStrategySellLimit'] if 'maxStrategySellLimit' in trade_env_parameters else 1
        action_strategy_id = trade_env_parameters[
            'actionStrategyId'] if 'actionStrategyId' in trade_env_parameters else "two_bulin_rsi"
        reward_id = trade_env_parameters['rewardId'] if 'rewardId' in trade_env_parameters else "rank_reward"
        obs_factor_num = trade_env_parameters['obsFactorNum'] if 'obsFactorNum' in trade_env_parameters else 5
        obs_day_num = trade_env_parameters['obsDayNum'] if 'obsDayNum' in trade_env_parameters else 20
        obs_factor_name_list = trade_env_parameters[
            'obsFactorNameList'] if 'obsFactorNameList' in trade_env_parameters else ["mytt"]
        normalize_type = trade_env_parameters['normalizeType'] if 'normalizeType' in trade_env_parameters else "minmax"
        obs_pca_num = trade_env_parameters['obsPcaNum'] if 'obsPcaNum' in trade_env_parameters else "1"



        get_data = GetData(country=country, start_date=train_start_time, end_date=train_end_time, code_list=code_list)
        trade_cal = get_data.get_trade_cal()
        trade_data = get_data.get_day_trade_data()
        code_list_tmp = []
        for code in code_list:
            if code[0] == "h":
                code_list_tmp.append(str(code)[-7:])
            else:
                code_list_tmp.append(str(code)[-6:])
        code_list = code_list_tmp
        del code_list_tmp
        self.df = trade_data
        self.train_end_time = train_end_time
        self.init_balance = float(balance)
        self.task_name = task_name
        self.code_list = code_list
        self.reward_range = (0, 100000)
        self.strategy_num = int(strategy_num)
        self.strategy_num_choose = [0 for _ in range(self.strategy_num)]  # 策略选择记录
        self.train_start_time = train_start_time
        self.train_end_time = train_end_time
        self.strategy_init_day = int(strategy_init_day)
        self.max_strategy_step_limit = int(max_strategy_step_limit)
        self.max_strategy_sell_limit = int(max_strategy_sell_limit)
        self.action_strategy_id = action_strategy_id
        self.reward_id = reward_id
        #TODO
        self.action_strategy = Action(
            out_strategy=Strategy(trade_cal, trade_data, max_strategy_step_limit=self.max_strategy_step_limit,
                                  max_strategy_sell_limit=self.max_strategy_sell_limit),
            action_strategy_id=self.action_strategy_id, reward_id=self.reward_id)

        self.obs_factor_num = int(obs_factor_num)
        self.obs_day_num = int(obs_day_num)
        self.obs_pca_num = int(obs_pca_num)

        self.current_step = self.obs_day_num+self.strategy_init_day

        self.last_tradedate = self.df.loc[self.current_step, 'date']
        self.obs_init = Observation(data=trade_data, task_name=self.task_name, code_list=code_list,
                                    obs_day_num=self.obs_day_num, obs_factor_num=self.obs_factor_num,
                                    obs_factor_name_list=obs_factor_name_list, normalize_type=normalize_type,obs_pca_num=self.obs_pca_num)
        self.obs_data = self.obs_init.init_obs()

        self.step_reward = 0