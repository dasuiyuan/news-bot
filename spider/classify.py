from util.log_util import logger
from util.llm_util import chat_qwen

PROMPT_NEWS_CLASSIFY = """
你是一个新闻分类器，请根据新闻标题和内容，判断该新闻属于以下哪类：
AI产品类
AI商业类
AI技术类
其他科技类
其他类

# 输出要求
1、只从上面几种类别输出，不要扩展其他类别，如果无法判断请输出UNK
2、只输出对应的分类名称，不要需要其他说明，不要前面加冒号


# 举例说明
案例1：
title:GpuGeek云平台正式亮相
content:36氪获悉，Gpugeek云平台已于1月6日正式上线，该平台是一个面向算法工程师的AI infra平台，为用户提供一站式GPU算力、对象存储、NAS存储、云盘、开发工具、模型部署等能力，专注模型研发和微调。
class:AI技术类

案例2：
title:韦德布什上调谷歌和亚马逊目标价
content:韦德布什将谷歌公司目标价格从210美元上调至220美元，将亚马逊目标价格从250美元上调至260美元。（财联社）
class:其他类

案例3：
title:特斯拉年交付量十年来首次下滑。
content:特斯拉 2024 年第四季度交付 49.6 万辆，不及预期的 51 万辆。全年交付量为 178.9 万辆，低于 2023 年的 181 万辆。据媒体报道，这是特斯拉年交付量自 2011 年来首次出现同比下滑。消息公布之后，特斯拉美股收盘下跌约 6%。
class:其他科技类

案例4：
title:三星与 OpenAI 合作，可能推出 AI 电视。
content:据报道，三星电子正在与 OpenAI 协调建立 “开放式合作伙伴关系”。如果合作顺利达成，未来三星电视可能会搭载 OpenAI 的 GPT、DALL-E、Whisper 和 o1 等技术，为用户提供个性化内容推荐、聊天机器人、实时语言翻译等功能。
class:AI产品类


title:{title}
content:{content}
"""


def classify(title, content) -> str:
    result = ""
    try:
        # 获取分类结果
        response = chat_qwen().complete(PROMPT_NEWS_CLASSIFY.format(title=title, content=content))
        result = response.text.replace(":", "")
        logger.info(f"{title}->{result}")
    except Exception as e:
        logger.error(f"分类识别失败:{e}")
    return result
