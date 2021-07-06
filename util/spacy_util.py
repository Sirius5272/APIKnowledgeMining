import spacy
from component.sentence_data_manager.special_tokenizer import SpecialTokenizer
from spacy.matcher.matcher import Matcher


class NLPUtil:
    spacy_model = None

    @classmethod
    def get_nlp(cls):
        if cls.spacy_model is None:
            cls.spacy_model = spacy.load("en_core_web_sm")
            cls.spacy_model.select_pipes(disable=["parser", "ner"])
            cls.spacy_model.add_pipe("sentencizer")
            cls.spacy_model = SpecialTokenizer.modified_hyphen_segmentation(cls.spacy_model)
            cls.spacy_model = SpecialTokenizer.modified_sign_segmentation(cls.spacy_model)
            cls.spacy_model = SpecialTokenizer.modified_brackets_segmentation(cls.spacy_model)
        return cls.spacy_model

    @classmethod
    def get_spacy_matcher(cls) -> Matcher:
        return Matcher(cls.get_spacy_nlp_vocab())

    @classmethod
    def get_spacy_nlp_vocab(cls):
        return cls.get_nlp().vocab

    @classmethod
    def clean_sentence(cls, sentence):
        clean_words = [
            # "duplicate]",
            # "closed]",  # 解决移除字符串会当作正则表达式的问题
            # "[",
            "[.?!,、:;]"
            # ".",
            # "?",
            # "!",
            # ",",
            # "、",
            # ":",
            # ";"
        ]
        for cw in clean_words:
            sentence = sentence.rstrip(cw)
            sentence = sentence.rstrip()
        return sentence
