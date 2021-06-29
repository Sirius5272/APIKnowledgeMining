# sentence类，定义一个sentence的数据结构
from kgdt.utils import SaveLoad


class Sentence:
    """
    储存Sentence的数据结构，和APIKnowledge可以组合成APIKnowledgeInstance
    """
    def __init__(self, post_id, api, sentence):
        self.post_id = post_id
        self.api = api
        self.sentence = sentence

    def __hash__(self):
        return hash(self.sentence)

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, Sentence):
            return False
        if other.post_id != self.post_id or other.api != self.api or other.sentence != self.sentence:
            return False
        return True

    def __repr__(self):
        return "<Sentence post_id=%r api=%s sentence=%s>" % (self.post_id, self.api, self.sentence)

    @staticmethod
    def from_dict(data: dict):
        return Sentence(post_id=data["post_id"],
                        api=data["api"],
                        sentence=data["sentence"])

    def to_dict(self):
        return {"post_id": self.post_id, "api": self.api, "sentence": self.sentence}


class SentenceCollection(SaveLoad):
    def __init__(self):
        self.sentence_set = set([])
        self.id2sentence = {}
        self.sentence2id = {}

    def add(self, sentence: Sentence):
        if sentence in self.sentence_set:
            return self.sentence2id[sentence]

