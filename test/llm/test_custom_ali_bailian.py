from llm.ali_bailian_custom_llm import ChatAliBailian
from settings import geoi_settings

if __name__ == '__main__':
    test_llm = ChatAliBailian(model=geoi_settings.ALI_BAILIAN_MODEL, reuse_client=True,
                              api_key=geoi_settings.ALI_BAILIAN_API_KEY, api_url=geoi_settings.ALI_BAILIAN_API_URL)
    # 对话模式
    test_messages = [{"role": "user", "content": "黑神话悟空好玩吗"}]
    chat_response = test_llm._chat(test_messages)

    # 直问流式输出
    complete_response = test_llm.stream_complete("北京有什么好玩的，只列举项目名称")
    for comp in complete_response:
        print(comp.delta, end="")

    # 直问同步输出
    complete_response = test_llm.complete("北京有什么好玩的，只列举项目名称")
    print(complete_response)
