import os

import pandas as pd

import data.factors.mytt_factors as mytt
import data.factors.mytt_plus_factors as mytt_plus
import talib
import numpy as np
from logger.logging_config import logger
# TA_COL_NAME有77个
TA_COL_NAME = ['SMA', 'upper', 'middle', 'lower', 'DEMA', 'MA', 'EMA', 'KAMA', 'MIDPOINT', 'SAR', 'T3', 'TEMA', 'SAREXT', 'WMA', 'ATR', 'NATR', 'TRANGE', 'AD', 'ADOSC', 'OBV', 'HT_DCPERIOD', 'HT_DCPHASE', 'HT_PHASOR_inphase', 'HT_PHASOR_quadrature', 'HT_SINE_sine', 'HT_SINE_leadsine', 'HT_TRENDMODE', 'AVGPRICE', 'MEDPRICE', 'TYPPRICE', 'WCLPRICE', 'ADX', 'ADXR', 'APO', 'AROON_aroondown', 'AROON_aroonup', 'AROONOSC', 'BOP', 'CCI', 'CMO', 'DX', 'MACD_macd', 'MACD_macdsignal', 'MACD_macdhist', 'MACDEXT_macd', 'MACDEXT_macdsignal', 'MACDEXT_macdhist', 'MFI', 'MINUS_DI', 'MINUS_DM', 'MOM', 'PLUS_DI', 'PLUS_DM', 'PPO', 'ROC', 'ROCP', 'ROCR', 'ROCR100', 'RSI', 'STOCH_slowk', 'STOCH_slowd', 'STOCHF_fastk', 'STOCHF_fastd', 'STOCHRSI_fastk', 'STOCHRSI_fastd', 'TRIX', 'ULTOSC', 'WILLR', 'BETA', 'CORREL', 'LINEARREG', 'LINEARREG_ANGLE', 'LINEARREG_INTERCEPT', 'LINEARREG_SLOPE', 'STDDEV', 'TSF', 'VAR']
# MYTT_COL_NAME有52个
MYTT_COL_NAME = ['DIF', 'DEA', 'MACD', 'K', 'D', 'J', 'BIAS1', 'BIAS2', 'BIAS3', 'UPPER', 'MID', 'LOWER', 'PSY', 'PSYMA', 'CCI', 'ATR', 'BBI', 'PDI', 'MDI', 'ADX', 'ADXR', 'UP', 'DOWN', 'TRIX', 'TRMA', 'VR', 'EMV', 'MAEMV', 'DPO', 'MADPO', 'AR', 'BR', 'DFMA_DIF', 'DFMA_DMA', 'MTM', 'MTMMA', 'MASS', 'MA_MASS', 'ROC', 'MAROC', 'EMA1', 'EMA2', 'OBV', 'MFI', 'ASI', 'ASIT', 'XSII_TD1', 'XSII_TD2', 'XSII_TD3', 'XSII_TD4','sar_x','SarX']

