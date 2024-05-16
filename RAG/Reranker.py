#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   Reranker.py
@Time    :   2024/05/15 14:27:42
@Author  :   YueZhengMeng
@Version :   1.0
@Desc    :   None
'''

from typing import List
import numpy as np


class BaseReranker:
    """
    Base class for reranker
    """

    def __init__(self, path: str) -> None:
        self.path = path

    def rerank(self, text: str, content: List[str], k: int) -> List[str]:
        raise NotImplementedError


class BgeReranker(BaseReranker):
    """
    class for Bge reranker
    """

    def __init__(self, path: str = 'BAAI/bge-reranker-base') -> None:
        super().__init__(path)
        self._model, self._tokenizer = self.load_model(path)

    def rerank(self, text: str, content: List[str], k: int) -> List[str]:
        import torch
        pairs = [(text, c) for c in content]
        with torch.no_grad():
            inputs = self._tokenizer(pairs, padding=True, truncation=True, return_tensors='pt', max_length=512)
            inputs = {k: v.to(self._model.device) for k, v in inputs.items()}
            scores = self._model(**inputs, return_dict=True).logits.view(-1, ).float()
            index = np.argsort(scores.tolist())[-k:][::-1]
        return [content[i] for i in index]

    def load_model(self, path: str):
        import torch
        from transformers import AutoModelForSequenceClassification, AutoTokenizer
        if torch.cuda.is_available():
            device = torch.device("cuda")
        else:
            device = torch.device("cpu")
        tokenizer = AutoTokenizer.from_pretrained(path)
        model = AutoModelForSequenceClassification.from_pretrained(path).to(device)
        model.eval()
        return model, tokenizer
