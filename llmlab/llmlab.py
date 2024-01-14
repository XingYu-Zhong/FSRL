from logger.logging_config import logger
from config.config import ConfigJson


class LLMLab:
    def __init__(self,task_name,env_type,trade_start_time,trade_end_time):
        logger.info(f"lab_name:{task_name},env_type:{env_type},trade_start_time:{trade_start_time},trade_end_time:{trade_end_time} begin")
        self.trade_start_time = trade_start_time
        self.trade_end_time = trade_end_time
        self.task_name = task_name
        config_init = ConfigJson()
        config_init.get_mainlab(task_name=task_name)
        self.mainlab_config=config_init
        self.mainlab_config.trade_env_parameters['tradeStartTime']=trade_start_time
        self.mainlab_config.trade_env_parameters['tradeEndTime'] = trade_end_time
        self.mainlab_config.trade_env_parameters['taskName'] = task_name
        self.env_type = env_type.lower()
        if self.env_type=="llm" or self.env_type=="gpt":
            self.run_llm()
        else:
            raise ValueError(f"config env_sys is not llm or gpt, env_sys: {env_type}")
        
    def run_llm(self):
        pass