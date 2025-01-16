# 定义一个新闻分类的枚举类:科技AI类、其他科技类、经济类、社会类、体育类、政治类
from enum import Enum


class NewsClassify(Enum):
    TECH_AI = "科技AI类"
    OTHER_TECH = "其他科技类"
    ECONOMY = "经济类"
    SOCIETY = "社会类"
    SPORT = "体育类"
    POLITICS = "政治类"
