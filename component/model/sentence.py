# sentence类，定义一个sentence的数据结构
from kgdt.utils import SaveLoad
from util.spacy_util import NLPUtil


class Sentence:
    """
    储存Sentence的数据结构，和APIKnowledge可以组合成APIKnowledgeInstance
    """
    def __init__(self, post_id, api, sentence: str):
        self.post_id = post_id
        self.api = api
        self.sentence = NLPUtil.clean_sentence(sentence)
        self.raw_sentence = self.sentence

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
        return "<Sentence %s>" % (self.to_str())

    def to_str(self):
        return "post_id = %r api = %s sentence = %s" % (self.post_id, self.api, self.sentence)

    @staticmethod
    def from_dict(data: dict):
        return Sentence(post_id=data["post_id"],
                        api=data["api"],
                        sentence=data["sentence"])

    def to_dict(self):
        return {"post_id": self.post_id, "api": self.api, "sentence": self.sentence, "raw_sentence": self.raw_sentence}


class SentenceCollection(SaveLoad):
    def __init__(self):
        self.sentence_set = set([])
        self.id2sentence = {}
        self.sentence2id = {}
        self.max_id = 0

    def add(self, sentence: Sentence):
        if sentence is None:
            return -1
        if sentence in self.sentence_set:
            return self.sentence2id[sentence]

        self.sentence_set.add(sentence)
        sentence_id = self.max_id
        self.id2sentence[sentence_id] = sentence
        self.sentence2id[sentence] = sentence_id
        self.max_id = sentence_id + 1
        return sentence_id

    def remove(self, sentence: Sentence):
        if sentence is None:
            return
        if sentence in self.sentence_set:
            self.sentence_set.remove(sentence)
        if sentence in self.sentence2id.keys():
            sentence_id = self.sentence2id.pop(sentence)
            if sentence_id in self.id2sentence.keys():
                self.id2sentence.pop(sentence_id)

    def remove_by_id(self, sentence_id):
        sentence = self.get_sentence_by_id(sentence_id)
        self.remove(sentence)

    def get_sentence_by_id(self, sentence_id):
        return self.id2sentence.get(sentence_id, None)

    def get_id_by_sentence(self, sentence: Sentence):
        if sentence is None:
            return -1
        if sentence not in self.sentence_set:
            return -1
        return self.sentence2id.get(sentence, -1)

    def size(self) -> int:
        return len(self.id2sentence.keys())

    def __len__(self):
        return self.size()

    def get_all_task(self):
        return self.sentence_set