class GetFactors:
    def __init__(self,task_name,data,obs_factor_name_list,fields_dict={"mytt":[],"ta":[]}):
        self.task_name = task_name
        self.obs_factor_name_list = obs_factor_name_list
        self.data = data
        self.fields_dict= fields_dict
        self.result_data = data
        logger.info(f"GetFactors init finish")

    def get_factors(self,code,start_time,end_time):
        if self.obs_factor_name_list==[]:
            logger.info(f"obs_factor_name_list is empty")
            return self.result_data
        root_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cachedata')
        file_name =code+"_"+start_time+"to"+end_time+ "_factors.csv"
        file_path = os.path.join(root_path,file_name )
        if os.path.exists(file_path):
            self.result_data = pd.read_csv(file_path)
            self.result_data = self.result_data.apply(pd.to_numeric, errors='ignore')
            logger.info(f"factors_file:{file_name} is exists")
        else:
            logger.info(f"factors_file:{file_name} is not exists")
            if "ta" in self.obs_factor_name_list:
                logger.info(f"begin calculate ta factors")
                ta_data = self.get_ta_factors(data=self.data, fields=self.fields_dict['ta'])
                logger.info(f"finish calculate ta factors")
                self.result_data = pd.concat([self.result_data, ta_data], axis=1)
            if "mytt" in self.obs_factor_name_list:
                logger.info(f"begin calculate mytt factors")
                mytt_data = self.get_mytt_factors(data=self.data, fields=self.fields_dict['mytt'])
                logger.info(f"finish calculate mytt factors")
                self.result_data = pd.concat([self.result_data, mytt_data], axis=1)
            self.result_data = self.result_data.loc[:,~self.result_data.columns.duplicated()]
            self.result_data = self.result_data.fillna(0)
            self.result_data.to_csv(file_path,index=False)
        return self.result_data

    def get_mytt_factors(self, data, fields=[]):
        if fields == []:
            fields = MYTT_COL_NAME
        close= data['close'].values
        high =  data['high'].values
        low =  data['low'].values

        #MACD：计算股票的MACD指标，包括DIF、DEA和MACD三个指标。
        DIF,DEA,MACD = mytt.MACD(CLOSE=close,SHORT=12,LONG=26,M=9)

        #KDJ：计算股票的KDJ指标，包括K、D和J三个指标。
        K,D,J = mytt.KDJ(CLOSE=close,LOW=low,HIGH=high,N=9,M1=3,M2=3)

        # BIAS：计算股票的BIAS指标，包括BIAS1、BIAS2和BIAS3三个指标。
        BIAS1, BIAS2, BIAS3 = mytt.BIAS(CLOSE=close, L1=6, L2=12, L3=24)

        # BOLL：计算股票的BOLL指标，包括UPPER、MID和LOWER三个指标。
        UPPER, MID, LOWER = mytt.BOLL(CLOSE=close, N=20, P=2)

        # PSY：计算股票的PSY指标，包括PSY和PSYMA两个指标。
        PSY, PSYMA = mytt.PSY(CLOSE=close, N=12, M=6)

        # CCI：计算股票的CCI指标。
        CCI = mytt.CCI(CLOSE=close, HIGH=high, LOW=low, N=14)

        # ATR：计算股票的ATR指标。
        ATR = mytt.ATR(CLOSE=close, HIGH=high, LOW=low, N=20)

        # BBI：计算股票的BBI指标。
        BBI = mytt.BBI(CLOSE=close, M1=3, M2=6, M3=12, M4=20)

        # DMI：计算股票的DMI指标，包括PDI、MDI、ADX和ADXR四个指标。
        PDI, MDI, ADX, ADXR = mytt.DMI(CLOSE=close, HIGH=high, LOW=low, M1=14, M2=6)

        # TAQ：计算股票的TAQ指标，包括UP、MID和DOWN三个指标。
        UP, MID, DOWN = mytt.TAQ(HIGH=high, LOW=low, N=20)

        # KTN：计算股票的KTN指标，包括UPPER、MID和LOWER三个指标。
        UPPER, MID, LOWER = mytt.KTN(CLOSE=close, HIGH=high, LOW=low, N=20, M=10)

        # TRIX：计算股票的TRIX指标，包括TRIX和TRMA两个指标。
        TRIX, TRMA = mytt.TRIX(CLOSE=close, M1=12, M2=20)

        # VR：计算股票的VR指标。
        VR = mytt.VR(CLOSE=close, VOL=data['volume'].values, M1=26)

        # EMV：计算股票的EMV指标，包括EMV和MAEMV两个指标。
        EMV, MAEMV = mytt.EMV(HIGH=high, LOW=low, VOL=data['volume'].values, N=14, M=9)

        # DPO：计算股票的DPO指标，包括DPO和MADPO两个指标。
        DPO, MADPO = mytt.DPO(CLOSE=close, M1=20, M2=10, M3=6)

        # BRAR：计算股票的BRAR指标，包括AR和BR两个指标。
        AR, BR = mytt.BRAR(OPEN=data['open'].values, CLOSE=close, HIGH=high, LOW=low, M1=26)

        #DFMA：计算平行线差指标，包括DIF和DMA两个指标。
        DFMA_DIF,DFMA_DMA = mytt.DFMA(CLOSE=close,N1=10,N2=50,M=10)

        #MTM：计算动量指标，包括MTM和MTMMA两个指标。
        MTM,MTMMA = mytt.MTM(CLOSE=close,N=12,M=6)

        #MASS：计算梅斯线指标，包括MASS和MA_MASS两个指标。
        MASS,MA_MASS = mytt.MASS(HIGH=high,LOW=low,N1=9,N2=25,M=6)

        #ROC：计算变动率指标，包括ROC和MAROC两个指标。
        ROC,MAROC = mytt.ROC(CLOSE=close,N=12,M=6)

        #EXPMA：计算EMA指数平均数指标，包括EMA1和EMA2两个指标。
        EMA1,EMA2 = mytt.EXPMA(CLOSE=close,N1=12,N2=50)

        #OBV：计算OBV指标。
        OBV = mytt.OBV(CLOSE=close,VOL=data['volume'].values)

        #MFI：计算MFI指标。
        MFI = mytt.MFI(CLOSE=close,HIGH=high,LOW=low,VOL=data['volume'].values,N=14)

        #ASI：计算振动升降指标，包括ASI和ASIT两个指标。
        ASI,ASIT = mytt.ASI(OPEN=data['open'].values,CLOSE=close,HIGH=high,LOW=low,M1=26,M2=10)

        #XSII：计算薛斯通道II指标，包括TD1、TD2、TD3和TD4四个指标。
        TD1,TD2,TD3,TD4 = mytt.XSII(CLOSE=close,HIGH=high,LOW=low,N=102,M=7)

        #SAR(HIGH, LOW, N=10, S=2, M=20): 抛物转向指标
        sar_x = mytt_plus.SAR(HIGH=high,LOW=low,N=10,S=2,M=20)

        #TDX_SAR(High, Low, iAFStep=2, iAFLimit=20): 通达信SAR指标
        SarX = mytt_plus.TDX_SAR(High=high, Low=low, iAFStep=2, iAFLimit=20)

        #将所有计算出的因子保存到DataFrame并返回
        factors_df = pd.DataFrame({
            'DIF': DIF, 'DEA': DEA, 'MACD': MACD, 'K': K, 'D': D,
            'J': J, 'BIAS1': BIAS1, 'BIAS2': BIAS2, 'BIAS3': BIAS3,
            'UPPER': UPPER, 'MID': MID, 'LOWER': LOWER, 'PSY': PSY,
            'PSYMA': PSYMA, 'CCI': CCI, 'ATR': ATR, 'BBI': BBI,
            'PDI': PDI, 'MDI': MDI, 'ADX': ADX, 'ADXR': ADXR,
            'UP': UP, 'DOWN': DOWN, 'TRIX': TRIX, 'TRMA': TRMA,
            'VR': VR, 'EMV': EMV, 'MAEMV': MAEMV, 'DPO': DPO,
            'MADPO': MADPO, 'AR': AR, 'BR': BR, 'DFMA_DIF': DFMA_DIF,
            'DFMA_DMA': DFMA_DMA, 'MTM': MTM, 'MTMMA': MTMMA, 'MASS': MASS,
            'MA_MASS': MA_MASS, 'ROC': ROC, 'MAROC': MAROC, 'EMA1': EMA1,
            'EMA2': EMA2, 'OBV': OBV, 'MFI': MFI, 'ASI': ASI,
            'ASIT': ASIT, 'XSII_TD1': TD1, 'XSII_TD2': TD2,
            'XSII_TD3': TD3, 'XSII_TD4': TD4,'sar_x':sar_x,'SarX':SarX
        }, index=data.index)

        return factors_df[fields]


    def get_ta_factors(self, data, fields=[]):

        # 一、重叠研究（overlap studies）
        # 1.简单移动平均指标SMA
        # 参数说明：talib.SMA(a,b)
        # a:要计算平均数的序列；b:计算平均线的周期。表示计算a的b日移动平均
        if fields == []:
            fields = TA_COL_NAME
        close = data['close'].values
        SMA = talib.SMA(close, 5)

        # 2.布林线BBANDS
        # 参数说明：talib.BBANDS(close, timeperiod, matype)
        # close:收盘价；timeperiod:周期；matype:平均方法(bolling线的middle线 = MA，用于设定哪种类型的MA)
        # MA_Type: 0=SMA, 1=EMA, 2=WMA, 3=DEMA, 4=TEMA, 5=TRIMA, 6=KAMA, 7=MAMA, 8=T3 (Default=SMA)
        upper, middle, lower = talib.BBANDS(close, 5, matype=talib.MA_Type.EMA)

        # 3. DEMA 双移动平均线:DEMA = 2*EMA-EMA(EMA)
        # 参数说明：talib.DEMA(close, timeperiod = 30)
        DEMA = talib.DEMA(close, timeperiod=30)

        # 4. MA
        # 参数说明：MA(close, timeperiod = 30, matype=0)
        # close:收盘价；timeperiod:周期；matype:计算平均线方法
        MA = talib.MA(close, timeperiod=30, matype=0)

        # 5. EMA
        # 参数说明：EMA = talib.EMA(np.array(close), timeperiod=6)
        # close:收盘价；timeperiod:周期；matype:计算平均线方法
        EMA = talib.EMA(np.array(close), timeperiod=6)

        # 6.KAMA：考夫曼的自适应移动平均线
        # 参数说明：KAMA = talib.KAMA(close, timeperiod = 30)
        KAMA = talib.KAMA(close, timeperiod=30)

        # 7. MIDPRICE：阶段中点价格
        # talib.MIDPOINT(close, timeperiod)
        # 参数说明：close:收盘价；timeperiod:周期；
        # MIDPOINT = talib.MIDPOINT(close, timeperiod=14)

        # 8.SAR：抛物线指标
        # SAR(high, low, acceleration=0, maximum=0)
        # 参数说明：high：最高价；low:最低价；acceleration：加速因子；maximum：极点价
        SAR = talib.SAR(data['high'].values, data['low'].values, acceleration=0, maximum=0)

        # 9.MIDPRICE：阶段中点价格（Midpoint Price over period）
        # talib.MIDPOINT(close, timeperiod=14)
        # 参数说明：close:收盘价；timeperiod:周期；
        MIDPOINT = talib.MIDPOINT(close, timeperiod=14)

        # 10. T3:三重移动平均线
        # talib.T3(close, timeperiod=5, vfactor=0)
        # 参数说明：close:收盘价；timeperiod:周期；vfactor: va 系数，当va=0时，T3就是三重移动平均线；va=1时，就是DEMA
        T3 = talib.T3(close, timeperiod=5, vfactor=0)

        # 11.TEMA：三重指数移动平均线
        # talib.TEMA(close, timeperiod = 30)
        # 参数说明：close:收盘价；timeperiod:周期；
        TEMA = talib.TEMA(close, timeperiod=30)

        # 12.SAREXT:SAR的抛物面扩展
        # talib.SAREXT(high_p, low_p, startvalue=0, offsetonreverse=0, accelerationinitlong=0, accelerationlong=0, accelerationmaxlong=0, accelerationinitshort=0, accelerationshort=0, accelerationmaxshort=0)
        SAREXT = talib.SAREXT(data['high'].values, data['low'].values, startvalue=0, offsetonreverse=0,
                              accelerationinitlong=0, accelerationlong=0, accelerationmaxlong=0,
                              accelerationinitshort=0, accelerationshort=0, accelerationmaxshort=0)

        # 13.WMA：移动加权平均法
        # talib.WMA(close, timeperiod = 30)
        # 参数说明：close:收盘价；timeperiod:周期；
        WMA = talib.WMA(close, timeperiod=30)

        # 二、 波动量指标
        # 1.ATR：真实波动幅度均值
        # ATR(high, low, close, timeperiod=14)
        # 参数说明：high:最高价；low:最低价；close:收盘价,timeperiod:周期
        ATR = talib.ATR(data['high'].values, data['low'].values, close, timeperiod=14)

        # 2.NATR:归一化波动幅度均值
        # NATR(high, low, close, timeperiod=14)
        # 参数说明：high:最高价；low:最低价；close:收盘价,timeperiod:周期
        NATR = talib.NATR(data['high'].values, data['low'].values, close, timeperiod=14)

        # 3.TRANGE：真正的范围
        # TRANGE(high, low, close)
        # 参数说明：high:最高价；low:最低价；close:收盘价
        TRANGE = talib.TRANGE(data['high'].values, data['low'].values, close)

        # 三、 量价指标
        # 1. AD:量价指标
        # AD(high, low, close, volume)
        # 参数说明：high:最高价；low:最低价；close:收盘价,volume:成交量
        AD = talib.AD(data['high'], data['low'], close, data['volume'])

        # 2.ADOSC:震荡指标
        # ADOSC(high, low, close, volume, fastperiod=3, slowperiod=10)
        # 参数说明：high:最高价；low:最低价；close:收盘价,volume:成交量; fastperiod:快周期； slowperiod：慢周期
        ADOSC = talib.ADOSC(data['high'], data['low'], close, data['volume'], fastperiod=3, slowperiod=10)

        # 3.OBV：能量潮
        # OBV(close, volume)
        # 参数说明：close:收盘价,volume:成交量
        OBV = talib.OBV(close, data['volume'])

        # 三、 周期指标
        # 1.HT_DCPERIOD：希尔伯特变换-主导周期
        # HT_DCPERIOD(close)
        # 参数说明：close:收盘价
        HT_DCPERIOD = talib.HT_DCPERIOD(close)

        # 2.HT_DCPHASE：希尔伯特变换-主导循环阶段
        # HT_DCPHASE(close)
        # 参数说明：close:收盘价
        HT_DCPHASE = talib.HT_DCPHASE(close)

        # 3.HT_PHASOR：希尔伯特变换-希尔伯特变换相量分量
        # inphase, quadrature = HT_PHASOR(close)
        # 参数说明：close:收盘价
        HT_PHASOR_inphase, HT_PHASOR_quadrature = talib.HT_PHASOR(close)

        # 4.HT_SINE：希尔伯特变换-正弦波
        # sine, leadsine = HT_SINE(close)
        # 参数说明：close:收盘价
        HT_SINE_sine, HT_SINE_leadsine = talib.HT_SINE(close)

        # 5.HT_TRENDMODE：希尔伯特变换-趋势与周期模式
        # integer = HT_TRENDMODE(close)
        # 参数说明：close:收盘价
        HT_TRENDMODE = talib.HT_TRENDMODE(close)

        # 四、价格变化函数
        # 1. AVGPRICE：平均价格函数
        # real = AVGPRICE(open, high, low, close)
        AVGPRICE = talib.AVGPRICE(data['open'].values, data['high'].values, data['low'].values, close)

        # 2. MEDPRICE:中位数价格
        # real = MEDPRICE(high, low)
        # 参数说明：high:最高价；low:最低价；
        MEDPRICE = talib.MEDPRICE(data['high'].values, data['low'].values)

        # 3. TYPPRICE ：代表性价格
        # real = TYPPRICE(high, low, close)
        # 参数说明：high:最高价；low:最低价；close：收盘价
        TYPPRICE = talib.TYPPRICE(data['high'].values, data['low'].values, close)

        # 4. WCLPRICE ：加权收盘价
        # real = WCLPRICE(high, low, close)
        # 参数说明：high:最高价；low:最低价；close：收盘价
        WCLPRICE = talib.WCLPRICE(data['high'].values, data['low'].values, close)

        # 五、 动量指标
        # 1. ADX：平均趋向指数
        # real = ADX(high, low, close, timeperiod=14)
        # 参数说明：high:最高价；low:最低价；close：收盘价；timeperiod：时间周期
        ADX = talib.ADX(data['high'].values, data['low'].values, close, timeperiod=14)

        # 2. ADXR：平均趋向指数的趋向指数
        # real = ADXR(high, low, close, timeperiod=14)
        # 参数说明：high:最高价；low:最低价；close：收盘价；timeperiod：时间周期
        ADXR = talib.ADXR(data['high'].values, data['low'].values, close, timeperiod=14)

        # 3. APO ：价格震荡指数
        # real = APO(close, fastperiod=12, slowperiod=26, matype=0)
        # 参数说明：close：收盘价；fastperiod:快周期； slowperiod：慢周期
        APO = talib.APO(close, fastperiod=12, slowperiod=26, matype=0)

        # 4. AROON ：阿隆指标
        # aroondown, aroonup = AROON(high, low, timeperiod=14)
        # 参数说明：high:最高价；low:最低价；close：收盘价；timeperiod：时间周期
        AROON_aroondown, AROON_aroonup = talib.AROON(data['high'].values, data['low'].values, timeperiod=14)

        # 5.AROONOSC ：阿隆振荡
        # real = AROONOSC(high, low, timeperiod=14)
        # 参数说明：high:最高价；low:最低价；close：收盘价；timeperiod：时间周期
        AROONOSC = talib.AROONOSC(data['high'].values, data['low'].values, timeperiod=14)

        # 6. BOP ：均势指标
        # real = BOP(open, high, low, close)
        # 参数说明：high:最高价；low:最低价；close：收盘价；timeperiod：时间周期
        BOP = talib.BOP(data['open'].values, data['high'].values, data['low'].values, close)

        # 7. CCI ：顺势指标
        # real = CCI(high, low, close, timeperiod=14)
        # 参数说明：high:最高价；low:最低价；close：收盘价；timeperiod：时间周期
        CCI = talib.CCI(data['high'].values, data['low'].values, close, timeperiod=14)

        # 8. CMO ：钱德动量摆动指标
        # real = CMO(close, timeperiod=14)
        # 参数说明：close：收盘价；timeperiod：时间周期
        CMO = talib.CMO(close, timeperiod=14)

        # 9. DX ：动向指标或趋向指标
        # real = DX(high, low, close, timeperiod=14)
        # 参数说明：high:最高价；low:最低价；close：收盘价；timeperiod：时间周期
        DX = talib.DX(data['high'].values, data['low'].values, close, timeperiod=14)

        # 10. MACD:平滑异同移动平均线
        # macd, macdsignal, macdhist = MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
        # 参数说明：high:最高价；low:最低价；close：收盘价；fastperiod:快周期； slowperiod：慢周期
        MACD_macd, MACD_macdsignal, MACD_macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)

        # 11. MACDEXT :MACD延伸
        # macd, macdsignal, macdhist = MACDEXT(close, fastperiod=12, fastmatype=0, slowperiod=26, slowmatype=0, signalperiod=9, signalmatype=0)
        # 参数说明：high:最高价；low:最低价；close：收盘价；timeperiod：时间周期
        MACDEXT_macd, MACDEXT_macdsignal, MACDEXT_macdhist = talib.MACDEXT(close, fastperiod=12, fastmatype=0,
                                                                           slowperiod=26, slowmatype=0, signalperiod=9,
                                                                           signalmatype=0)

        # 12. MFI ：资金流量指标
        # real = MFI(high, low, close, volume, timeperiod=14)
        # 参数说明：high:最高价；low:最低价；close：收盘价；timeperiod：时间周期
        MFI = talib.MFI(data['high'].values, data['low'].values, close, data['volume'], timeperiod=14)

        # 13. MINUS_DI：DMI 中的DI指标 负方向指标
        # real = MINUS_DI(high, low, close, timeperiod=14)
        # 参数说明：high:最高价；low:最低价；close：收盘价；timeperiod：时间周期
        MINUS_DI = talib.MINUS_DI(data['high'].values, data['low'].values, close, timeperiod=14)

        # 14. MINUS_DM：上升动向值
        # real = MINUS_DM(high, low, timeperiod=14)
        # 参数说明：high:最高价；low:最低价；close：收盘价；timeperiod：时间周期
        MINUS_DM = talib.MINUS_DM(data['high'].values, data['low'].values, timeperiod=14)

        # 六、波动率指标
        # 1.MOM： 上升动向值
        # real = MOM(close, timeperiod=10)
        # 参数说明：close：收盘价；timeperiod：时间周期
        MOM = talib.MOM(close, timeperiod=10)

        # 2.PLUS_DI
        # real = PLUS_DI(high, low, close, timeperiod=14)
        # 参数说明：high:最高价；low:最低价；close：收盘价；timeperiod：时间周期
        PLUS_DI = talib.PLUS_DI(data['high'].values, data['low'].values, close, timeperiod=14)

        # 3.PLUS_DM
        # real = PLUS_DM(high, low, timeperiod=14)
        # 参数说明：high:最高价；low:最低价；close：收盘价；timeperiod：时间周期
        PLUS_DM = talib.PLUS_DM(data['high'].values, data['low'].values, timeperiod=14)

        # 4. PPO： 价格震荡百分比指数
        # real = PPO(close, fastperiod=12, slowperiod=26, matype=0)
        # 参数说明：close：收盘价；timeperiod：时间周期，fastperiod:快周期； slowperiod：慢周期
        PPO = talib.PPO(close, fastperiod=12, slowperiod=26, matype=0)

        # 5.ROC：变动率指标
        # real = ROC(close, timeperiod=10)
        # 参数说明：close：收盘价；timeperiod：时间周期
        ROC = talib.ROC(close, timeperiod=10)

        # 6. ROCP：变动百分比
        # real = ROCP(close, timeperiod=10)
        # 参数说明：close：收盘价；timeperiod：时间周期
        ROCP = talib.ROCP(close, timeperiod=10)

        # 7.ROCR ：变动百分率
        # real = ROCR(close, timeperiod=10)
        # 参数说明：close：收盘价；timeperiod：时间周期
        ROCR = talib.ROCR(close, timeperiod=10)

        # 8. ROCR100 ：变动百分率（*100）
        # real = ROCR100(close, timeperiod=10)
        # 参数说明：close：收盘价；timeperiod：时间周期
        ROCR100 = talib.ROCR100(close, timeperiod=10)

        # 9. RSI：相对强弱指数
        # real = RSI(close, timeperiod=14)
        # 参数说明：close：收盘价；timeperiod：时间周期
        RSI = talib.RSI(close, timeperiod=14)

        # 10.STOCH ：随机指标,俗称KD
        # slowk, slowd = STOCH(high, low, close, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
        # 参数说明：high:最高价；low:最低价；close：收盘价；fastk_period：N参数, slowk_period：M1参数, slowk_matype：M1类型, slowd_period:M2参数, slowd_matype：M2类型
        # #matype: 0=SMA, 1=EMA, 2=WMA, 3=DEMA, 4=TEMA, 5=TRIMA, 6=KAMA, 7=MAMA, 8=T3 (Default=SMA)
        STOCH_slowk, STOCH_slowd = talib.STOCH(data['high'].values, data['low'].values, close, fastk_period=9,
                                               slowk_period=3, slowk_matype=1, slowd_period=3, slowd_matype=1)

        # 11. STOCHF ：快速随机指标
        # fastk, fastd = STOCHF(high, low, close, fastk_period=5, fastd_period=3, fastd_matype=0)
        STOCHF_fastk, STOCHF_fastd = talib.STOCHF(data['high'].values, data['low'].values, close, fastk_period=5,
                                                  fastd_period=3, fastd_matype=0)

        # 12.STOCHRSI：随机相对强弱指数
        # fastk, fastd = STOCHRSI(high, low, close, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
        STOCHRSI_fastk, STOCHRSI_fastd = talib.STOCHF(data['high'].values, data['low'].values, close, fastk_period=5,
                                                      fastd_period=3, fastd_matype=0)

        # 13.TRIX：1-day Rate-Of-Change (ROC) of a Triple Smooth EMA
        # real = TRIX(close, timeperiod=30)
        TRIX = talib.TRIX(close, timeperiod=30)

        # 14.ULTOSC：终极波动指标
        # real = ULTOSC(high, low, close, timeperiod1=7, timeperiod2=14, timeperiod3=28)
        ULTOSC = talib.ULTOSC(data['high'].values, data['low'].values, close, timeperiod1=7, timeperiod2=14,
                              timeperiod3=28)

        # 15.WILLR ：威廉指标
        # real = WILLR(high, low, close, timeperiod=14)
        WILLR = talib.WILLR(data['high'].values, data['low'].values, close, timeperiod=14)

        # 七、Statistic Functions 统计学指标
        # 1. BETA：β系数也称为贝塔系数
        # real = BETA(high, low, timeperiod=5)
        BETA = talib.BETA(data['high'].values, data['low'].values, timeperiod=5)

        # 2. CORREL ：皮尔逊相关系数
        # real = CORREL(high, low, timeperiod=30)
        CORREL = talib.CORREL(data['high'].values, data['low'].values, timeperiod=30)

        # 3.LINEARREG ：线性回归
        # real = LINEARREG(close, timeperiod=14)
        LINEARREG = talib.LINEARREG(close, timeperiod=14)

        # 4.LINEARREG_ANGLE ：线性回归的角度
        # real = LINEARREG_ANGLE(close, timeperiod=14)
        LINEARREG_ANGLE = talib.LINEARREG_ANGLE(close, timeperiod=14)

        # 5. LINEARREG_INTERCEPT ：线性回归截距
        # real = LINEARREG_INTERCEPT(close, timeperiod=14)
        LINEARREG_INTERCEPT = talib.LINEARREG_INTERCEPT(close, timeperiod=14)

        # 6.LINEARREG_SLOPE：线性回归斜率指标
        # real = LINEARREG_SLOPE(close, timeperiod=14)
        LINEARREG_SLOPE = talib.LINEARREG_SLOPE(close, timeperiod=14)

        # 7.STDDEV ：标准偏差
        # real = STDDEV(close, timeperiod=5, nbdev=1)
        STDDEV = talib.STDDEV(close, timeperiod=5, nbdev=1)

        # 8.TSF：时间序列预测
        # real = TSF(close, timeperiod=14)
        TSF = talib.TSF(close, timeperiod=14)

        # 9. VAR：方差
        # real = VAR(close, timeperiod=5, nbdev=1)
        VAR = talib.VAR(close, timeperiod=5, nbdev=1)

        results_pd = pd.DataFrame({'SMA': SMA, 'upper': upper, 'middle': middle, 'lower': lower, 'DEMA': DEMA,
              'MA': MA, 'EMA': EMA, 'KAMA': KAMA, 'MIDPOINT': MIDPOINT, 'SAR': SAR,
              'T3': T3, 'TEMA': TEMA, 'SAREXT': SAREXT, 'WMA': WMA, 'ATR': ATR,
              'NATR': NATR, 'TRANGE': TRANGE, 'AD': AD, 'ADOSC': ADOSC, 'OBV': OBV,
              'HT_DCPERIOD': HT_DCPERIOD, 'HT_DCPHASE': HT_DCPHASE,'HT_PHASOR_inphase': HT_PHASOR_inphase,
              'HT_PHASOR_quadrature': HT_PHASOR_quadrature,'HT_SINE_sine': HT_SINE_sine,
              'HT_SINE_leadsine': HT_SINE_leadsine, 'HT_TRENDMODE': HT_TRENDMODE,
              'AVGPRICE': AVGPRICE, 'MEDPRICE': MEDPRICE,'TYPPRICE': TYPPRICE,
              'WCLPRICE': WCLPRICE,'ADX': ADX,'ADXR': ADXR,'APO': APO,'AROON_aroondown': AROON_aroondown,
              'AROON_aroonup': AROON_aroonup,'AROONOSC': AROONOSC,'BOP': BOP,'CCI': CCI,'CMO': CMO,'DX': DX,
              'MACD_macd': MACD_macd,'MACD_macdsignal': MACD_macdsignal,'MACD_macdhist': MACD_macdhist,
              'MACDEXT_macd': MACDEXT_macd,'MACDEXT_macdsignal': MACDEXT_macdsignal,
              'MACDEXT_macdhist': MACDEXT_macdhist,'MFI': MFI,'MINUS_DI': MINUS_DI,'MINUS_DM': MINUS_DM,
              'MOM': MOM,'PLUS_DI': PLUS_DI,'PLUS_DM': PLUS_DM,'PPO': PPO,'ROC': ROC,'ROCP': ROCP,'ROCR': ROCR,
              'ROCR100': ROCR100,'RSI': RSI,'STOCH_slowk': STOCH_slowk,'STOCH_slowd': STOCH_slowd,
              'STOCHF_fastk': STOCHF_fastk,'STOCHF_fastd': STOCHF_fastd,'STOCHRSI_fastk': STOCHRSI_fastk,
              'STOCHRSI_fastd': STOCHRSI_fastd,'TRIX': TRIX,'ULTOSC': ULTOSC,'WILLR': WILLR,
              'BETA': BETA,'CORREL': CORREL,'LINEARREG': LINEARREG,'LINEARREG_ANGLE': LINEARREG_ANGLE,
              'LINEARREG_INTERCEPT': LINEARREG_INTERCEPT,'LINEARREG_SLOPE': LINEARREG_SLOPE,'STDDEV': STDDEV,
              'TSF': TSF,'VAR': VAR},index=data.index)


        return results_pd[fields]