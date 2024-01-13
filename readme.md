# 📈 FSRL: Financial Strategy Reinforcement Learning 🤖

<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=python,github,pytorch,tensorflow" />
  </a>
</p>

<div align="center">
    <img src="img/FSRL-cat.png" width="500">
</div>

[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)

*Read this in other languages: [English](readme.md), [中文](readme_zh.md).*

FSRL (Financial Strategy Reinforcement Learning) is the first open-source framework capable of dynamic switching among multiple strategies.🔥

### 📘 Overview

FSRL employs reinforcement learning techniques to allow the possibility of dynamically switching strategies in the financial market. This advancement ushers us into the era of multi-strategy models from the multi-factor model era. We can train FSRL with multiple strategies, and once the model is trained, we can input new data into the model. The model will then automatically select which strategy to use based on the current data.

![FSRL_process.png](img%2FFSRL_process.png)

FSRL consists of three layers: Strategy, Agent, and Market Environment. The Strategy layer interacts with the Market Environment, provides the strategy data during backtesting, and gives rewards based on this. The Market Environment interacts with the Agent layer, providing observation data for the Agent layer to make decision actions. The Market Environment calculates rewards based on the Agent's actions and backtest data and returns the rewards to the Agent layer. After receiving the rewards, the Agent layer continues to optimize the decision actions, thus forming a positive loop.

![FSRL-Architecture.png](img%2FFSRL-Architecture.png)

### 📁 File Structure

The entire framework is divided into several modules: algomodel, analysis, backtest, env, config, logger, data, mainlab, strategy.

algomodel:

1. Manages the reinforcement learning algorithm models and can incorporate algorithms from various fields, such as stable-baselines3, tensorforce, ElegantRL, and self-built algorithm libraries. Currently, the algorithms in SB3 have been implemented.
2. Allows the selection of algorithms and the setting of specific algorithm parameters, with default parameters that can be set.

analysis:

1. Responsible for analyzing existing strategies. Currently, it has implemented the comparison with the effects of the original single strategy.
2. Visualization analysis and other functions will be added in the future.

backtest:

1. Backtest framework. Currently, backtesting for the Chinese and American stock markets has been implemented. In the future, third-party backtesting libraries can be integrated, such as [backtrader](https://github.com/mementum/backtrader), [qlib](https://github.com/microsoft/qlib), [quanttrader](https://github.com/letianzj/quanttrader), [backtesting](https://github.com/kernc/backtesting.py), and so on.
2. The reason for not using a third party so far is for integration with the strategy, so everything is customized. However, in the future, it will be possible to abstract backtesting.

env:

1. This module is used to manage the RL environment. It includes the action, evaluation, observation, and reward submodules, which are responsible for managing the agent's actions, calculating the agent's evaluation indicators, managing the agent's observations, and managing the rewards received by the agent.
2. The specific environment used by the user is managed through environment_init.py.

config:

1. Parameters are stored in a json file, and this module reads the parameters in the json file.

logger:

1. Log setup module.

data:

1. Get basic stock data.
2. Process basic data to obtain factor data.

mainlab:

1. The entry point for experimental training, loading, and testing models.

strategy:

1. Strategy implementation module. Multiple strategies are implemented here and then used for backtesting in the backtest framework.

### 💻 Installation

Firstly, install the Python libraries listed in the `requirements.txt`.

```shell
pip install -r requirements.txt
```
Afterwards, install ta_lib. Make sure to select the appropriate ta_lib installation according to your specific environment.
 
https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
### 🚀 Quick Start
1.Configure global_config.json in the config directory, mainly to set up your email information and other settings.
2.Register an account on the official Tushare website, retrieve your token, and then configure the commission rate and minimum commission for the backtest system in test_account.json located in the config directory.
3.Configure your data, environment, model, etc. in test_mainlab.json, also located in the config directory.
4.Begin training FSRL.
```shell
python -u run.py --task_name=hDJIADQN\
                 --env_type=train\
                 --start_time=20101201\
                 --end_time=20210101
```
5.After training is completed, test the model.
```shell
python -u run.py --task_name=hDJIADQN\
                 --env_type=test\
                 --start_time=20201201\
                 --end_time=20230101
```
## tensorboard
```shell
tensorboard --logdir=tensorboard_logs
```

### 👥 Contributors

Welcome more people can participate in,Thank you!

### 💰 Sponsorship

Welcome gifts to support FSRL.

Network: USDT-TRC20

<img src="img/USDT-TRC20.jpg" width="150" height="150">

## 📝 License

MIT License

**Disclaimer: We are sharing this code for academic purposes under the MIT educational license. This is not financial advice, nor a suggestion to trade real currency. Always use your best judgment before trading or investing, and consult a professional if necessary.**
