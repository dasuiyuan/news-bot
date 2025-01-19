from util.llm_util import chat_deepseek, chat_qwen, chat_glm
from process import prompt

NEWS = {"中国考虑限制部分汽车电池技术出口": """1 月 2 日中国商务部、科技部等部门将汽车动力电池领域中的磷酸铁锂材料制造工艺技术列入《中国禁止出口限制出口技术目录》调整征求意见稿中。
目录中涉及技术是第四代磷酸铁锂电池制造的核心工艺，通过挤压化学材料，提升同等体积下电池的电容量，主要用在宁德时代的高性价比电池中，并非标准续航版特斯拉使用的普通磷酸铁锂电池。
目前全球仅有宁德时代的供应商湖南裕能和富临精工掌握这种工艺。
按照定义 ，技术出口包含海外投资建厂、技术 / 专利授权或转让等。目前宁德时代、亿纬锂能等电池公司都在海外推广转让、授权部分电池技术的业务模式，与海外车企合作生产电池。目前尚未确定限制电池技术出口对上述公司海外业务的影响。
根据历史文件，字节跳动等公司使用的推荐算法技术也曾出现在该目录中。""",
        "OpenAI攻略传媒领域之际，苹果撤回AI新闻功能": "OpenAI宣布与美国数字媒体Axios达成战略伙伴关系。除了常见的内容合作外，科技巨头还将出资帮助Axios建立“由OpenAI技术支持的地方新闻编辑室”。面对AI能力不足的争议，苹果公司在最新测试版系统中暂停了新闻APP的AI“通知摘要”功能；自去年底以来，苹果股价已经累计下跌超13%。"}

if __name__ == '__main__':
    for title, content in NEWS.items():
        response = chat_deepseek().complete(
            prompt.PROMPT_NEWS_SUMMARIZE.format(length=50, title=title, content=content))
        print(response)
