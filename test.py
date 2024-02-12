from VectorBase import VectorStore
from LLM import OpenAIChat


vector = VectorStore()
vector.load_vector()

question = '逆向纠错的原理是什么？'

content = vector.query(question, model='zhipu', k=1)[0]
chat = OpenAIChat()
print(chat.chat(question, [], content))
