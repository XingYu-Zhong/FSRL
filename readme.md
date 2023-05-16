# 📈 FSRL:Financial Strategy Reinforcement Learning.🤖





<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=python,github,pytorch,tensorflow" />
  </a>
</p>


![cat](img/FSRL-cat.png#pic_center)

[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/) 

金融策略强化学习（FSRL）是第一个用于动态切换多种策略的开源框架。🔥

### 概述

FSRL通过强化学习技术让动态切换策略的设想在金融市场上成为了可能，将把多因子模型推进到多策略模型的时代，我们可以将多个策略交给FSRL进行训练，给训练好的模型导入新数据后，模型会在当前数据下自动选择用哪种策略。

![FSRL_process.png](img%2FFSRL_process.png)


FSRL有三层：策略，代理，市场环境层，策略层与市场环境进行交互，提供策略在回测中的数据，并以此作为依据给出奖励，市场环境与代理层进行交互，市场环境层提供观察数据，代理层根据观察数据给出决策动作，市场环境层通过代理的动作和回测的数据计算奖励返回代理层，代理层得到奖励继续优化决策动作，以此行成正向循环。

![FSRL-Architecture.png](img%2FFSRL-Architecture.png)

### 文件结构

整个框架分为几个模块：algomodel，analysis，backtest，env，config，logger，data，mainlab，strategy。

algomodel：

1. 管理RL算法模型，设想可以接入多个方面的算法，比如stable-baselines3，tensorforce，RlegantRL，自己构造的算法库，目前实现了SB3里的算法
2. 可以选择算法以及具体算法参数，设定默认参数

analysis：

1. 负责对已有策略进行分析，目前实现了对比原有当个策略的效果
2. 后续加上可视化分析等等

backtest：

1. 回测框架，目前只实现了中国股票的回测，应该后续可以设计介入第三方的回测库，比如[backtrader](https://github.com/mementum/backtrader)，[qlib](https://github.com/microsoft/qlib)，[quanttrader](https://github.com/letianzj/quanttrader)，[backtesting](https://github.com/kernc/backtesting.py)，自己设计等等
2. 目前没有用到第三方的原因是为了和策略集成所以全部自定义，但是可以实现将回测抽离出来的

env：

1. 这个模块是用于管理RL环境的，包括action，evaluation，observation，reward这几个子模块，分别负责管理agent的动作，计算agent的评估指标，管理agent的观察值，管理agent获得的奖励
2. 通过environment_init.py来管理用户具体使用的环境

config：

1. 将参数放到json文件里，通过这个模块去读取json文件里的参数

logger：

1. 日志设置模块

data：

1. 获取股票基本数据
2. 对基本数据加工获取因子数据

mianlab：

1. 实验训练，加载，测试模型的入口

strategy：

1. 策略实现模块，多个策略放到这里进行实现，去调用回测框架里进行回测 

### Contributors

Thank you!


### Sponsorship

欢迎礼物用于支持FSRL。

Network: USDT-TRC20 网络： USDT-TRC20

![USDT-TRC20.jpg](img%2FUSDT-TRC20.jpg)

## LICENSE

MIT License

**免责声明：我们正在根据麻省理工学院教育许可证共享用于学术目的的代码。此处没有任何财务建议，也不是交易真实货币的建议。请使用常识，并在交易或投资之前始终首先咨询专业人士。**