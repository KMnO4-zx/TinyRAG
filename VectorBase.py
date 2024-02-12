#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   VectorBase.py
@Time    :   2024/02/12 10:11:13
@Author  :   不要葱姜蒜
@Version :   1.0
@Desc    :   None
'''

import os
from typing import Dict, List, Optional, Tuple, Union
import json
from Embeddings import BaseEmbeddings, OpenAIEmbedding, JinaEmbedding, ZhipuEmbedding
import numpy as np
from tqdm import tqdm


class VectorStore:
    def __init__(self, document: List[str] = ['']) -> None:
        self.document = document

    def get_vector(self, model: str = 'zhipu') -> List[List[float]]:
        if model == "openai":
            embedding = OpenAIEmbedding()
        elif model == "jina":
            embedding = JinaEmbedding()
        elif model == "zhipu":
            embedding = ZhipuEmbedding()
        else:
            raise ValueError("Model not supported")
        self.vectors = []
        for doc in tqdm(self.document, desc="Calculating embeddings"):
            self.vectors.append(embedding.get_embedding(doc))
        return self.vectors

    def persist(self, path: str = 'storage'):
        if not os.path.exists(path):
            os.makedirs(path)
        with open(f"{path}/doecment.json", 'w', encoding='utf-8') as f:
            json.dump(self.document, f, ensure_ascii=False)
        if self.vectors:
            with open(f"{path}/vectors.json", 'w', encoding='utf-8') as f:
                json.dump(self.vectors, f)

    def load_vector(self, path: str = 'storage'):
        with open(f"{path}/vectors.json", 'r', encoding='utf-8') as f:
            self.vectors = json.load(f)
        with open(f"{path}/doecment.json", 'r', encoding='utf-8') as f:
            self.document = json.load(f)

    def get_similarity(self, vector1: List[float], vector2: List[float]) -> float:
        return BaseEmbeddings.cosine_similarity(vector1, vector2)

    def query(self, query: str, model: str = 'zhipu', k: int = 1) -> List[str]:
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


# if __name__ == "__main__":
#     from utils import ReadFiles
#     # docs = ReadFiles('./data').get_content()
#     vector = VectorStore()
#     # vector.get_vector(model='zhipu')
#     # vector.persist()
#     vector.load_vector()
#     print(vector.query("git如何管理分支", model='zhipu', k=1))
