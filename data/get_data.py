import datetime
import os

import baostock as bs

import pandas as pd
import akshare as ak

import tushare as ts
from config.config import ConfigJson
from logger.logging_config import logger
import yfinance as yf
from pandas_datareader import data as pdr
yf.pdr_override()

def timestampchange(x):
    return datetime.datetime.strptime(x, '%Y-%m-%d').strftime('%Y%m%d')

def prue_num_code(x):
    return ''.join(e for e in x if e.isdigit())

class GetData:

    def __init__(self,country,start_date,end_date,code_list):
        bs.login()
        config = ConfigJson()
        config.get_account()
        self.tushare_token = config.tushare_token
        ts.set_token(self.tushare_token)  # 设置token，只需设置一次
        self.api = ts.pro_api()  # 初始化接口
        self.country = country.lower()
        self.start_date =  start_date
        self.end_date = end_date
        self.code_list = code_list

    def get_trade_cal(self):
        root_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cachedata')
        file_name = self.country + "_trade_cal_" + self.start_date + "to" + self.end_date + ".csv"
        file_path = os.path.join(root_path,file_name )
        if os.path.exists(file_path):
            trade_cal_data = pd.read_csv(file_path,dtype={'cal_date':'str','is_open':'int64'})


        else:
            if self.country == "us":
                trade_cal_data = self.api.us_tradecal(start_date=self.start_date, end_date=self.end_date)
                if self.end_date > "20220620":
                    trade_cal_data.loc[trade_cal_data['cal_date'] == "20220620", ["is_open"]] = 0
            elif self.country == "zh":
                trade_cal_data = self.api.trade_cal(start_date=self.start_date, end_date=self.end_date)
            else:
                trade_cal_data = pd.DataFrame()
                logger.error(f"this country:{self.country} not support")
            trade_cal_data = trade_cal_data[["cal_date", "is_open"]]

            trade_cal_data.to_csv(file_path,index=False)
        trade_cal_data['cal_date'] = pd.to_datetime(trade_cal_data['cal_date'])
        return trade_cal_data[["cal_date", "is_open"]]

    def _get_data(self,code_list,start_date,end_date):
        if self.country == "us":
            result = pd.DataFrame()
            for code in code_list:
                if code[0] == 'h':
                    code_tmp = '^' + code[1:]
                else:
                    code_tmp = '^' + code

                data = pdr.get_data_yahoo(code_tmp, start=start_date, end=end_date)
                data['code'] = code
                data['date'] = data.index
                result = pd.concat([result, data])
            result['date'] = result['date'].astype(str).apply(timestampchange)
            result['code'] = result['code']
            result['open'] = result['Open'].astype(float)
            result['high'] = result['High'].astype(float)
            result['low'] = result['Low'].astype(float)
            result['close'] = result['Close'].astype(float)
            result['volume'] = result['Volume'].astype(float)
            result = result[['date','code','open','high','low','close','volume']]

        else:
            data_list = []
            for bs_code in code_list:
                if bs_code[0] == '6' or bs_code[0] == '5' or bs_code[0] == 'h':
                    bs_code = 'sh.' + bs_code[-6:]
                else:
                    bs_code = 'sz.' + bs_code[-6:]
                rs = bs.query_history_k_data_plus(bs_code,
                                                  "date,code,open,high,low,close,volume,amount",
                                                  start_date=start_date, end_date=end_date,
                                                  frequency='d', adjustflag="3")

                while (rs.error_code == '0') & rs.next():
                    # 获取一条记录，将记录合并在一起
                    data_list.append(rs.get_row_data())
            result = pd.DataFrame(data_list, columns=rs.fields).sort_values(["date", "code"], ignore_index=True)
            result['date'] = result['date'].apply(timestampchange)
            result['code'] = result['code'].apply(prue_num_code)
            for code in code_list:
                if code[0] == 'h':
                    code_tmp = code[-6:]
                    result.loc[result['code'] == code_tmp, 'code'] = code

            result['open'] = result['open'].astype(float)
            result['high'] = result['high'].astype(float)
            result['low'] = result['low'].astype(float)
            result['close'] = result['close'].astype(float)
            result['volume'] = result['volume'].astype(float)
            result['amount'] = result['amount'].astype(float)
        result = result.sort_values(["code","date"], ignore_index=True)
        return result

    def get_day_trade_data(self):
        start_date = datetime.datetime.strptime(self.start_date, '%Y%m%d').strftime('%Y-%m-%d')
        end_date = datetime.datetime.strptime(self.end_date, '%Y%m%d').strftime('%Y-%m-%d')
        root_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cachedata')
        file_name = self.country + "_trade_data_" + self.start_date + "to" + self.end_date + ".csv"
        file_path = os.path.join(root_path, file_name)
        if os.path.exists(file_path):
            result = pd.read_csv(file_path, dtype={'date': 'str', 'code': 'str','open': 'float', 'high': 'float','low': 'float', 'close': 'float','volume': 'float', 'amount': 'float'})
            # 将 DataFrame 中的 code 列转换为集合
            df_code_set = set(result['code'])

            # 将 codelist 转换为集合
            codelist_set = set(self.code_list)

            # 使用集合差集操作找出 codelist 中未在 DataFrame 中匹配的代码
            unmatched_codes_list = list(codelist_set.difference(df_code_set))
            if len(unmatched_codes_list)>0:
                new_result = self._get_data(code_list=unmatched_codes_list, start_date=start_date, end_date=end_date)
                result = pd.concat([result,new_result])
                result.to_csv(file_path, index=False)

            result = result[result['code'].isin(self.code_list)]

        else:
            result = self._get_data(code_list=self.code_list,start_date=start_date,end_date=end_date)

            result.to_csv(file_path,index=False)

        result = result.sort_values(["code","date"], ignore_index=True)
        return result

