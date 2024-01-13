# 📈 FSRL：金融策略强化学习 🤖

<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=python,github,pytorch,tensorflow" />
  </a>
</p>

<div align="center">
    <img src="img/FSRL-cat.png" width="500">
</div>

[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)

*此文档其他语言版本： [English](readme.md), [中文](readme_zh.md).*

金融策略强化学习（FSRL）是首个能动态切换多种策略的开源框架。🔥

### 📘 概述

FSRL运用强化学习技术实现在金融市场上动态切换策略，从而将多因子模型时代推进到多策略模型时代。我们可以将多个策略交给FSRL进行训练，模型训练完成后，将新数据导入模型，模型会自动选择在当前数据下应使用哪种策略。

![FSRL_process.png](img%2FFSRL_process.png)

FSRL由三层构成：策略层，代理层，以及市场环境层。策略层与市场环境互动，提供策略在回测中的数据，并以此作为给出奖励的依据。市场环境与代理层互动，提供观察数据，代理层根据观察数据做出决策动作。市场环境根据代理的动作和回测数据计算奖励，并将奖励返回给代理层。代理层在得到奖励后，继续优化决策动作，从而形成一个正向循环。

![FSRL-Architecture.png](img%2FFSRL-Architecture.png)

### 📁 文件结构

整个框架分为几个模块：algomodel，analysis，backtest，env，config，logger，data，mainlab，strategy。

algomodel：

1. 负责管理强化学习算法模型，可以接入多个类型的算法，例如stable-baselines3，tensorforce，ElegantRL，以及自己构建的算法库。目前已经实现了SB3里的算法。
2. 可以选择算法以及设定具体的算法参数，默认参数可以进行设定。

analysis：

1. 负责分析现有策略，目前已经实现了与原有单个策略效果的对比。
2. 之后将会增加可视化分析等功能。

backtest：

1. 回测框架，目前已经为中国和美国股票市场的回测实现，未来可以设计接入第三方的回测库，例如[backtrader](https://github.com/mementum/backtrader)，[qlib](https://github.com/microsoft/qlib)，[quanttrader](https://github.com/letianzj/quanttrader)，[backtesting](https://github.com/kernc/backtesting.py)以及自定义设计等等。
2. 目前并未使用第三方库，这是为了和策略集成所以全部自定义，但是未来可以实现将回测抽离出来。

env：

1. 这个模块用于管理强化学习环境，包括action，evaluation，observation，reward这几个子模块，分别负责管理代理的动作，计算代理的评估指标，管理代理的观察值，以及管理代理所获得的奖励。
2. 通过environment_init.py管理用户所使用的具体环境。

config：

1. 将参数放到json文件里，通过这个模块读取json文件中的参数。

logger：

1. 日志设置模块。

data：

1. 获取股票基本数据。
2. 加工基本数据，获得因子数据。

mainlab：

1. 实验训练、加载、测试模型的入口。

strategy：

1. 策略实现模块，将多个策略实现后放在这里，然后调用回测框架进行回测。

### 💻 安装

首先，安装`requirements.txt`中列出的Python库。
```python
pip install -r requirements.txt
```
接下来，安装ta_lib。根据您的具体环境选择合适的ta_lib安装。

https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib

### 🚀 快速开始
1.在config目录中，设置global_config.json，主要是配置您的电子邮件信息和其他设置。
2.在Tushare官网注册账号，获取您的token，然后在config目录中的test_account.json中配置回测系统的佣金率和最低佣金。
3.在config目录中的test_mainlab.json中，配置您的数据、环境、模型等。
4.开始训练FSRL。
```shell
python -u run.py --task_name=hDJIADQN --env_type=train --start_time=20101201 --end_time=20210101
```
5.训练完成后，测试模型。
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
### 👥 贡献者

欢迎更多人能参与进来，感谢！

### 💰 赞助

欢迎用礼物来支持FSRL。

网络： USDT-TRC20

<img src="img/USDT-TRC20.jpg" width="150" height="150">

## 📝 许可证

MIT许可证

**免责声明：我们正在根据麻省理工学院教育许可证分享代码，供学术目的使用。此处并无任何财务建议，也不是交易真实货币的建议。请在交易或投资前始终首先使用常识，并咨询专业人士。**
