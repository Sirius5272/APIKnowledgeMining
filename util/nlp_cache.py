from util.spacy_util import NLPUtil
from util.path_util import PathUtil
from spacy.tokens import Doc
from util.sentence_to_doc import Sentence2Doc
import os


class NLPCache:
    doc_dict: Sentence2Doc = Sentence2Doc()
    nlp = NLPUtil.get_nlp()

    @classmethod
    def get_doc(cls, sentence):
        if not cls.doc_dict.sentence_to_doc:
            cls.load_doc()
        if sentence not in cls.doc_dict.get_sentence_to_doc_keys():
            doc = cls.nlp(sentence)
            doc_bytes = doc.to_bytes()
            cls.doc_dict.set_doc(sentence, doc_bytes)
            return doc
        else:
            doc_bytes = cls.doc_dict.get_doc(sentence)
            doc = Doc(cls.nlp.vocab).from_bytes(doc_bytes)
            return doc

    @classmethod
    def save_doc(cls, path=PathUtil.nlp_doc_cache()):
        cls.doc_dict.save(path)

    @classmethod
    def load_doc(cls, path=PathUtil.nlp_doc_cache()):
        if os.path.exists(path) and os.path.getsize(path):
            cls.doc_dict = Sentence2Doc.load(path)
