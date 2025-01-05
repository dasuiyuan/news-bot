# -*- coding: utf-8 -*-
# @Time: 2024/9/10 15:42
# @Author: Sui Yuan
# @Software: PyCharm
# @Desc:
from llm.glm_custom_llm import (
    ChatGLM,
    ZHIPU_API_KEY
)
from llm.glm_custom_embeding import ChatGLMEmbeddings
from llm.jdy_qwen_custom_llm import (
    ChatQwen,
    DEFAULT_MODEL,
    Qwen_API_KEY,
    Qwen_API_URL
)
from llm.deepseek_custom_llm import (
    ChatDeepSeek,
    DEFAULT_MODEL as DEEPSEEK_MODEL,
    DEEPSEEK_API_KEY,
    DEEPSEEK_API_URL
)
from llm.xinference_embedding import xi_default_embedding

_chat_deepseek = ChatDeepSeek(model=DEEPSEEK_MODEL, reuse_client=True, api_key=DEEPSEEK_API_KEY,
                              api_url=DEEPSEEK_API_URL)
_chat_qwen = ChatQwen(model=DEFAULT_MODEL, reuse_client=True,
                      api_url=Qwen_API_URL,
                      api_key=Qwen_API_KEY, )

_chat_glm = ChatGLM(model='glm-4', reuse_client=True, api_key=ZHIPU_API_KEY, )
_embedding_glm = ChatGLMEmbeddings(model='embedding-2', reuse_client=True, api_key=ZHIPU_API_KEY, )


def chat_deepseek():
    return _chat_deepseek


def chat_glm():
    return _chat_glm


def glm_embedding():
    return _embedding_glm


def chat_qwen():
    return _chat_qwen


def bge_m3_xinfer():
    return xi_default_embedding
