PROMPT_NEWS_CLASSIFY = """
你是一个新闻分类器，请根据新闻标题和内容，判断该新闻属于以下哪类：
1. 科技类
2. 经济类
3. 社会类
4. 体育类
5. 政治类

# 输出要求
1、

# 举例说明

title={title}
content={content}
"""

PROMPT_AI_NEWS_CLASSIFY = """
你是一个新闻分类器，请根据新闻标题和内容，判断该新闻属于以下哪类：
1. 科技类
2. 经济类
3. 社会类
4. 体育类
5. 政治类

# 输出要求
1、

# 举例说明

title={title}
content={content}
"""

PROMPT_NEWS_SUMMARIZE = """
你是一个新闻总结专家，请将一段比较长的新闻，总结为一段{length}个字以内的文字。

# 输出要求
1、保持原文意思，不要扩展
2、提取出最重点的内容，整体长度不能超过{length}

# 举例说明
案例1：
title:
content:
summary:


案例2：
title:
content:
summary:

title={title}
content={content}
"""
