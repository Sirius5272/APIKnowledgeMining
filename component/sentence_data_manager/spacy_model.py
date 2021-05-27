import spacy


def spacy_model():
    nlp = spacy.load("en_core_web_sm")
    return nlp
