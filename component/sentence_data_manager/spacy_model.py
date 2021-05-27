import spacy
from component.sentence_data_manager.special_tokenizer import SpecialTokenizer


def spacy_model():
    nlp = spacy.load("en_core_web_sm")
    nlp.select_pipes(disable=["parser", "ner"])
    nlp.add_pipe("sentencizer")
    nlp = SpecialTokenizer.modified_hyphen_segmentation(nlp)
    nlp = SpecialTokenizer.modified_sign_segmentation(nlp)
    nlp = SpecialTokenizer.modified_brackets_segmentation(nlp)
    return nlp
