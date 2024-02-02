
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
[[[0.00893057 0.24922724 0.15655836 0.0501937  0.07213932 0.0066283
   0.2599888  0.66964643 0.68199022 0.61363435 0.68940389 0.3628068
   1.         0.66935737 0.39708252 0.37408602 0.17137272 0.07677412
   0.         0.0945907 ]
  [0.43236134 0.67005458 0.64205779 0.65246954 0.73952731 0.76518073
   0.91691542 1.         0.76203214 0.54341323 0.46325904 0.22992101
   0.50181658 0.14069139 0.         0.0954667  0.11476265 0.2408934
   0.37419416 0.55292885]
  [0.         0.00865908 0.12334063 0.37766187 0.37733797 0.49369873
   0.52715166 0.68489886 0.56971664 0.36349734 0.42200027 0.56528153
   0.55263041 0.46981744 0.25504684 0.37802197 0.50892007 0.82740373
   1.         0.95998516]
  [0.         0.31478162 0.42948985 0.2181062  0.55830068 0.75500281
   0.89110978 0.25204192 0.38833635 0.85063499 0.46748618 0.24963946
   0.25023157 0.27246872 1.         0.68889083 0.54313806 0.14664947
   0.21950052 0.79913425]
  [0.50089195 0.0740211  0.52348105 0.57615292 0.33596349 0.87781504
   0.44712206 0.17142821 0.62056979 0.55979365 0.35477881 0.82992969
   0.25004437 1.         0.51303895 0.         0.09089925 0.22326024
   0.46195587 0.36336605]]]
"""

action_prompt_hint = """
You should only respond in JSON format as described below 
Response Format: 

{{{{
    "thoughts": {{{{
        "text": "Your trend analysis of the input data",
        "reasoning": "reasons for choosing this strategy",
        "criticism": "critical thinking on strategy selection",
    }}}},
    "actions": {{{{
        "strategy": 'strategy_name', 
        "action_num": strategy_number
    }}}}
}}}}

The strings corresponding to "text", "reasoning", "criticism"in JSON should be described in Chinese.

Do not output any other information and do not contain quotation marks, such as `, \", \' and so on.
Ensure the output can be parsed by Python json.loads.
Don't output in markdown format, something like ```json or ```,just output in the corresponding string format

"""

two_bulin_rsi = """
The output needs to be the value of the corresponding policy from the following dictionary:
\{'bulin_strategy':0,'rsi_strategy':1,'twoma_strategy':2\}
Select a specific number at the time of output
"""

two_bulin_rsi_empty_vwap = """
The output needs to be the value of the corresponding policy from the following dictionary:
\{'bulin_strategy':0,'rsi_strategy':1,'twoma_strategy':2,'empty_strategy':3,'vwap_strategy':4\}
Select a specific number at the time of output
"""