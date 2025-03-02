# -*- coding: utf-8 -*-
# @Time: 2024/12/19 16:20
# @Author: Sui Yuan
# @Software: PyCharm
# @Desc:
import time

NEWS = """
1️⃣ 百度APP全面焕新：上线AI入口 DeepseekR1深度搜索不卡顿	🎉 百度APP全面焕新，正式上线AI入口，集成文心大模型与DeepSeek。 🔍 实现“千人千面”个性化体验，精准理解用户需求。 📚 提供多模态内容推荐，无需频繁跳转网页。 📅 2月16日接入深度搜索功能，2月20日正式推出DeepSeek-R1满血版。 📈 首日使用量突破千万次，用户反响热烈。👍	2️⃣ 腾讯健康接入DeepSeek+腾讯混元双模型 升级就医体验	🌟 腾讯健康接入DeepSeek+混元双模型，全面提升医疗服务 🚀 涵盖智能导诊、预问诊、健康问答、智能用药等多场景 🏥 帮助超1000家医院提升智能应用水平，支持医疗机构、体检中心等 👩‍⚕️ 提供个性化就医计划和健康管理，助力医生决策支持 📊 小觅AI助手快速分析影像报告，提升医生书写效率 🧬 推进基因组学和药械数字化领域发展，助力企业转型	3️⃣ DeepSeek 开源周首日：发布大模型加速利器FlashMLA 解码性能飙升至3000GB/s	🎉 DeepSeek 开源周首日发布 FlashMLA，专为英伟达 Hopper 架构 GPU 打造的高效多层注意力解码内核。 ⚡ 优化变长序列场景，显著提升大模型推理性能，BF16 精度全面支持。 📦 采用块大小为64的页式键值缓存系统，实现精准内存管理。 📈 性能表现卓越：在H800SXM5 GPU上，处理速度达3000GB/s，算力水平580TFLOPS。 🛠️ 经生产环境验证，稳定性优异。开发者可通过 "python setup.py install" 快速部署。	4️⃣ 科大讯飞等入股AI语音产品研发商声临奇境	科大讯飞旗下公司及武汉长湖科技入股深圳声临奇境人工智能有限公司。 公司注册资本从200万增至约202万人民币。 声临奇境成立于2019年7月，法定代表人周超。	5️⃣ 华为昇腾概念持续活跃，云从科技20CM涨停	华为昇腾概念持续活跃，云从科技盘中封20CM涨停🎉 同方股份2连板，拓维信息一度涨超5%，续创历史新高📈 开普云、软通动力、东方国信、常山北明等涨幅靠前。 华为推出FusionCube A3000训/推超融合一体机，适配DeepSeek V3&R1及蒸馏模型，支持私有化部署💻
"""

print(len(NEWS))


def doBase():
    return doSomething()


def doSomething(stream=False):
    values = [1, 2, 3, "aa"]
    if stream:
        for i in values:
            # 睡眠2s
            time.sleep(2)
            yield i
        return
    return values


if __name__ == '__main__':
    print(doBase())
