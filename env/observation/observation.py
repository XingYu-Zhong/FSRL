import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler

from data.get_factors import GetFactors

MAX_ACCOUNT_BALANCE = 2147483647
MAX_NUM_SHARES = 2147483647
MAX_SHARE_PRICE = 5000
class Observation:
    def __init__(self,task_name,code_list,data,obs_day_num=20,obs_factor_num=5,normalize_type="minmax",obs_factor_name_list=[],obs_pca_num=1):
        self.task_name = task_name
        self.obs_day_num = obs_day_num
        self.obs_factor_num = obs_factor_num
        self.obs_factor_name_list = obs_factor_name_list
        self.code_list = code_list
        self.data = data
        self.normalize_type = normalize_type
        self.obs_pca_num = obs_pca_num


    def normalize_data(self,data,normalize_type="minmax"):
        """
        对数据进行归一化处理，将数据缩放到0到1之间
        :param data: 需要归一化的数据，可以是列表、数组或DataFrame
        :return: 归一化后的数据，与输入数据类型相同
        """
        max_number = 2147483647
        if normalize_type =="minmax":
            if isinstance(data, list) or isinstance(data, np.ndarray):
                # 对于列表或数组，使用sklearn中的MinMaxScaler进行归一化

                scaler = MinMaxScaler()
                normalized_data = scaler.fit_transform(data)
            elif isinstance(data, pd.DataFrame):
                # 对于DataFrame，使用apply函数对每一列进行归一化处理
                normalized_data = data.apply(lambda x: (x - x.min()) / (x.max() - x.min()))
            else:
                raise TypeError("不支持的数据类型")
        elif normalize_type == "bignum":
            if isinstance(data, list) or isinstance(data, np.ndarray):
                # 对于列表或数组，使用sklearn中的MinMaxScaler进行归一化

                normalized_data = data/max_number
            elif isinstance(data, pd.DataFrame):
                # 对于DataFrame，使用apply函数对每一列进行归一化处理
                normalized_data = data.apply(lambda x: x/max_number)
            else:
                raise TypeError("不支持的数据类型")
        else:
            normalized_data = data
        return normalized_data

    def init_obs(self):
        result_df = pd.DataFrame()
        for code in self.code_list:
            df = self.data[self.data["code"]==code]
            # 重置索引
            df = df.reset_index(drop=True)
            start_time = df.iloc[0]['date']
            end_time = df.iloc[-1]['date']
            df = df[["open", "high", "low", "close", "volume"]]#过滤code和date
            df = GetFactors(task_name=self.task_name, data=df, obs_factor_name_list=self.obs_factor_name_list).get_factors(
                start_time=start_time,end_time=end_time,code=code)
            df['code'] = code#把code加回来
            result_df = pd.concat([result_df,df],axis=0)
        # 重置索引
        result_df = result_df.reset_index(drop=True)
        return result_df

    # 处理数据
    def process_columns(self,df):
        for column in df.columns:
            # 检查字段值的shape
            shape = df[column].iloc[0].shape
            if len(shape) > 0 and shape[0] == 2:
                # 合并两列为一列
                df[column] = df[column].apply(lambda x: np.mean(x))
        return df

    def get_obs(self, current_step, df=pd.DataFrame()):
        # 提取code字段并存储
        code_series = df['code']

        # 选择数值列
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        # 删除非数值列
        df = df[numeric_cols]
        df = self.normalize_data(data=df, normalize_type=self.normalize_type)
        df = self.process_columns(df)
        df = df.iloc[:, :self.obs_factor_num]

        column_name_list = df.columns.tolist()
        column_name_list = list(set(column_name_list))

        # 将code字段添加回df
        df['code'] = code_series
        pca = PCA(n_components=self.obs_pca_num)  # 创建PCA实例
        scaler = MinMaxScaler()  # 创建一个MinMaxScaler实例
        obs_list_tmp = []
        for code in self.code_list:
            code_df = df[df["code"] == str(code)]
            # 重置索引
            code_df = code_df.reset_index(drop=True)
            # 提取需要的数据
            data = code_df.iloc[current_step - self.obs_day_num: current_step][column_name_list].values
            if data.shape[0] > 1:  # 确保有足够的数据进行PCA
                data = pca.fit_transform(data)  # PCA降维
            data = scaler.fit_transform(data)
            obs_list_tmp.append(data.ravel())  # 由于每个数
        # 转换为Numpy数组
        obs_array = np.array(obs_list_tmp)
        return obs_array


