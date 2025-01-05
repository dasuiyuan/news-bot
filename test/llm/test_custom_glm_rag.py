# -*- coding: utf-8 -*-
# @Time: 2024/8/28 15:31
# @Author: Sui Yuan
# @Software: PyCharm
# @Desc:

from llama_index.core import SimpleDirectoryReader
from llama_index.core import Settings
from llama_index.core import VectorStoreIndex
from custom.llm.glm_custom_llm import ChatGLM, ZHIPU_API_KEY
from custom.llm.glm_custom_embeding import ChatGLMEmbeddings

if __name__ == '__main__':
    # define our LLM
    Settings.llm = ChatGLM(model='glm-4', reuse_client=True, api_key=ZHIPU_API_KEY, )

    # define embed model
    Settings.embed_model = ChatGLMEmbeddings(model='embedding-2', reuse_client=True, api_key=ZHIPU_API_KEY, )

    # Load the your data
    documents = SimpleDirectoryReader(input_files=[r"../data/部门bp.txt"]).load_data()

    index = VectorStoreIndex.from_documents(documents, show_progress=True)
    query_engine = index.as_query_engine()
    response = query_engine.query("税务BP是谁？")
    print(response)
