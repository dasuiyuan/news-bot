# 定义一个新闻分类的枚举类:AI产品类、AI技术类、AI商业类、其他科技类、其他类
from enum import Enum


class NewsType(Enum):
    AI_PRODUCT = "AI产品类"
    AI_TECHNOLOGY = "AI技术类"
    AI_BUSINESS = "AI商业类"
    OTHER_TECHNOLOGY = "其他科技类"
    OTHER_CLASS = "其他类"


NEWS_TYPE_SKIPPED = ['其他类']
