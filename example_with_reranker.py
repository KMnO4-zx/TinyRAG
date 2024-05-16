import os
from RAG.VectorBase import VectorStore
from RAG.utils import ReadFiles
from RAG.LLM import ZhipuChat
from RAG.Embeddings import BgeEmbedding
from RAG.Reranker import BgeReranker

# 未创建向量数据库、更换数据集、或更换其他Embeddings模型后将have_created_db设置为False
# 运行一次成功创建向量数据库后可以将have_created_db设置为True
have_created_db = True
# 请将*替换为自己的API_KEY
os.environ['ZHIPUAI_API_KEY'] = "*"

# 创建EmbeddingModel
embedding = BgeEmbedding()

# 创建RerankerModel
reranker = BgeReranker()

if have_created_db:
    # 保存数据库之后
    vector = VectorStore()
    vector.load_vector('./storage')  # 加载本地的数据库
else:
    # 没有保存数据库
    docs = ReadFiles('./data').get_content(max_token_len=600, cover_content=150)  # 获得data目录下的所有文件内容并分割
    vector = VectorStore(docs)
    vector.get_vector(EmbeddingModel=embedding)
    vector.persist(path='storage')  # 将向量和文档内容保存到storage目录下，下次再用就可以直接加载本地的数据库

question = '远程仓库的协作与贡献有哪些？'

# 从向量数据库中查询出最相似的3个文档
content = vector.query(question, EmbeddingModel=embedding, k=3)
# 从一阶段查询结果中用Reranker再次筛选出最相似的2个文档
rerank_content = reranker.rerank(question, content, k=2)
# 最后选择最相似的文档, 交给LLM作为可参考上下文
best_content = rerank_content[0]
chat = ZhipuChat()
print(chat.chat(question, [], best_content))
