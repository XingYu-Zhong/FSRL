from env.env_strategy_test import EnvStrategyTest
from env.env_strategy_train import EnvStrategyTrain


class EnvironmentInit:
    def __init__(self,env_name,env_type):
        if env_type.lower()=="load":
            self.env_name = env_name+"_train"
        else:
            self.env_name = env_name+"_"+env_type.lower()

    def get_env(self,trade_env_parameters):
        ischeck = False
        if self.env_name=="env_strategy_train":
            ischeck = True
            env = EnvStrategyTrain(trade_env_parameters)
        elif self.env_name=="env_strategy_test":
            ischeck = True
            env = EnvStrategyTest(trade_env_parameters)
        if not ischeck:
            raise ValueError(f"env_name non exist , env_name:{self.env_name}")
        else:
            return env