"""
fast text 模型的包装类
"""
import fasttext
from util.path_util import PathUtil
import os


class APISentenceClassifier:
    def __init__(self):
        self.classifier = None

    def train(self, train_data_path):
        classifier = fasttext.train_supervised(
            input=train_data_path,
            label_prefix='__label__',
            dim=512,
            epoch=100,
            lr=0.5,
            lr_update_rate=50,
            min_count=2,
            loss='softmax',
            word_ngrams=2,
            bucket=1000000
        )
        self.classifier = classifier

    def save(self, model_path=PathUtil.api_sentence_classifier_model()):
        if self.classifier:
            self.classifier.save_model(model_path)

    def load(self, model_path=PathUtil.api_sentence_classifier_model()):
        if os.path.exists(model_path):
            self.classifier = fasttext.load_model(model_path)
        else:
            raise ValueError("api sentence classifier model not exist")

    def is_api_sentence(self, sentence):
        pass

    def get_score(self, sentence):
        pass
