from llmlab.agent.agent import TradeAgent
from logger.logging_config import logger
from config.config import ConfigJson
from llmlab.env.env_strategy_llm import EnvStrategyLlm
from analysis.analysis_center import AnalysisCenter
import csv
import os
from datetime import datetime
class LLMLab:
    def __init__(self,task_name,env_type,trade_start_time,trade_end_time):
        logger.info(f"lab_name:{task_name},env_type:{env_type},trade_start_time:{trade_start_time},trade_end_time:{trade_end_time} begin")
        self.trade_start_time = trade_start_time
        self.trade_end_time = trade_end_time
        self.task_name = task_name
        
        config_init = ConfigJson()
        config_init.get_account()
        config_init.get_llmlab(task_name=task_name)
        self.llmlab_config=config_init
        
        
        self.llmlab_config.trade_env_parameters['tradeStartTime']=trade_start_time
        self.llmlab_config.trade_env_parameters['tradeEndTime'] = trade_end_time
        self.llmlab_config.trade_env_parameters['taskName'] = task_name
        self.actionStrategyId = self.llmlab_config.trade_env_parameters['actionStrategyId']
        self.env_type = env_type.lower()
        if self.env_type=="llm":
            self.llm_api_key = self.llmlab_config.openai_api_key
            self.llm_model = self.llmlab_config.algo_model
            self.run_llm()
        else:
            raise ValueError(f"config env_sys is not llm or gpt, env_sys: {env_type}")
        
    def run_llm(self):
        env = EnvStrategyLlm(trade_env_parameters=self.llmlab_config.trade_env_parameters)
        obs = env.reset()
        agent = TradeAgent(llm_api_key=self.llm_api_key,llm_model=self.llm_model,strategy_id=self.actionStrategyId)
        rewards = None
        # Create a directory for logs if it doesn't exist
        log_dir = "llmlog"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Create a new log file with the current timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file_path = os.path.join(log_dir, f"llm_log_{timestamp}.csv")
        # Open the log file and write headers
        with open(log_file_path, mode='w', newline='') as file:
            log_writer = csv.writer(file)
            log_writer.writerow(['input', 'output','reward'])
            while True:
                '''
                obs simility
                hist record
                final act = sim * hist recor + action * (1 - sim)
                '''
                action,output,input = agent.predict(obs,rewards)
                obs, rewards, done, info = env.step(action)
                # Write the input and output to the log file
                log_writer.writerow([input, output,rewards])
                if done:
                    break
        AnalysisCenter().compare_strategy(country=self.llmlab_config.trade_env_parameters['marketCountry'],start_time=self.trade_start_time,end_time=self.trade_end_time,code_list=self.llmlab_config.trade_env_parameters['codeList'],init_balance=float(self.llmlab_config.trade_env_parameters['balance']),task_name=self.task_name)
