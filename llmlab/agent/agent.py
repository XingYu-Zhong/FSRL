

from typing import Any
from llmlab.llm.lc_openai import LangChainLLM
from llmlab.prompt.strategy_prompt import *

class TradeAgent:
    def __init__(self,llm_api_key,llm_model,strategy_id) -> None:
        self.context = None
        self.llm_api_key = llm_api_key
        self.lc_llm = LangChainLLM(openai_api_key=llm_api_key,model=llm_model)
        if strategy_id == "two_bulin_rsi":
            strategy_summary = two_bulin_rsi
        elif strategy_id =="two_bulin_rsi_empty_vwap":
            strategy_summary = two_bulin_rsi_empty_vwap
        else:
            raise ValueError("未知的策略ID 请检查策略ID是否正确。")

        self.strategy_summary = strategy_summary
    
    def predict(self,obs:Any):
        pass

        
        