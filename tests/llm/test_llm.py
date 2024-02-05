import pytest
from unittest.mock import patch, MagicMock
from llmlab.llm.lc_openai import LangChainLLM
#设置代理
import os

os.environ['http_proxy'] = 'http://127.0.0.1:10809'
os.environ['https_proxy'] = 'http://127.0.0.1:10809'
@pytest.fixture
def mock_openai_api_key():
    return "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"

@pytest.fixture
def mock_model():
    return "gpt-3.5-turbo"

@pytest.fixture
def lang_chain_llm(mock_openai_api_key, mock_model):
    return LangChainLLM(openai_api_key=mock_openai_api_key, model=mock_model)


# def test_chat_with_instructions(lang_chain_llm):
#     prompt = "Hello, how are you?"
#     instructions = "Please be friendly."

    
#     response = lang_chain_llm.chat(prompt=prompt, instructions=instructions)
#     print(f'response:{response}')

def testorigin(mock_openai_api_key):
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser


    from langchain_core.runnables import RunnablePassthrough


    prompt = ChatPromptTemplate.from_template(
        "Tell me a short joke about 123"
    )
    output_parser = StrOutputParser()
    model = ChatOpenAI(model="gpt-3.5-turbo",api_key=mock_openai_api_key)
    chain = (
        prompt
        | model
        | output_parser
    )

    resp = chain.invoke({'':''})
    print(f"chain:{resp}")