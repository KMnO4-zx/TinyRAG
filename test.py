from Embeddings import BaseEmbeddings, OpenAIEmbedding, JinaEmbedding, ZhipuEmbedding

embedding = ZhipuEmbedding()
response1 = embedding.get_embedding('我不喜欢你')
response2 = embedding.get_embedding('我喜欢你')
print('Zhipu: ',embedding.cosine_similarity(response1, response2))

embedding_openai = OpenAIEmbedding()
response3 = embedding_openai.get_embedding('我喜欢你')
response4 = embedding_openai.get_embedding('我不喜欢你')
print('OpenAI: ',embedding_openai.cosine_similarity(response3, response4))