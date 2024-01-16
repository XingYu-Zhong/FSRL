

from typing import Any
from llmlab.llm.lc_openai import LangChainLLM

class TradeAgent:
    def __init__(self,llm_api_key,llm_model) -> None:
        self.context = None
        self.llm_api_key = llm_api_key
        self.lc_llm = LangChainLLM(openai_api_key=llm_api_key,model=llm_model)
    
    def predict(self,obs:Any):
        pass

        
        