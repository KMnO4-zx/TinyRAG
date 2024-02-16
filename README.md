# RAG-Learning

此仓库用于学习大模型RAG的相关内容，目前为手搓实现，主要是llama-index和langchain不太好魔改。此仓库可以方便看论文的时候，实现一些小的实验。

以下为RAG的实现过程。

![alt text](images/image.png)

# QuickStrat

安装依赖，需要 Python 3.10 以上版本。

```bash
pip install -r requirements.txt
```

导入所使用的包

```python
from RAG.VectorBase import VectorStore
from RAG.utils import ReadFiles
from RAG.LLM import OpenAIChat
```

如果没有数据库那就按照如下代码：

> 可以使用`VectorStore.persist()`保存到向量数据库。

```python
docs = ReadFiles('./data').get_content(max_token_len=600, cover_content=150) # 获得data目录下的所有文件内容并分割
vector = VectorStore(docs)
vector.get_vector(model='zhipu')
vector.persist(path='storage') # 将向量和文档内容保存到storage目录下，下次再用就可以直接加载本地的数据库

# vector.load_vector('./storage') # 加载本地的数据库

question = 'git的原理是什么？'

content = vector.query(question, model='zhipu', k=1)[0]
chat = OpenAIChat(model='gpt-3.5-turbo-1106')
print(chat.chat(question, [], content))
```

如果有数据库那就按照如下代码：

```python
vector = VectorStore()

vector.load_vector('./storage') # 加载本地的数据库

question = 'git的原理是什么？'

content = vector.query(question, model='zhipu', k=1)[0]
chat = OpenAIChat(model='gpt-3.5-turbo-1106')
print(chat.chat(question, [], content))
```

> 如果大家的文档有中文的话，不建议使用`openai`的向量接口，可以使用智谱AI或者Jina的向量模型或接口

# 实现细节

## 向量化

在这一部分共使用了三种向量化的方法，分别是`zhipu`、`jina`和`openai`。大家可以在`Embedding`文中找到实现的方式。

如果你有兴趣想使用其他的向量模型可以继承`BaseEmbeddings`类，然后实现`get_embedding`方法。

```python
class BaseEmbeddings:
    """
    Base class for embeddings
    """
    def __init__(self, path: str, is_api: bool) -> None:
        self.path = path
        self.is_api = is_api
    
    def get_embedding(self, text: str, model: str) -> List[float]:
        raise NotImplementedError
    
    @classmethod
    def cosine_similarity(cls, vector1: List[float], vector2: List[float]) -> float:
        """
        calculate cosine similarity between two vectors
        """
        dot_product = np.dot(vector1, vector2)
        magnitude = np.linalg.norm(vector1) * np.linalg.norm(vector2)
        if not magnitude:
            return 0
        return dot_product / magnitude
```

## 向量检索

这里未使用任何成熟的数据库，只是简单的使用`Json`保存了文档分割后的片段和对应的向量。大家可以在`VectorBase`中找到实现的方式。

在向量检索的时候仅使用`Numpy`进行加速，代码非常容易理解和修改。

```python
def query(self, query: str, model: str = 'openai', k: int = 1) -> List[str]:
    if not self.vectors:
        raise ValueError("No vectors found")
    if model == "openai":
        embedding = OpenAIEmbedding()
    elif model == "jina":
        embedding = JinaEmbedding()
    elif model == "zhipu":
        embedding = ZhipuEmbedding()
    else:
        raise ValueError("Model not supported")
    query_vector = embedding.get_embedding(query)
    result = np.array([self.get_similarity(query_vector, vector) for vector in self.vectors])
    return np.array(self.document)[result.argsort()[-k:][::-1]]
```

> 没有考虑生产环境使用，仅供学习使用

## LLM 模型

这里支持了`openai`模型和`InternLM2`模型，如果想要用其他的模型，大家可以在`LLM`中找到实现的方式。继承以下基类，然后在此基础上进行修改即可。

```python
class BaseModel:
    def __init__(self, path: str = '') -> None:
        self.path = path

    def chat(self, prompt: str, history: List[dict], content: str) -> str:
        pass

    def load_model(self):
        pass
```


# 参考文献

[When Large Language Models Meet Vector Databases: A Survey](https://arxiv.org/abs/2402.01763)