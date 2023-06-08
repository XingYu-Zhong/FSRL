
import datetime
import os
import random

import gym
import numpy as np
import pandas as pd
from gym import spaces

from env.action.action import Action
from env.evaluation.evaluation import Evaluation
from env.observation.observation import Observation
from logger.logging_config import logger
from data.get_data import GetData
from env.reward.calculate_reward import CalReward
from strategy.strategy import Strategy
MAX_ACCOUNT_BALANCE = 2147483647
#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)
#设置value的显示长度为100，默认为50
pd.set_option('max_colwidth',100)

class EnvStrategyTest(gym.Env):
    def __init__(self,trade_env_parameters):
        super(EnvStrategyTest, self).__init__()
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
        is_discrete = trade_env_parameters['isDiscrete'] if 'isDiscrete' in trade_env_parameters else "False"
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
        self.action_strategy = Action(
            out_strategy=Strategy(trade_cal, trade_data, max_strategy_step_limit=self.max_strategy_step_limit,
                                  max_strategy_sell_limit=self.max_strategy_sell_limit),
            action_strategy_id=self.action_strategy_id, reward_id=self.reward_id)
        # Actions of the format Buy x%, Sell x%, Hold, etc.
        self.is_discrete = is_discrete
        self.obs_factor_num = int(obs_factor_num)
        self.obs_day_num = int(obs_day_num)
        self.obs_pca_num = int(obs_pca_num)
        if is_discrete:
            self.action_space = spaces.Discrete(self.strategy_num)
        else:
            self.action_space = spaces.Box(
                low=0, high=1, shape=(1,), dtype=np.float16)
        # Prices contains the OHCL values for the last trade timestamp prices
        self.observation_space = spaces.Box(
            low=0, high=1, shape=(1, self.obs_day_num), dtype=np.float16)

        # Set the current step to a random point within the data frame
        self.current_step = self.obs_day_num+self.strategy_init_day

        self.last_tradedate = self.df.loc[self.current_step, 'date']
        self.obs_init = Observation(data=trade_data, task_name=self.task_name, code_list=code_list,
                                    obs_day_num=self.obs_day_num, obs_factor_num=self.obs_factor_num,
                                    obs_factor_name_list=obs_factor_name_list, normalize_type=normalize_type,obs_pca_num=self.obs_pca_num)
        self.obs_data = self.obs_init.init_obs()

        self.step_reward = 0



    def _next_observation(self):
        # Get the stock data points for the last trade timestamp days and scale to between 0-1
        print(f"self.current_step:{self.current_step}")
        obs = self.obs_init.get_obs(current_step=self.current_step,df=self.obs_data)
        return obs

    def reset(self):
        # Reset the state of the environment to an initial state
        self.balance = self.init_balance
        self.result_df = pd.DataFrame()
        # 重置累积奖励
        self.step_reward = 0
        # Set the current step to a random point within the data frame
        self.current_step = self.obs_day_num+self.strategy_init_day
        self.last_tradedate = self.df.loc[self.current_step, 'date']

        return self._next_observation()

    def _take_action(self, actions):
        if self.is_discrete:
            choose_action = actions
        else:
            choose_action =-1
            actions *= self.strategy_num
            for i in range(1, self.strategy_num + 1):
                if actions[0] < i:
                    choose_action = i - 1
                    break
        self.result_df, self.strategy_num_choose, reward, add_step = self.action_strategy.action_strategy(
            all_result_df=self.result_df, strategy_num_choose=self.strategy_num_choose, choose_action=choose_action,
            balance=self.balance, last_tradedate=self.last_tradedate, train_end_time=self.train_end_time,
            code_list=self.code_list)
        self.balance = self.result_df.iloc[-1]['value']
        # Update the current_step_list only if the current_step is not at the maximum value for the respective stock
        self.current_step = self.current_step + add_step if self.current_step < self.df.shape[
            0]/len(self.code_list) - 1 else self.current_step
        self.last_tradedate = self.result_df.iloc[-1]['date'].strftime('%Y%m%d')
        return reward

    def step(self, action):
        # Execute one time step within the environment
        rewards = self._take_action(action)
        # 累计奖励
        self.step_reward = rewards
        done = self.current_step >= self.df.shape[0]/len(self.code_list) - 1
        if done:

            snc_pd = pd.DataFrame(data=self.strategy_num_choose, columns=['strategy_num_choose'])
            logger.info(f"snc_pd:\n{snc_pd}")


            sharpe_ratio_no_risk, sharpe_ratio, max_drawdown, annualized_return, annualized_volatility, total_return, total_profits = Evaluation(
                sr_risk=0.02).standard_evaluation(df=self.result_df.copy())
            result_list = [sharpe_ratio_no_risk, sharpe_ratio, max_drawdown, annualized_return, annualized_volatility,total_return,total_profits]
            logger.info(f"strategy:all")
            logger.info(f'sharpe_ratio:{sharpe_ratio_no_risk}')
            logger.info(f'sharpe_ratio(0.02):{sharpe_ratio}')
            logger.info(f'max_drawdown:{max_drawdown}')
            logger.info(f'annual_return:{annualized_return}')
            logger.info(f'annual_volatility:{annualized_volatility}')
            logger.info(f'Total return:{total_return}')
            logger.info(f'Total profits:{total_profits}')
            all_result_pd = pd.DataFrame(data=result_list,columns=[self.action_strategy_id],
                                     index=["sharpe_ratio", "sharpe_ratio(0.02)", "max_drawdown", "annual_return",
                                              "annual_volatility","total_return", "total_profits"]).T
            root_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resultdata')
            file_name = self.task_name + f"_Evaluation_result_{self.train_start_time}_to_{self.train_end_time}.csv"
            file_path = os.path.join(root_path, file_name)
            balance_file_name = self.task_name + f"_balance_{self.train_start_time}_to_{self.train_end_time}.csv"
            balance_file_path= os.path.join(root_path, balance_file_name)
            all_result_pd.to_csv(file_path)
            self.result_df  = self.result_df[['value','cash','date','strategy_name','position']]
            self.result_df.to_csv(balance_file_path, index=False)
            logger.info(f"all_result_pd:\n{all_result_pd}")
            return [], rewards, done, {}
        # Update the state
        obs = self._next_observation()

        return obs, rewards, done, {}

    def render(self, mode="human"):
        snc_pd = pd.DataFrame(data=self.strategy_num_choose, columns=['strategy_num_choose'])
        logger.info(f"snc_pd:\n{snc_pd}")
        pass
