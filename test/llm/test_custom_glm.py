# -*- coding: utf-8 -*-
# @Time: 2024/10/29 9:38
# @Author: Sui Yuan
# @Software: PyCharm
# @Desc:

from llm.glm_custom_llm import ChatGLM, ZHIPU_API_KEY
from llm.glm_custom_embeding import ChatGLMEmbeddings

if __name__ == '__main__':
    test_llm = ChatGLM(model="GLM-4-0520", reuse_client=True, api_key=ZHIPU_API_KEY, )
    # 对话模式
    test_messages = [{"role": "user", "content": "黑神话悟空好玩吗"}]
    chat_response = test_llm._chat(test_messages)

    # 直问流式输出
    complete_response = test_llm.stream_complete("北京有什么好玩的，只列举项目名称")
    for comp in complete_response:
        print(comp.delta)

    # 直问同步输出
    complete_response = test_llm.complete("北京有什么好玩的，只列举项目名称")
    print(complete_response)
