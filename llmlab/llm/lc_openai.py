from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.prompts.chat import HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from transformers import GPT2Tokenizer
from langchain.text_splitter import CharacterTextSplitter
import logging
import asyncio

class LangChainLLM:
    def __init__(self, openai_api_key, model="gpt-3.5-turbo") -> None:
        # 初始化LangChainLLM类，设置OpenAI的API密钥和模型名称
        self.openai_api_key = openai_api_key
        self.model = model
        # 设置日志级别以忽略警告
        logging.getLogger("transformers.tokenization_utils_base").setLevel(logging.ERROR)
        # 使用GPT2的tokenizer
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

    def count_tokenizer(self, text: str):
        # 计算给定文本的token数量
        tokens = self.tokenizer.tokenize(text)
        num_tokens = len(tokens)
        return num_tokens

    def split_text(self, text: str, nums_token: int):
        # 根据指定的token数量分割文本
        text_splitter = CharacterTextSplitter.from_huggingface_tokenizer(self.tokenizer, chunk_size=nums_token, chunk_overlap=0)
        texts = text_splitter.split_text(text)
        return texts[0]

    def chat(self, prompt, instructions=None):
        # 使用指定的prompt和instructions进行聊天
        prompt = prompt.replace("{", "{{").replace("}", "}}")
        if instructions:
            chatprompt = ChatPromptTemplate.from_messages(
                [
                    SystemMessage(content=(instructions)),
                    HumanMessagePromptTemplate.from_template(prompt),
                ]
            )
        else:
            chatprompt = ChatPromptTemplate.from_template(prompt)
        model = ChatOpenAI(model=self.model, api_key=self.openai_api_key)
        output_parser = StrOutputParser()
        chain = chatprompt | model | output_parser
        # 调用链式处理并返回结果
        return chain.invoke("")

    async def achat(self, prompt, instructions=None):
        # 异步版本的chat方法
        prompt = prompt.replace("{", "{{").replace("}", "}}")
        if instructions:
            chatprompt = ChatPromptTemplate.from_messages(
                [
                    SystemMessage(content=(instructions)),
                    HumanMessagePromptTemplate.from_template(prompt),
                ]
            )
        else:
            chatprompt = ChatPromptTemplate.from_template(prompt)
        model = ChatOpenAI(model=self.model, api_key=self.openai_api_key)
        output_parser = StrOutputParser()
        chain = chatprompt | model | output_parser
        # 异步调用链式处理并返回结果
        return await chain.ainvoke("")