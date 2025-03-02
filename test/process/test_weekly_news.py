from test.process import init_env

init_env()
from util.llm_util import chat_deepseek, chat_qwen, chat_glm, chat_ali_bailian
from process import prompt
from util.storage.sqlite_sqlalchemy import globle_db, SQLiteDB
from spider.po.news_po import BriefNews
from datetime import datetime, timedelta
from process import weekly_news
from process import image_generate
from process.weekly_news import weekly_integrate
import os
import json
from process.weekly_news import generate_weekly_news

WEEKLY_NEWS_TEXT = """
```json
{
  "hot-words": [
    {
      "hot-word": "AI模型开源",
      "reason": "本周多个公司如通义、DeepSeek和360智脑发布了开源的AI模型，显著推动了AI技术的透明化和社区协作。这不仅促进了技术创新，还为开发者提供了更多选择和灵活性。🚀"
    },
    {
      "hot-word": "学术诚信与AI",
      "reason": "随着AI工具在教育领域的广泛应用，高校教师对AI生成内容的担忧日益增加，多所高校出台了使用规范。这一现象引发了关于学术诚信和技术伦理的广泛讨论。📚"
    },
    {
      "hot-word": "高效推理模型",
      "reason": "Tiny-R1-32B和Claude3.7等高效推理模型的发布，展示了小参数量模型在性能上的巨大潜力，并大幅降低了推理成本，为AI应用提供了新的可能性。🤖"
    }
  ],
  "hot-company": {
    "company": "字节跳动",
    "reason": "字节跳动通过其AI编程软件Trae集成Claude3.7并提供无限免费使用的政策，在开发者社区中引起了广泛关注和热烈反响。此举不仅展示了字节的技术实力，还可能改变AI编程工具的市场格局。🎉"
  },
  "hot-tech": {
    "tech": "通义万相Wan2.1视频生成模型",
    "reason": "通义万相Wan2.1凭借其卓越的视频生成能力，在权威评测中登顶榜首，显著领先其他知名模型。该模型支持高质量视频生成，优化了指令遵循和物理规律还原，极大提升了用户体验。🎥"
  },
  "prediction": [
    "下周DeepSeek将陆续开源5个代码库，预计这些代码库将进一步推动AI基础设施建设，并吸引更多开发者参与其中。💻",
    "随着苹果自研基带芯片的应用，预计更多科技公司将加大对自研芯片的投入，以减少对外部供应商的依赖。⚡",
    "阿里计划在未来三年内投资3800亿元用于云和AI硬件基础设施建设，预计将加速国内AI生态的发展，推动更多企业进行AI转型。💡"
  ]
}
```
"""

if __name__ == '__main__':
    generate_weekly_news()
    # weekly_news_text = WEEKLY_NEWS_TEXT
    # # weekly_news_text = weekly_integrate()
    # img_path = os.path.join(os.environ.get("NEWS_BOT_ROOT"), "data", "image",
    #                         datetime.now().strftime("%Y-%m-%d"))
    # weekly_news_str = weekly_news_text.replace("```json", "").replace("```", "")
    # weekly_news = json.loads(weekly_news_str)
    # image_generate.generate_keywords_weekly(weekly_news["hot-words"], img_path)
    # image_generate.generate_hot_weekly(weekly_news["hot-company"], weekly_news["hot-tech"], img_path)
    # image_generate.generate_prediction_weekly(weekly_news["prediction"], img_path)
