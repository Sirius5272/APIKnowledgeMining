from unittest import TestCase
from component.matcher.sentence_matcher import SentenceMatcher
from component.model.sentence import Sentence
from component.model.api_knowledge import APIKnowledge
from component.model.api_knowledge_instance import APIKnowledgeInstance


class TestSentenceMatcher(TestCase):
    def test_extract_api_knowledge_instances(self):
        sentence_dict = [
            {
                "post_id": 29508992,
                "sentence": "Calling _api_ is thread_safe.",
                "api": "stringBuffer"
            },
            {
                "post_id": 5694471,
                "sentence": "Use the _api_ to retrieve an array of File objects for each file in the directory, "
                            "and then call the getName() method to get the filename.",
                "api": "listFiles()"

            },
            {
                "post_id": 25433848,
                "sentence": "_api_ will help you to compare values of different kinds of objects with "
                            "each collection implementing java.util.Comparator would be a good possible option!",
                "api": "Collections.sort()"
            },
            # 以下是没有对应知识的句子
            {
                "post_id": 59710690,
                "sentence": "You must iterate, one way or another So now without iterating I want to set all the "
                            "_api+ flag to true, is it possible in java?",
                "api": "isActive"
            },
            {
                "post_id": 45190206,
                "sentence": "On the other hand, seeing that your Fruit is an interface rather than a base class, you"
                            " can have each of the classes which implement that interface have a _api_ method "
                            "returning a different value.",
                "api": "getName()"
            },
            {
                "post_id": 19718656,
                "sentence": "This Graphics g = _api_; is not how custom painting is done.",
                "api": "panel.getGraphics()"
            }
        ]
        api_knowledge_dict = [
            {
                "api": "stringBuffer",
                "objects": {
                    "object1": "Calling",
                    "object2": "thread_safe"
                }
            },
            {
                "api": "listFiles()",
                "objects": {
                    "object1": "Use",
                    "object2": "retrieve"
                }
            },
            {
                "api": "Collections.sort()",
                "objects": {
                    "object1": "help",
                    "object2": "compare"
                }
            }
        ]

        sentences = [Sentence.from_dict(d) for d in sentence_dict]
        knowledge = [APIKnowledge.from_dict(d) for d in api_knowledge_dict]
        sm = SentenceMatcher()
        result = sm.extract_api_knowledge_instances(sentences, knowledge)
        for each in result:
            print(each)
