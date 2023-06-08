import os

from stable_baselines3.common.vec_env import DummyVecEnv

from algomodel.algo_center import AlgoCenter
from analysis.analysis_center import AnalysisCenter
from callback.reward_callback import RewardLoggerCallback
from config.config import ConfigJson
from env.environment_init import EnvironmentInit
from logger.logging_config import logger
from utiltools.utils import email_server


class MainLab:
    def __init__(self,task_name,env_type,trade_start_time,trade_end_time,load_time_steps = 1e5):
        logger.info(f"lab_name:{task_name},env_type:{env_type},trade_start_time:{trade_start_time},trade_end_time:{trade_end_time} begin")
        self.trade_start_time = trade_start_time
        self.trade_end_time = trade_end_time
        self.task_name = task_name
        self.load_time_steps = load_time_steps
        config_init = ConfigJson()
        config_init.get_mainlab(task_name=task_name)
        self.mainlab_config=config_init
        self.mainlab_config.trade_env_parameters['tradeStartTime']=trade_start_time
        self.mainlab_config.trade_env_parameters['tradeEndTime'] = trade_end_time
        self.mainlab_config.trade_env_parameters['taskName'] = task_name
        self.env_type = env_type.lower()
        if self.env_type=="train" or self.env_type=="load":
            self.train_load_model()
        elif self.env_type=="test":
            self.test_model()
        else:
            raise ValueError(f"config env_sys is not Train or Test, env_sys: {env_type}")


    def get_rl_model(self,env,task_name,is_test=False,path="",is_load = False):
        logger.info(f"self.mainlab_config.alog_parameters:{self.mainlab_config.alog_parameters}")
        algo_center = AlgoCenter(algo_sys=self.mainlab_config.algo_sys, algo_model=self.mainlab_config.algo_model,
                                 algo_parameters_dict=self.mainlab_config.alog_parameters, env=env, task_name=task_name)

        if is_test:
            model = algo_center.get_test_model(path=path)
        elif is_load:
            model = algo_center.get_load_model(path=path,env=env)
        else:
            model = algo_center.get_model()

        return model
    def train_load_model(self):
        reward_callback = RewardLoggerCallback()
        env = DummyVecEnv(
            [lambda: EnvironmentInit(env_name=self.mainlab_config.trade_env_name,env_type=self.env_type).get_env(trade_env_parameters=self.mainlab_config.trade_env_parameters)])

        model = self.get_rl_model(env=env,task_name=self.task_name)
        if self.env_type=="load":
            model = self.get_rl_model(env=env,task_name=self.task_name,path="resultmodel/"+self.task_name,is_load=True)
            model.learn(total_timesteps=int(self.load_time_steps), callback=reward_callback)
        else:
            total_timesteps = self.mainlab_config.total_timesteps
            model.learn(total_timesteps=total_timesteps, callback=reward_callback)
        model_path = os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), "resultmodel"),self.task_name)
        model.save(model_path)
        email_server(emailContext=self.task_name+" model is save",mail_host=self.mainlab_config.mail_host,mail_user=self.mainlab_config.mail_user,mail_pass=self.mainlab_config.mail_pass,receivers=self.mainlab_config.receivers)
        return model


    def test_model(self):
        env = DummyVecEnv(
            [lambda: EnvironmentInit(env_name=self.mainlab_config.trade_env_name,env_type=self.env_type).get_env(trade_env_parameters=self.mainlab_config.trade_env_parameters)])

        model = self.get_rl_model(env=env,task_name=self.task_name,is_test=True,path="resultmodel/"+self.task_name)
        obs = env.reset()
        while True:
            '''
            obs simility
            hist record
            final act = sim * hist recor + action * (1 - sim)
            '''
            action, _states = model.predict(obs)
            print(f'obs:{obs}')
            print(f'action:{action}')
            obs, rewards, done, info = env.step(action)
            if done:
                break
            env.render()
        AnalysisCenter().compare_strategy(country=self.mainlab_config.trade_env_parameters['marketCountry'],start_time=self.trade_start_time,end_time=self.trade_end_time,code_list=self.mainlab_config.trade_env_parameters['codeList'],init_balance=float(self.mainlab_config.trade_env_parameters['balance']),task_name=self.task_name)

        email_server(emailContext=self.task_name + " model is save", mail_host=self.mainlab_config.mail_host,
                     mail_user=self.mainlab_config.mail_user, mail_pass=self.mainlab_config.mail_pass,
                     receivers=self.mainlab_config.receivers)
        return model