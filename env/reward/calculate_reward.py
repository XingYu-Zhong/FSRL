import numpy as np


class CalReward:
    def __init__(self,reward_id):
        self.reward_id = reward_id

    def calculate_reward(self, params):
        if self.reward_id == "rank_reward":
            return self.rank_reward(params)
        # 在此处添加其他计算奖励的方法

    def rank_reward(self, params):
        scores = params["scores"]
        action = params["action"]
        cap = params["cap"]

        # 将策略得分与策略索引组合
        indexed_scores = list(enumerate(scores))

        # 对得分进行排序
        ranked_scores = sorted(indexed_scores, key=lambda x: x[1], reverse=True)

        # 给策略分配排名
        ranks = [0] * len(scores)
        for rank, (index, _) in enumerate(ranked_scores):
            ranks[index] = rank + 1

        # 获取当前策略的排名
        rank = ranks[action]

        # 设定排名奖励,长度与scores相同且逐级减半
        rank_rewards = [1.0 / (2 ** i) for i in range(len(scores))]

        reward = rank_rewards[rank - 1]

        # 如果当前策略的比例大于50%且当前策略排名不是第一，则让奖励归零
        if cap.count(action) > len(cap) * 0.3 and len(cap)==6:
            if cap[-1]==action:
                if rank == 2:
                    reward = reward * 0.4
                elif rank == 3:
                    reward = reward * 0.2
            else:
                if rank == 2:
                    reward = reward * 0.8
                elif rank == 3:
                    reward = reward * 0.4



        return reward

    def composite_strategy_score(self, df, risk_free_rate=0.02, weights=None):
        if weights is None:
            weights = [0.09, 0.06, 0.65, 0.05, 0.05]  # 默认权重分配

        # 计算收益率
        df['return'] = df['value'].pct_change()

        # 年化收益率和年化波动率
        annualized_return = np.mean(df['return']) * 252
        annualized_volatility = np.std(df['return']) * np.sqrt(252)
        if annualized_volatility == 0:
            return 0

        # 计算夏普比率
        sharpe_ratio = (annualized_return - risk_free_rate) / annualized_volatility

        # 计算最大回撤
        df['cummax'] = df['value'].cummax()
        df['drawdown'] = df['value'] / df['cummax'] - 1
        max_drawdown = df['drawdown'].min()

        # 计算总收益率
        total_return = (df['value'].iloc[-1] / df['value'].iloc[0]) - 1

        indicators = [sharpe_ratio, max_drawdown, total_return, annualized_return, annualized_volatility]

        # 计算综合评分
        score = sum(w * i for w, i in zip(weights, indicators))

        return score