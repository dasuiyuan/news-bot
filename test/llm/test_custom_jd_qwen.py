# -*- coding: utf-8 -*-
# @Time: 2024/10/29 9:40
# @Author: Sui Yuan
# @Software: PyCharm
# @Desc:
from custom.llm.jdy_qwen_custom_llm import ChatQwen


if __name__ == '__main__':
    test_llm = ChatQwen(model="qwen-32b", reuse_client=True,
                        api_url="https://ai-api-gateway-cn-north-1.jdcloud.com/api/predict/qwen2-32b/v1",
                        api_key="7d1eca5ea994fafcdf6f0d760eec0ee3", )
    # test_messages = [{"role": "user", "content": "黑神话悟空好玩吗"}]
    # chat_response = test_llm._chat(test_messages)
    complete_response = test_llm.stream_complete_origin("北京有什么好玩的，只列举项目名称")
    for i in complete_response:
        print(i.json())

