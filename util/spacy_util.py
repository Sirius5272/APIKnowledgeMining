import spacy
from component.sentence_data_manager.special_tokenizer import SpecialTokenizer


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
