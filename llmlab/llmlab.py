from llmlab.agent.agent import TradeAgent
from logger.logging_config import logger
from config.config import ConfigJson
from llmlab.env.env_strategy_llm import EnvStrategyLlm

class LLMLab:
    def __init__(self,task_name,env_type,trade_start_time,trade_end_time,llm_api_key,llm_model):
        logger.info(f"lab_name:{task_name},env_type:{env_type},trade_start_time:{trade_start_time},trade_end_time:{trade_end_time} begin")
        self.trade_start_time = trade_start_time
        self.trade_end_time = trade_end_time
        self.task_name = task_name
        self.llm_api_key = llm_api_key
        self.llm_model = llm_model
        config_init = ConfigJson()
        config_init.get_mainlab(task_name=task_name)
        self.mainlab_config=config_init
        self.mainlab_config.trade_env_parameters['tradeStartTime']=trade_start_time
        self.mainlab_config.trade_env_parameters['tradeEndTime'] = trade_end_time
        self.mainlab_config.trade_env_parameters['taskName'] = task_name
        self.env_type = env_type.lower()
        if self.env_type=="openai":
            self.run_llm()
        else:
            raise ValueError(f"config env_sys is not llm or gpt, env_sys: {env_type}")
        
    def run_llm(self):
        env = EnvStrategyLlm(trade_env_parameters=self.mainlab_config.trade_env_parameters)
        obs = env.reset()
        agent = TradeAgent(llm_api_key=self.llm_api_key,llm_model=self.llm_model)
        while True:
            '''
            obs simility
            hist record
            final act = sim * hist recor + action * (1 - sim)
            '''
            action = agent.predict(obs)
            print(f'obs:{obs}')
            print(f'action:{action}')
            obs, rewards, done, info = env.step(action)
            if done:
                break