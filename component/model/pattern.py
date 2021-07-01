# pattern类，定义一个pattern的数据结构
from component.model.api_knowledge import APIKnowledge
from component.model.sentence import Sentence
import copy


class Pattern:
    # this is a test for SSH update
    def __init__(self, api_knowledge: APIKnowledge, sentence: Sentence, token_pattern_list: []):
        self.api_knowledge = copy.deepcopy(api_knowledge)
        self.sentence = copy.deepcopy(sentence)
        self.token_pattern_list = token_pattern_list


