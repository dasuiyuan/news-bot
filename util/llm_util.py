# -*- coding: utf-8 -*-
# @Time: 2024/9/10 15:42
# @Author: Sui Yuan
# @Software: PyCharm
# @Desc:

import urllib.request
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
from llm.ali_bailian_custom_llm import ChatAliBailian, ALI_BAILIAN_DEFAULT_MODEL, ALI_BAILIAN_API_KEY, \
    ALI_BAILIAN_API_URL
from llm.deepseek_custom_llm import (
    ChatDeepSeek,
    DEFAULT_MODEL as DEEPSEEK_MODEL,
    DEEPSEEK_API_KEY,
    DEEPSEEK_API_URL
)
from llm.xinference_embedding import xi_default_embedding
from zhipuai import ZhipuAI

_chat_deepseek = ChatDeepSeek(model=DEEPSEEK_MODEL, reuse_client=True, api_key=DEEPSEEK_API_KEY,
                              api_url=DEEPSEEK_API_URL)
_chat_qwen = ChatQwen(model=DEFAULT_MODEL, reuse_client=True,
                      api_url=Qwen_API_URL,
                      api_key=Qwen_API_KEY, )

_chat_ali_bailian = ChatAliBailian(model=ALI_BAILIAN_DEFAULT_MODEL, reuse_client=True, context_window=32000,
                             api_url=ALI_BAILIAN_API_URL,
                             api_key=ALI_BAILIAN_API_KEY, )

_chat_glm = ChatGLM(model='glm-4', reuse_client=True, api_key=ZHIPU_API_KEY, )
_embedding_glm = ChatGLMEmbeddings(model='embedding-2', reuse_client=True, api_key=ZHIPU_API_KEY, )


def chat_deepseek():
    return _chat_deepseek


def chat_glm():
    return _chat_glm


def chat_ali_bailian():
    return _chat_ali_bailian


def glm_embedding():
    return _embedding_glm


def chat_qwen():
    return _chat_qwen


def bge_m3_xinfer():
    return xi_default_embedding


def img_gen(prompt: str, size: str = "1344x768", save_path: str = None):
    client = ZhipuAI(api_key=ZHIPU_API_KEY)

    response = client.images.generations(
        model="cogView-4",  # 填写需要调用的模型编码
        prompt=prompt,
        size=size
    )
    url = response.data[0].url
    if save_path:
        download_image(url, save_path)
    return url


def download_image(url, save_path):
    try:
        # 打开 URL 并获取响应
        response = urllib.request.urlopen(url)
        # 读取响应内容
        image_data = response.read()
        # 以二进制写入模式打开文件
        with open(save_path, 'wb') as f:
            # 将图片数据写入文件
            f.write(image_data)
        print(f"图片已成功保存到 {save_path}")
    except Exception as e:
        print(f"下载图片时出现错误: {e}")
