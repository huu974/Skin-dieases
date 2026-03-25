"""
用户提问，搜索参考资料，将提问和参考资料提交给模型，让模型总结服务
逻辑：实现检索增强（RAG）功能，根据用户查询从向量数据库检索相关文档，并结合查询和上下文生成总结回复
"""

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from rag.vector_store import VectorStoreService
from utils.prompt_loader import load_rag_prompts
from langchain_core.prompts import PromptTemplate
from model.factory import chat_model



#调试函数，打印提示词内容
def print_prompt(prompt):
    print("="*20)
    print(prompt.to_string())
    print("="*20)
    return prompt



#RAG总结服务类
class RagSummarizeService(object):
    def __init__(self):
        self.vector_store = VectorStoreService()
        self.retriever = self.vector_store.get_retriever()
        #加载提示词
        self.prompt_text = load_rag_prompts()
        #创建提示词模板
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)
        self.model = chat_model
        self.chain = self._init_chain()


    def _init_chain(self):
        chain = self.prompt_template | print_prompt | self.model | StrOutputParser()
        return chain


    #根据查询检索相关文档的方法
    def retriever_docs(self,query:str) -> list[Document]:
        #检索
        return self.retriever.invoke(query)


    #RAG总结的主要方法
    def rag_summarize(self,query:str) ->str :
        context_docs = self.retriever_docs(query)
        context = ""
        counter = 0
        for doc in context_docs:
            counter += 1
            context += f"【参考资料{counter}】:参考资料:{doc.page_content} | 参考元数据:{doc.metadata}\n"

        return self.chain.invoke(
            {"input": query,
             "context":context,
             }
        )




if __name__ == "__main__":
    rag = RagSummarizeService()
    print(rag.rag_summarize(""))













