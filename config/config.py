import json
import os


class ConfigJson:

    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__),'global_config.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        self.mail_host = json_data['global_variables']['mailHost']
        self.mail_user = json_data['global_variables']['mailUser']
        self.mail_pass = json_data['global_variables']['mailPass']
        self.receivers = json_data['global_variables']['receivers']
        if json_data['global_variables']['isTest'] == "True":
            self.is_test = True
        else:
            self.is_test = False

    def get_account(self):
        config_path = os.path.join(os.path.dirname(__file__), 'test_account.json') if self.is_test else os.path.join(
            os.path.dirname(__file__),
            'account.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        self.tushare_token = json_data["tushare"]["token"]
        self.commission_rate = json_data["stock_account"]["commission_rate"]
        self.lowest_commission = json_data["stock_account"]["lowest_commission"]

    def get_mainlab(self,task_name):
        config_path = os.path.join(os.path.dirname(__file__), 'test_mainlab.json') if self.is_test else os.path.join(
            os.path.dirname(__file__),
            'mainlab.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        rlEnvInit =self.trade_env_sys = json_data[task_name]['rlEnvInit']
        self.trade_env_name = rlEnvInit['envName']
        self.trade_env_parameters = rlEnvInit['envParameters']


        algorithm  = json_data[task_name]['algorithm']
        self.algo_sys = algorithm['system'] if 'system' in algorithm else "stable-baselines3"
        if self.algo_sys == "stable-baselines3":
            self.algo_model = algorithm['algorithmModel'] if 'algorithmModel' in algorithm else "PPO"
            alog_parameters = algorithm['algorithmParameters']
            self.alog_parameters = alog_parameters
            self.total_timesteps = int(float(algorithm['totalTimeSteps']))










