import os

from stable_baselines3 import *

from logger.logging_config import logger


class AlgoCenter:
    def __init__(self,algo_sys,algo_model,algo_parameters_dict,env,task_name):
        self.algo_sys = algo_sys
        self.algo_model = algo_model
        self.algo_parameters_dict = algo_parameters_dict
        self.env = env
        tensorboard_log = os.path.join("tensorboard_logs", task_name)  # 设置日志存储路径
        self.tensorboard_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), tensorboard_log)


    def get_model(self):
        if self.algo_sys == "stable-baselines3":
            model = self.stable_baselines3_algo(self.algo_model,self.algo_parameters_dict,self.env)
        else:
            raise ValueError(f"not support this algo system:{self.algo_sys}")
        return model

    def get_test_model(self,path):
        if self.algo_sys == "stable-baselines3":
            str_algo = self.algo_model+'.load("'+path+'")'
            model = eval(str_algo)
        else:
            raise ValueError(f"not support this algo system:{self.algo_sys}")
        return model
    def get_load_model(self,path,env):
        if self.algo_sys == "stable-baselines3":
            env = env
            str_algo = self.algo_model+'.load("'+path+'",env=env)'
            model = eval(str_algo)
        else:
            raise ValueError(f"not support this algo system:{self.algo_sys}")
        return model
    def stable_baselines3_algo(self,algo_model,alog_parameters,env):
        logger.info(f"algo_model:{algo_model},alog_parameters:{alog_parameters}")
        if algo_model == "PPO":
            self.policy = alog_parameters['policy'] if 'policy' in alog_parameters else "MlpPolicy"
            self.learning_rate = float(
                alog_parameters['learning_rate']) if 'learning_rate' in alog_parameters else float("3e-4")
            self.n_steps = int(alog_parameters['n_steps']) if 'n_steps' in alog_parameters else 2048
            self.batch_size = int(alog_parameters['batch_size']) if 'batch_size' in alog_parameters else 64
            self.n_epochs = int(alog_parameters['n_epochs']) if 'n_epochs' in alog_parameters else 10
            self.gamma = float(alog_parameters['gamma']) if 'gamma' in alog_parameters else 0.99
            self.gae_lambda = float(alog_parameters['gae_lambda']) if 'gae_lambda' in alog_parameters else 0.95
            self.clip_range = float(alog_parameters['clip_range']) if 'clip_range' in alog_parameters else 0.2
            self.clip_range_vf = alog_parameters['clip_range_vf'] if 'clip_range_vf' in alog_parameters else None
            self.normalize_advantage = alog_parameters.get('normalize_advantage', 'True') == 'True'
            self.ent_coef = float(alog_parameters['ent_coef']) if 'ent_coef' in alog_parameters else 0.0
            self.vf_coef = float(alog_parameters['vf_coef']) if 'vf_coef' in alog_parameters else 0.5
            self.max_grad_norm = float(
                alog_parameters['max_grad_norm']) if 'max_grad_norm' in alog_parameters else 0.5
            alog_parameters['use_sde'] = alog_parameters['use_sde'] == "True"
            self.use_sde = alog_parameters['use_sde'] if 'use_sde' in alog_parameters else False
            self.sde_sample_freq = int(
                alog_parameters['sde_sample_freq']) if 'sde_sample_freq' in alog_parameters else -1
            self.target_kl = alog_parameters['target_kl'] if 'target_kl' in alog_parameters else None
            self.tensorboard_log = alog_parameters[
                'tensorboard_log'] if 'tensorboard_log' in alog_parameters else self.tensorboard_path
            self.policy_kwargs = alog_parameters['policy_kwargs'] if 'policy_kwargs' in alog_parameters else None
            self.verbose = int(alog_parameters['verbose']) if 'verbose' in alog_parameters else 0
            self.seed = int(alog_parameters['seed']) if 'seed' in alog_parameters else None
            self.device = alog_parameters['device'] if 'device' in alog_parameters else 'auto'
            self.init_setup_model = alog_parameters.get('_init_setup_model', 'True') == 'True'

            model = PPO(
                        policy =self.policy,
                        n_steps=self.n_steps,
                        batch_size=self.batch_size,
                        n_epochs=self.n_epochs,
                        gamma=self.gamma,
                        gae_lambda=self.gae_lambda,
                        clip_range=self.clip_range,
                        clip_range_vf=self.clip_range_vf,
                        normalize_advantage=self.normalize_advantage,
                        ent_coef=self.ent_coef,
                        vf_coef=self.vf_coef,
                        max_grad_norm=self.max_grad_norm,
                        use_sde=self.use_sde,
                        sde_sample_freq=self.sde_sample_freq,
                        target_kl=self.target_kl,
                        tensorboard_log=self.tensorboard_log,
                        policy_kwargs=self.policy_kwargs,
                        verbose=self.verbose,
                        seed=self.seed,
                        device=self.device,
                        _init_setup_model=self.init_setup_model,
                        env=env)
        elif algo_model == "A2C":
            self.policy = alog_parameters['policy'] if 'policy' in alog_parameters else "MlpPolicy"
            self.learning_rate = float(
                alog_parameters['learning_rate']) if 'learning_rate' in alog_parameters else float("7e-4")
            self.n_steps = int(alog_parameters['n_steps']) if 'n_steps' in alog_parameters else 5
            self.gamma = float(alog_parameters['gamma']) if 'gamma' in alog_parameters else 0.99
            self.gae_lambda = float(alog_parameters['gae_lambda']) if 'gae_lambda' in alog_parameters else 1
            self.normalize_advantage = alog_parameters.get('normalize_advantage', True) == 'True'

            self.ent_coef = float(alog_parameters['ent_coef']) if 'ent_coef' in alog_parameters else 0.0
            self.vf_coef = float(alog_parameters['vf_coef']) if 'vf_coef' in alog_parameters else 0.5
            self.max_grad_norm = float(
                alog_parameters['max_grad_norm']) if 'max_grad_norm' in alog_parameters else 0.5
            self.rms_prop_eps = float(
                alog_parameters['rms_prop_eps']) if 'rms_prop_eps' in alog_parameters else 1e-5
            self.use_rms_prop = alog_parameters.get('use_rms_prop', True) == 'True'
            self.use_sde = alog_parameters['use_sde'] if 'use_sde' in alog_parameters else False
            self.sde_sample_freq = int(
                alog_parameters['sde_sample_freq']) if 'sde_sample_freq' in alog_parameters else -1
            self.tensorboard_log = alog_parameters[
                'tensorboard_log'] if 'tensorboard_log' in alog_parameters else self.tensorboard_path
            self.policy_kwargs = alog_parameters['policy_kwargs'] if 'policy_kwargs' in alog_parameters else None
            self.verbose = int(alog_parameters['verbose']) if 'verbose' in alog_parameters else 0
            self.seed = int(alog_parameters['seed']) if 'seed' in alog_parameters else None
            self.device = alog_parameters['device'] if 'device' in alog_parameters else 'auto'
            self.init_setup_model = alog_parameters.get('_init_setup_model', True) == 'True'

            model = A2C(policy=self.policy,
                        learning_rate=self.learning_rate,
                        n_steps=self.n_steps,
                        gamma=self.gamma,
                        gae_lambda=self.gae_lambda,
                        normalize_advantage=self.normalize_advantage,
                        ent_coef=self.ent_coef,
                        vf_coef=self.vf_coef,
                        max_grad_norm=self.max_grad_norm,
                        rms_prop_eps = self.rms_prop_eps,
                        use_rms_prop = self.use_rms_prop,
                        use_sde=self.use_sde,
                        sde_sample_freq=self.sde_sample_freq,
                        tensorboard_log=self.tensorboard_log,
                        policy_kwargs=self.policy_kwargs,
                        verbose=self.verbose,
                        seed=self.seed,
                        device=self.device,
                        _init_setup_model=self.init_setup_model,
                        env=env)
        elif algo_model == "SAC":
            self.policy = alog_parameters['policy'] if 'policy' in alog_parameters else "MlpPolicy"
            self.learning_rate = float(
                alog_parameters['learning_rate']) if 'learning_rate' in alog_parameters else float("3e-4")
            self.buffer_size = int(alog_parameters['buffer_size']) if 'buffer_size' in alog_parameters else int(
                "1000000")
            self.learning_starts = int(
                alog_parameters['learning_starts']) if 'learning_starts' in alog_parameters else int("1024")
            self.batch_size = int(alog_parameters['batch_size']) if 'batch_size' in alog_parameters else int("256")
            self.tau = float(alog_parameters['tau']) if 'tau' in alog_parameters else float("0.005")
            self.gamma = float(alog_parameters['gamma']) if 'gamma' in alog_parameters else float("0.99")
            self.train_freq = int(alog_parameters['train_freq']) if 'train_freq' in alog_parameters else int("10")
            self.gradient_steps = int(
                alog_parameters['gradient_steps']) if 'gradient_steps' in alog_parameters else int("1")
            self.action_noise = alog_parameters['action_noise'] if 'action_noise' in alog_parameters else None
            self.replay_buffer_class = alog_parameters[
                'replay_buffer_class'] if 'replay_buffer_class' in alog_parameters else None
            self.replay_buffer_kwargs = alog_parameters[
                'replay_buffer_kwargs'] if 'replay_buffer_kwargs' in alog_parameters else None
            self.optimize_memory_usage = alog_parameters.get('optimize_memory_usage', 'False') == 'True'

            self.ent_coef = alog_parameters['ent_coef'] if 'ent_coef' in alog_parameters else "auto"
            self.target_update_interval = int(
                alog_parameters['target_update_interval']) if 'target_update_interval' in alog_parameters else int(
                "1")
            self.target_entropy = alog_parameters[
                'target_entropy'] if 'target_entropy' in alog_parameters else "auto"
            self.use_sde = alog_parameters.get('use_sde', 'False') == 'True'

            self.sde_sample_freq = int(
                alog_parameters['sde_sample_freq']) if 'sde_sample_freq' in alog_parameters else int("-1")
            self.use_sde_at_warmup = alog_parameters.get('use_sde_at_warmup', 'False') == 'True'
            self.tensorboard_log = alog_parameters[
                'tensorboard_log'] if 'tensorboard_log' in alog_parameters else self.tensorboard_path
            self.policy_kwargs = alog_parameters['policy_kwargs'] if 'policy_kwargs' in alog_parameters else None
            self.verbose = int(alog_parameters['verbose']) if 'verbose' in alog_parameters else int("0")
            self.seed = alog_parameters['seed'] if 'seed' in alog_parameters else None
            self.device = alog_parameters['device'] if 'device' in alog_parameters else "auto"
            self.init_setup_model = alog_parameters.get('_init_setup_model', 'True') == 'True'


            model = SAC(policy=self.policy,
                        env=env,
                        learning_rate=self.learning_rate,
                        buffer_size=self.buffer_size,
                        learning_starts=self.learning_starts,
                        batch_size=self.batch_size,
                        tau=self.tau,
                        gamma=self.gamma,
                        train_freq=self.train_freq,
                        gradient_steps=self.gradient_steps,
                        action_noise=self.action_noise,
                        replay_buffer_class=self.replay_buffer_class,
                        replay_buffer_kwargs=self.replay_buffer_kwargs,
                        optimize_memory_usage=self.optimize_memory_usage,
                        ent_coef=self.ent_coef,
                        target_update_interval=self.target_update_interval,
                        target_entropy=self.target_entropy,
                        use_sde=self.use_sde,
                        sde_sample_freq=self.sde_sample_freq,
                        use_sde_at_warmup=self.use_sde_at_warmup,
                        tensorboard_log=self.tensorboard_log,
                        policy_kwargs=self.policy_kwargs,
                        verbose=self.verbose,
                        seed=self.seed,
                        device=self.device,
                        _init_setup_model=self.init_setup_model
                        )
        elif algo_model == "DQN":
            self.policy = alog_parameters['policy'] if 'policy' in alog_parameters else "MlpPolicy"
            self.learning_rate = float(
                alog_parameters['learning_rate']) if 'learning_rate' in alog_parameters else float("1e-4")
            self.buffer_size = int(alog_parameters['buffer_size']) if 'buffer_size' in alog_parameters else int(
                "1000000")
            self.learning_starts = int(
                alog_parameters['learning_starts']) if 'learning_starts' in alog_parameters else int("50000")
            self.batch_size = int(alog_parameters['batch_size']) if 'batch_size' in alog_parameters else int("256")
            self.tau = float(alog_parameters['tau']) if 'tau' in alog_parameters else float("1")
            self.gamma = float(alog_parameters['gamma']) if 'gamma' in alog_parameters else float("0.99")
            self.train_freq = int(alog_parameters['train_freq']) if 'train_freq' in alog_parameters else int("4")
            self.gradient_steps = int(
                alog_parameters['gradient_steps']) if 'gradient_steps' in alog_parameters else int("1")
            self.replay_buffer_class = alog_parameters[
                'replay_buffer_class'] if 'replay_buffer_class' in alog_parameters else None
            self.replay_buffer_kwargs = alog_parameters[
                'replay_buffer_kwargs'] if 'replay_buffer_kwargs' in alog_parameters else None
            self.optimize_memory_usage = alog_parameters.get('optimize_memory_usage', 'False') == 'True'

            self.target_update_interval = int(
                alog_parameters['target_update_interval']) if 'target_update_interval' in alog_parameters else 10000
            self.exploration_fraction = float(alog_parameters['exploration_fraction']) if 'exploration_fraction' in alog_parameters else 0.1
            self.exploration_initial_eps = float(alog_parameters['exploration_initial_eps']) if 'exploration_initial_eps' in alog_parameters else 1.0
            self.exploration_final_eps = float(alog_parameters['exploration_final_eps']) if 'exploration_final_eps' in alog_parameters else 0.05
            self.max_grad_norm = float(alog_parameters['max_grad_norm']) if 'max_grad_norm' in alog_parameters else 10
            self.tensorboard_log = alog_parameters[
                'tensorboard_log'] if 'tensorboard_log' in alog_parameters else self.tensorboard_path
            self.policy_kwargs = alog_parameters['policy_kwargs'] if 'policy_kwargs' in alog_parameters else None
            self.verbose = int(alog_parameters['verbose']) if 'verbose' in alog_parameters else int("0")
            self.seed = alog_parameters['seed'] if 'seed' in alog_parameters else None
            self.device = alog_parameters['device'] if 'device' in alog_parameters else "auto"
            self.init_setup_model = alog_parameters.get('_init_setup_model', 'True') == 'True'

            model = DQN(policy=self.policy,
                        env=env,
                        learning_rate=self.learning_rate,
                        buffer_size=self.buffer_size,
                        learning_starts=self.learning_starts,
                        batch_size=self.batch_size,
                        tau=self.tau,
                        gamma=self.gamma,
                        train_freq=self.train_freq,
                        gradient_steps=self.gradient_steps,
                        replay_buffer_class=self.replay_buffer_class,
                        replay_buffer_kwargs=self.replay_buffer_kwargs,
                        optimize_memory_usage=self.optimize_memory_usage,
                        target_update_interval=self.target_update_interval,
                        exploration_fraction=self.exploration_fraction ,
                        exploration_initial_eps=self.exploration_initial_eps ,
                        exploration_final_eps = self.exploration_final_eps ,
                        max_grad_norm = self.max_grad_norm ,

                        tensorboard_log=self.tensorboard_log,
                        policy_kwargs=self.policy_kwargs,
                        verbose=self.verbose,
                        seed=self.seed,
                        device=self.device,
                        _init_setup_model=self.init_setup_model)

        else:
            raise ValueError(f"not support this algo model:{algo_model}")


        return model
