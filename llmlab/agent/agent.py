

import re
from typing import Any, Optional
from llmlab.llm.lc_openai import LangChainLLM
from llmlab.prompt.strategy_prompt import *
from llmlab.prompt.action_prompt import *
import json
class TradeAgent:
    def __init__(self,llm_api_key,llm_model,strategy_id) -> None:
        self.context = None
        self.llm_api_key = llm_api_key
        self.lc_llm = LangChainLLM(openai_api_key=llm_api_key,model=llm_model)
        if strategy_id == "two_bulin_rsi":
            strategy_summary = two_bulin_rsi
            actions_prompt = two_bulin_rsi_output_actions
        elif strategy_id =="two_bulin_rsi_empty_vwap":
            strategy_summary = two_bulin_rsi_empty_vwap
            actions_prompt = two_bulin_rsi_empty_vwap_output_actions
        else:
            raise ValueError("未知的策略ID 请检查策略ID是否正确。")

        self.strategy_summary = strategy_summary
        self.actions_prompt = actions_prompt
    
    def predict(self,obs:Any,rewards:Optional[int]):
        obs_str = "Input:\n"+str(obs)+"\nOutput:"
        instructions = action_prompt_begin+self.strategy_summary+self.actions_prompt+action_prompt_example+action_prompt_hint
        max_attempts = 5
        attempts = 0
        while attempts < max_attempts:
            try:
                response = self.lc_llm.chat(prompt=obs_str,instructions=instructions)
                # 使用正则表达式匹配字典部分
                match = re.search(r'\{.*\}', response, re.DOTALL)
                if match:
                    dict_str = match.group()
                    # 使用json.loads()函数将字符串转换为字典
                    response = json.loads(dict_str)
                else:
                    response = json.loads(response)
                action_num = response['actions']['action_num']
                break
            except json.JSONDecodeError:
                attempts += 1
                continue
        
        return action_num,response,obs_str


        
        