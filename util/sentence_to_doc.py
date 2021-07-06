from kgdt.utils import SaveLoad


class Sentence2Doc(SaveLoad):
    def __init__(self):
        self.sentence_to_doc = {}

    def get_sentence_to_doc_keys(self):
        return self.sentence_to_doc.keys()

    def get_doc(self, sentence):
        return self.sentence_to_doc[sentence]

    def set_doc(self, sentence, doc):
        self.sentence_to_doc[sentence] = doc
