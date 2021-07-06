from unittest import TestCase
from component.model.pattern import Pattern
from component.model.api_knowledge import APIKnowledge
from component.model.sentence import Sentence
from component.model.api_knowledge_instance import APIKnowledgeInstance
from component.model.factory.pattern_factory import PatternFactory
from component.model.factory.pattern_mutator import PatternMutator


class TestPlaceHolderMutator(TestCase):
    def test_mutate(self):
        sentence_dict = {
            "post_id": 29508992,
            "sentence": "Calling stringBuffer is thread_safe.",
            "api": "com.sun.javafx.scene.control.skin.VirtualFlow.ArrayLinkedList.removeFirst()"
        }
        api_knowledge_dict = {
            "api": "stringBuffer",
            "objects": {
                "object1": "Calling",
                "object2": "thread_safe"
            }
        }
        sentence: Sentence = Sentence.from_dict(sentence_dict)
        api_knowledge: APIKnowledge = APIKnowledge.from_dict(api_knowledge_dict)
        instance: APIKnowledgeInstance = APIKnowledgeInstance(sentence=sentence, api_knowledge=api_knowledge)
        pf = PatternFactory()
        pattern: Pattern = pf.get_pattern_from_sentence(instance)
        pm = PatternMutator()
        new_patterns = pm.mutate(pattern)
        print(pattern)
        print("*" * 10)
        for each in new_patterns:
            print(each)
