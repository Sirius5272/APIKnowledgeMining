from unittest import TestCase
from component.matcher.pattern_matcher import PatternMatcher
from component.matcher.sentence_matcher import SentenceMatcher
from component.model.factory.pattern_factory import PatternFactory
from component.model.sentence import Sentence
from component.model.api_knowledge import APIKnowledge
from component.model.pattern import Pattern
from component.model.api_knowledge_instance import APIKnowledgeInstance
from component.snowball import Snowball


class TestPatternMatcher(TestCase):
    def test_match_patterns(self):
        sentence_dict = [
            {
                "post_id": 29508992,
                "sentence": "Calling stringBuffer is thread_safe.",
                "api": "com.sun.javafx.scene.control.skin.VirtualFlow.ArrayLinkedList.removeFirst()"
            },
        ]
        api_knowledge_dict = [
            {
                "api": "stringBuffer",
                "objects": {
                    "object1": "Calling",
                    "object2": "thread_safe"
                }
            }
        ]

        sentences = [Sentence.from_dict(d) for d in sentence_dict]
        knowledge = [APIKnowledge.from_dict(d) for d in api_knowledge_dict]
        sm = SentenceMatcher()
        instances = sm.extract_api_knowledge_instances(sentences, knowledge)
        sb = Snowball()
        # pf = PatternFactory()
        patterns = sb.extract_pattern_from_instances(instances)
        pm = PatternMatcher()
        matched_instance = pm.match_patterns(sentence_list=sentences, patterns=patterns)
        for each in matched_instance:
            print(each)
