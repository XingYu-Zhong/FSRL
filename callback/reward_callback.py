import numpy as np
from stable_baselines3.common.callbacks import BaseCallback
from torch.utils.tensorboard import SummaryWriter

class RewardLoggerCallback(BaseCallback):
    def __init__(self, verbose: int = 0):
        super().__init__(verbose)
        self.current_rewards = []

    def _on_step(self) -> bool:
        # print(f"self.locals:{self.locals}")
        # print(f"self.locals.get('infos'):{self.locals.get('infos')}")


        info = self.locals.get('infos')[0]

        if info is not None:
            step_reward = info['step_reward']
        else:
            raise ValueError(f"env step function info have problem")
        self.current_rewards.append(step_reward)
        done = info['done']

        if done:
            # Calculate the average reward for the epoch
            avg_reward = np.mean(self.current_rewards)
            self.current_rewards = []
            # Log the average reward to TensorBoard
            print(f'reward/avg_reward：{avg_reward}')
            self.logger.record('reward/avg_reward', avg_reward)
        return True

