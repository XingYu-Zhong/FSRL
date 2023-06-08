import copy
import datetime
import os

import pandas as pd

from data.get_data import GetData
from env.evaluation.evaluation import Evaluation
from logger.logging_config import logger
from strategy.strategy import Strategy

MAX_NUM = 2147483647
class AnalysisCenter:
    def __init__(self):
        pass

    def compare_strategy(self,country,start_time,end_time,code_list,init_balance,task_name):
        get_data = GetData(country=country, start_date=start_time, end_date=end_time, code_list=code_list)
        trade_cal = get_data.get_trade_cal()
        trade_data = get_data.get_day_trade_data()
        out_strategy = Strategy(trade_cal,trade_data, max_strategy_step_limit=MAX_NUM,max_strategy_sell_limit=MAX_NUM)
        root_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resultdata')
        result_df_path = os.path.join(root_path,task_name+f"_balance_{start_time}_to_{end_time}.csv")
        result_df = pd.read_csv(result_df_path) if os.path.exists(result_df_path) else pd.DataFrame()
        # 将字符串转换为datetime对象

        train_start_time = datetime.datetime.strptime(result_df['date'][0], '%Y-%m-%d').strftime('%Y%m%d')
        train_end_time = datetime.datetime.strptime(result_df['date'].iloc[-1], '%Y-%m-%d').strftime('%Y%m%d')

        logger.info(f"self.init_balance:{init_balance},train_start_time:{train_start_time},self.train_end_time:{train_end_time},self.code_list:{code_list}")

        twoma_strategy_copy = copy.deepcopy(out_strategy)
        bulin_strategy_copy = copy.deepcopy(out_strategy)
        rsi_strategy_copy = copy.deepcopy(out_strategy)
        empty_strategy_copy = copy.deepcopy(out_strategy)
        true_empty_strategy_copy = copy.deepcopy(out_strategy)

        twoma_strategy_df = twoma_strategy_copy.twoma_strategy(cash=init_balance,start_date=train_start_time,end_date=train_end_time,code_list=code_list)
        bulin_strategy_df = bulin_strategy_copy.bulin_strategy(cash=init_balance,start_date=train_start_time,end_date=train_end_time,code_list=code_list)
        rsi_strategy_df = rsi_strategy_copy.rsi_strategy(cash=init_balance, start_date=train_start_time,
                                                               end_date=train_end_time, code_list=code_list)
        empty_strategy_df = empty_strategy_copy.empty_strategy(cash=init_balance,start_date=train_start_time,end_date=train_end_time,code_list=code_list)
        true_empty_strategy_df = true_empty_strategy_copy.true_empty_strategy(cash=init_balance, start_date=train_start_time,
                                                        end_date=train_end_time, code_list=code_list)


        twoma_strategy_df.to_csv(os.path.join(root_path, f"{task_name}_twoma_strategy_df_{start_time}_to_{end_time}.csv"))
        bulin_strategy_df.to_csv(os.path.join(root_path,
                                              f"{task_name}_bulin_strategy_df_{start_time}_to_{end_time}.csv"))
        rsi_strategy_df.to_csv(os.path.join(root_path,
                                              f"{task_name}_rsi_strategy_df_{start_time}_to_{end_time}.csv"))
        empty_strategy_df.to_csv(os.path.join(root_path,
                                              f"{task_name}_empty_strategy_df_{start_time}_to_{end_time}.csv"))
        true_empty_strategy_df.to_csv(os.path.join(root_path,
                                              f"{task_name}_true_empty_strategy_df_{start_time}_to_{end_time}.csv"))

        sharpe_ratio_no_risk, sharpe_ratio, max_drawdown, annualized_return, annualized_volatility, total_return, total_profits = Evaluation(
            sr_risk=0.02).standard_evaluation(df=twoma_strategy_df)

        logger.info(f"strategy:twoma_strategy_df")
        logger.info(f'sharpe_ratio:{sharpe_ratio_no_risk}')
        logger.info(f'sharpe_ratio(0.02):{sharpe_ratio}')
        logger.info(f'max_drawdown:{max_drawdown}')
        logger.info(f'annual_return:{annualized_return}')
        logger.info(f'annual_volatility:{annualized_volatility}')
        logger.info(f'Total return:{total_return}')
        logger.info(f'Total profits:{total_profits}')
        result_list = [sharpe_ratio_no_risk, sharpe_ratio, max_drawdown, annualized_return, annualized_volatility,
                       total_return, total_profits]
        twoma_strategy_result_pd = pd.DataFrame(data=result_list, columns=['twoma_strategy'],
                                                index=["sharpe_ratio", "sharpe_ratio(0.02)", "max_drawdown",
                                                       "annual_return",
                                                       "annual_volatility", "total_return", "total_profits"]).T


        sharpe_ratio_no_risk, sharpe_ratio, max_drawdown, annualized_return, annualized_volatility, total_return, total_profits = Evaluation(
            sr_risk=0.02).standard_evaluation(df=bulin_strategy_df)



        logger.info(f"strategy:bulin_strategy_df")
        logger.info(f'sharpe_ratio:{sharpe_ratio_no_risk}')
        logger.info(f'sharpe_ratio(0.02):{sharpe_ratio}')
        logger.info(f'max_drawdown:{max_drawdown}')
        logger.info(f'annual_return:{annualized_return}')
        logger.info(f'annual_volatility:{annualized_volatility}')
        logger.info(f'Total return:{total_return}')
        logger.info(f'Total profits:{total_profits}')
        result_list = [sharpe_ratio_no_risk, sharpe_ratio, max_drawdown, annualized_return, annualized_volatility,
                       total_return, total_profits]
        bulin_strategy_result_pd = pd.DataFrame(data=result_list, columns=['bulin_strategy'],
                                                index=["sharpe_ratio", "sharpe_ratio(0.02)", "max_drawdown",
                                                       "annual_return",
                                                       "annual_volatility", "total_return", "total_profits"]).T

        sharpe_ratio_no_risk, sharpe_ratio, max_drawdown, annualized_return, annualized_volatility, total_return, total_profits = Evaluation(
            sr_risk=0.02).standard_evaluation(df=rsi_strategy_df)

        logger.info(f"strategy:rsi_strategy_df")
        logger.info(f'sharpe_ratio:{sharpe_ratio_no_risk}')
        logger.info(f'sharpe_ratio(0.02):{sharpe_ratio}')
        logger.info(f'max_drawdown:{max_drawdown}')
        logger.info(f'annual_return:{annualized_return}')
        logger.info(f'annual_volatility:{annualized_volatility}')
        logger.info(f'Total return:{total_return}')
        logger.info(f'Total profits:{total_profits}')
        result_list = [sharpe_ratio_no_risk, sharpe_ratio, max_drawdown, annualized_return, annualized_volatility,
                       total_return, total_profits]
        rsi_strategy_result_pd = pd.DataFrame(data=result_list, columns=['rsi_strategy'],
                                                index=["sharpe_ratio", "sharpe_ratio(0.02)", "max_drawdown",
                                                       "annual_return",
                                                       "annual_volatility", "total_return", "total_profits"]).T

        sharpe_ratio_no_risk, sharpe_ratio, max_drawdown, annualized_return, annualized_volatility, total_return, total_profits = Evaluation(
            sr_risk=0.02).standard_evaluation(df=empty_strategy_df)

        logger.info(f"strategy:empty_strategy_df")
        logger.info(f'sharpe_ratio:{sharpe_ratio_no_risk}')
        logger.info(f'sharpe_ratio(0.02):{sharpe_ratio}')
        logger.info(f'max_drawdown:{max_drawdown}')
        logger.info(f'annual_return:{annualized_return}')
        logger.info(f'annual_volatility:{annualized_volatility}')
        logger.info(f'Total return:{total_return}')
        logger.info(f'Total profits:{total_profits}')
        result_list = [sharpe_ratio_no_risk, sharpe_ratio, max_drawdown, annualized_return, annualized_volatility,
                       total_return, total_profits]
        empty_strategy_result_pd = pd.DataFrame(data=result_list, columns=['empty_strategy'],
                                                index=["sharpe_ratio", "sharpe_ratio(0.02)", "max_drawdown",
                                                       "annual_return",
                                                       "annual_volatility", "total_return", "total_profits"]).T

        sharpe_ratio_no_risk, sharpe_ratio, max_drawdown, annualized_return, annualized_volatility, total_return, total_profits = Evaluation(
            sr_risk=0.02).standard_evaluation(df=true_empty_strategy_df)

        logger.info(f"strategy:true_empty_strategy_df")
        logger.info(f'sharpe_ratio:{sharpe_ratio_no_risk}')
        logger.info(f'sharpe_ratio(0.02):{sharpe_ratio}')
        logger.info(f'max_drawdown:{max_drawdown}')
        logger.info(f'annual_return:{annualized_return}')
        logger.info(f'annual_volatility:{annualized_volatility}')
        logger.info(f'Total return:{total_return}')
        logger.info(f'Total profits:{total_profits}')
        result_list = [sharpe_ratio_no_risk, sharpe_ratio, max_drawdown, annualized_return, annualized_volatility,
                       total_return, total_profits]
        true_empty_strategy_result_pd = pd.DataFrame(data=result_list, columns=['true_empty_strategy'],
                                                index=["sharpe_ratio", "sharpe_ratio(0.02)", "max_drawdown",
                                                       "annual_return",
                                                       "annual_volatility", "total_return", "total_profits"]).T

        file_path = os.path.join(root_path,task_name + f"_Evaluation_result_{start_time}_to_{end_time}.csv")
        orgin_result_pd = pd.read_csv(file_path,index_col=0)
        all_result_pd = pd.concat([orgin_result_pd, twoma_strategy_result_pd,bulin_strategy_result_pd,rsi_strategy_result_pd,empty_strategy_result_pd,true_empty_strategy_result_pd])
        print(all_result_pd)
        all_result_pd.to_csv(file_path)