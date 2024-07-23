# 📈 FSRL：金融戦略強化学習 🤖

<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=python,github,pytorch,tensorflow" />
  </a>
</p>

<div align="center">
    <img src="img/FSRL-cat.png" width="500">
</div>

[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)

*この文書を他の言語で読む: [English](readme.md), [中文](readme_zh.md).*

FSRL（金融戦略強化学習）は、複数の戦略を動的に切り替えることができる最初のオープンソースフレームワークです。🔥

### 📘 概要

FSRLは強化学習技術を用いて、金融市場で戦略を動的に切り替える可能性を提供します。この進歩により、私たちは多因子モデルの時代から多戦略モデルの時代に突入します。複数の戦略でFSRLを訓練し、モデルが訓練された後、新しいデータをモデルに入力します。モデルは現在のデータに基づいてどの戦略を使用するかを自動的に選択します。

![FSRL_process.png](img%2FFSRL_process.png)

FSRLは、戦略、エージェント、および市場環境の3つの層で構成されています。戦略層は市場環境と対話し、バックテスト中の戦略データを提供し、これに基づいて報酬を与えます。市場環境はエージェント層と対話し、エージェント層に観察データを提供して意思決定を行います。市場環境はエージェントの行動とバックテストデータに基づいて報酬を計算し、エージェント層に報酬を返します。エージェント層は報酬を受け取った後、意思決定を最適化し続け、正のループを形成します。

![FSRL-Architecture.png](img%2FFSRL-Architecture.png)

### 📁 ファイル構造

フレームワーク全体は、algomodel、analysis、backtest、env、config、logger、data、mainlab、strategyのいくつかのモジュールに分かれています。

algomodel：

1. 強化学習アルゴリズムモデルを管理し、stable-baselines3、tensorforce、ElegantRL、自己構築のアルゴリズムライブラリなど、さまざまな分野のアルゴリズムを組み込むことができます。現在、SB3のアルゴリズムが実装されています。
2. アルゴリズムの選択と特定のアルゴリズムパラメータの設定を許可し、デフォルトパラメータを設定できます。

analysis：

1. 既存の戦略を分析する責任があります。現在、元の単一戦略の効果との比較が実装されています。
2. 将来的には、視覚化分析などの機能が追加されます。

backtest：

1. バックテストフレームワーク。現在、中国とアメリカの株式市場のバックテストが実装されています。将来的には、[backtrader](https://github.com/mementum/backtrader)、[qlib](https://github.com/microsoft/qlib)、[quanttrader](https://github.com/letianzj/quanttrader)、[backtesting](https://github.com/kernc/backtesting.py)などのサードパーティのバックテストライブラリを統合できます。
2. これまでサードパーティを使用していない理由は、戦略との統合のためにすべてがカスタマイズされているためです。ただし、将来的にはバックテストを抽象化することが可能です。

env：

1. このモジュールは、RL環境を管理するために使用されます。アクション、評価、観察、および報酬のサブモジュールが含まれており、エージェントの行動を管理し、エージェントの評価指標を計算し、エージェントの観察を管理し、エージェントが受け取る報酬を管理します。
2. environment_init.pyを通じて、ユーザーが使用する特定の環境を管理します。

config：

1. パラメータはjsonファイルに保存され、このモジュールはjsonファイルのパラメータを読み取ります。

logger：

1. ログ設定モジュール。

data：

1. 基本的な株式データを取得します。
2. 基本データを処理してファクターデータを取得します。

mainlab：

1. 実験のトレーニング、ロード、およびテストモデルのエントリーポイント。

strategy：

1. 戦略実装モジュール。ここで複数の戦略が実装され、バックテストフレームワークでバックテストに使用されます。

### 💻 インストール
python 3.8を使用

まず、`requirements.txt`に記載されているPythonライブラリをインストールします。

```shell
pip install -r requirements.txt
```
その後、ta_libをインストールします。特定の環境に応じて適切なta_libインストールを選択してください。
 
https://ta-lib.github.io/ta-lib-python/install.html



### 🚀 クイックスタート
1. configディレクトリでglobal_config.jsonを設定し、主にメール情報やその他の設定を行います。
2. Tushare公式サイトでアカウントを登録し、トークンを取得し、configディレクトリのtest_account.jsonでバックテストシステムの手数料率と最低手数料を設定します。
3. configディレクトリのtest_mainlab.jsonでデータ、環境、モデルなどを設定します。
4. FSRLのトレーニングを開始します。
```shell
python -u run.py --task_name=hDJIADQN\
                 --env_type=train\
                 --start_time=20101201\
                 --end_time=20210101
```
5. トレーニングが完了したら、モデルをテストします。
```shell
python -u run.py --task_name=hDJIADQN\
                 --env_type=test\
                 --start_time=20201201\
                 --end_time=20230101
```
llmを使用する


```shell
python -u run.py --task_name=h000905llm5Strategy --env_type=llm --start_time=20201201 --end_time=20230101 --proxy=10809
```

## tensorboard
```shell
tensorboard --logdir=tensorboard_logs
```

### 👥 貢献者

より多くの人々が参加できることを歓迎します。ありがとうございます！

### 💰 スポンサーシップ

FSRLをサポートするためのギフトを歓迎します。

ネットワーク: USDT-TRC20

<img src="img/USDT-TRC20.jpg" width="150" height="150">

## 📝 ライセンス

MITライセンス

**免責事項：このコードはMIT教育ライセンスの下で学術目的で共有しています。これは財務アドバイスではなく、実際の通貨を取引するための提案でもありません。取引や投資を行う前に常に最善の判断を使用し、必要に応じて専門家に相談してください。**
