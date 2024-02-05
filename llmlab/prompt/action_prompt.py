
action_prompt_begin = """
You, as an experienced financial strategist, are sensitive to data and you can choose the right strategy based on current trend data.

--The data given to you is some open-high close-low fitted Technical Factor Indicators for the past period of time, and since there are too many of them, the data is downscaled by PAC.
--To better see the trend of the data, we normalize the data after PAC downscaling.
--Please go ahead and choose which strategy you should be using at the moment based on the trend.

you'll need to follow these steps:

1. Analyze the current trend based on data from the past period.
2. Analyze which strategy is suitable for the current data trend based on the current trend and the strategy summary.
3. Combine the chosen strategy to find the corresponding number.
4. You need to give thought to why you are using this strategy.
5. You need to give an analysis of current data trends.

"""

action_prompt_example = """
Here is some examples about actions choosing:
Input:
open          high           low         close       volume  \
317  12958.650391  12958.730469  12734.860352  12759.150391  142330000.0
318  12756.120117  12857.730469  12751.509766  12837.330078  175110000.0
319  12835.530273  12937.190430  12835.530273  12907.940430  103530000.0
320  12908.620117  12968.790039  12906.429688  12922.019531  103240000.0
321  12920.580078  12976.360352  12919.980469  12959.709961  100000000.0
322  12953.200195  13180.400391  12953.129883  13177.679688  163130000.0
323  13177.150391  13221.269531  13166.250000  13194.099609  163610000.0
324  13192.969727  13253.509766  13170.190430  13252.759766  161650000.0
325  13253.509766  13289.080078  13231.450195  13232.620117  392620000.0
326  13231.940430  13269.709961  13208.629883  13239.129883  147120000.0
327  13238.450195  13238.450195  13123.379883  13170.190430  131660000.0
328  13170.790039  13190.019531  13112.929688  13124.620117  124860000.0
329  13124.400391  13124.469727  13017.419922  13046.139648  122060000.0
330  13045.990234  13099.910156  13002.769531  13080.730469  129930000.0
331  13082.620117  13243.860352  13082.389648  13241.629883  122080000.0
332  13242.089844  13264.980469  13194.330078  13197.730469  129280000.0
333  13195.389648  13212.639648  13069.259766  13126.209961  141540000.0
334  13125.990234  13151.570312  13032.669922  13145.820312  136250000.0
335  13147.940430  13224.490234  13147.780273  13212.040039  171190000.0
336  13211.360352  13297.110352  13153.690430  13264.490234  108790000.0
Ouput:
\{
    "thoughts": \{
        "text": "根据提供的数据，近期股市呈现出上升趋势，特别是在最后几个交易日内，收盘价有稳定的上升。这表明市场情绪正面，投资者信心增强。",
        "reasoning": "选择双均线策略(twoma_strategy)是因为这种策略适用于趋势跟踪，特别是在当前市场显示出明显上升趋势时。双均线策略通过比较短期和长期均线的位置来生成买卖信号，适合当前的市场条件。",
        "criticism": "虽然RSI策略和布林带策略也是有效的交易策略，但RSI策略更适合识别过买或过卖条件，布林带策略适用于振荡市场。鉴于当前数据显示一个明确的上升趋势，双均线策略更能直接利用这种趋势进行交易。"
    \},
    "actions": \{
        "strategy": "twoma_strategy",
        "action_num": 2
    \}
\}
"""

action_prompt_hint = """
You should only respond in JSON format as described below 
Response Format: 

{{{{
    "thoughts": {{{{
        "text": "Your trend analysis of the input data",
        "reasoning": "reasons for choosing this strategy",
        "criticism": "It is only necessary to think critically about how these strategies compare with the current data, without considering other",
    }}}},
    "actions": {{{{
        "strategy": 'strategy_name', 
        "action_num": strategy_number
    }}}}
}}}}

The strings corresponding to "text", "reasoning", "criticism"in JSON should be described in en.

Do not output any other information and do not contain quotation marks, such as `, \", \' and so on.
Ensure the output can be parsed by Python json.loads.
Don't output in markdown format, something like ```json or ```,just output in the corresponding string format

"""

two_bulin_rsi_output_actions = """
The output needs to be the value of the corresponding policy from the following dictionary:
\{'bulin_strategy':0,'rsi_strategy':1,'twoma_strategy':2\}
Select a specific number at the time of output
"""

two_bulin_rsi_empty_vwap_output_actions = """
The output needs to be the value of the corresponding policy from the following dictionary:
\{'bulin_strategy':0,'rsi_strategy':1,'twoma_strategy':2,'empty_strategy':3,'vwap_strategy':4\}
Select a specific number at the time of output
"""