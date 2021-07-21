from nltk.corpus import stopwords
from typing import List, Set, Iterable, Tuple
from component.model.pattern import Pattern
from component.model.api_knowledge import APIKnowledge
from component.model.api_knowledge_instance import APIKnowledgeInstance
from component.model.sentence import Sentence
import re


class Filter:
    """
    用来过滤掉一些明显不合法的pattern、instance、api knowledge
    """
    INVALID_OBJECTS = {
        "-api-",
        "api",
        "-code-",
        "the"
    }

    def __init__(self):
        self.INVALID_OBJECTS.update(set(stopwords.words('english')))

    def filter_relation_between_pattern_and_instance(self, relation_list: List[Tuple[Pattern, APIKnowledgeInstance]]) -> List[Tuple[Pattern, APIKnowledgeInstance]]:
        result = []
        for pattern, instance in relation_list:
            api_knowledge = pattern.get_api_knowledge()
            if self.is_valid_api_knowledge(api_knowledge):
                result.append((pattern, instance))
        return result

    def filter_instance_by_invalid_object(self, instance_list: Iterable[APIKnowledgeInstance]):
        valid_instance = []
        for instance in instance_list:
            if self.is_valid_api_knowledge(instance.get_api_knowledge()):
                valid_instance.append(instance)
        return valid_instance

    def filter_api_knowledge_by_invalid_object(self, api_knowledge_list: Set[APIKnowledge]):
        valid_knowledge = []

        for api_knowledge in api_knowledge_list:
            if self.is_valid_api_knowledge(api_knowledge):
                valid_knowledge.append(api_knowledge)

        return set(valid_knowledge)

    def filter_patterns_by_invalid_object(self, patterns: Set[Pattern]):
        valid_pattern = []
        # invalid_pattern = []
        for pattern in patterns:
            if pattern is not None and self.is_valid_pattern_check_by_object(pattern):
                valid_pattern.append(pattern)
            # else:
            #     invalid_pattern.append(pattern)
        return set(valid_pattern)

    def is_valid_pattern_check_by_object(self, pattern: Pattern):
        api_knowledge = pattern.get_api_knowledge()
        return self.is_valid_api_knowledge(api_knowledge)

    def is_valid_api_knowledge(self, api_knowledge: APIKnowledge):
        object_list = api_knowledge.get_all_argument_values()
        for _object in object_list:
            if _object in self.INVALID_OBJECTS:
                return False
            re_result = re.search(r"\W", _object)
            if re_result:
                return False
            object_words = _object.split(" ")
            # 每个object长度不应该超过一定数目，目前设置为3
            if len(object_words) > 2:
                return False
            for word in object_words:
                if word == "-api-" or word == "-code-":
                    return False
        return True

    def is_valid_instance(self, instance: APIKnowledgeInstance):
        api_knowledge = instance.get_api_knowledge()
        return self.is_valid_api_knowledge(api_knowledge)

    def is_valid_api_in_sentence(self, sentence: Sentence):
        api: str = sentence.api
        if api.startswith("https://"):
            return False
        if api.startswith("http://"):
            return False
        return True

    def filter_sentence_by_api(self, sentence_list: List[Sentence]):
        valid_sentence = []
        for sentence in sentence_list:
            if self.is_valid_api_in_sentence(sentence):
                valid_sentence.append(sentence)
        return valid_sentence
