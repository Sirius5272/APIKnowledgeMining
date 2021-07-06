from unittest import TestCase
from component.matcher.sentence_matcher import SentenceMatcher
from component.model.sentence import Sentence
from component.model.api_knowledge import APIKnowledge
from component.model.api_knowledge_instance import APIKnowledgeInstance
from component.model.factory.pattern_factory import PatternFactory
from component.snowball import Snowball
from component.matcher.pattern_matcher import PatternMatcher


class TestSnowball(TestCase):
    def test_run_for_one_step(self):
        # 分步骤测试一下是否能成功
        sentence_dict = [
            {
                "post_id": 29508992,
                "sentence": "Calling stringBuffer is thread_safe.",
                "api": "com.sun.javafx.scene.control.skin.VirtualFlow.ArrayLinkedList.removeFirst()"
            },
            {
                "post_id": 5694471,
                "sentence": "Use the listFiles() to retrieve an array of File objects for each file in the directory, "
                            "and then call the getName() method to get the filename.",
                "api": "java.io.File.listFiles()"

            },
            {
                "post_id": 25433848,
                "sentence": "Collections.sort() will help you to compare values of different kinds of objects with "
                            "each collection implementing java.util.Comparator would be a good possible option!",
                "api": "java.util.Comparator"
            },
            # 以下是没有对应知识的句子
            {
                "post_id": 59710690,
                "sentence": "You must iterate, one way or another So now without iterating I want to set all the "
                            "isActive flag to true, is it possible in java?",
                "api": "javax.swing.text.DefaultCaret.isActive()"
            },
            {
                "post_id": 45190206,
                "sentence": "On the other hand, seeing that your Fruit is an interface rather than a base class, you"
                            " can have each of the classes which implement that interface have a getName() method "
                            "returning a different value.",
                "api": "org.w3c.dom.html.HTMLTextAreaElement.getName()"
            },
            {
                "post_id": 19718656,
                "sentence": "This Graphics g = panel.getGraphics(); is not how custom painting is done.",
                "api": "java.awt.Graphics.Graphics()"
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
        # 第一步，将种子API Knowledge拿去匹配句子库，得到instance
        instance_result = sm.extract_api_knowledge_instances(sentences, knowledge)
        sb = Snowball()
        # 第二步，从上一步得到的instance里抽取出pattern，并且变异出挖空的pattern
        patterns = sb.extract_pattern_from_instances(instance_result)
        # 第三步，使用得到的pattern拿回句子库里匹配，得到匹配的instance
        pm = PatternMatcher()
        matched_instance = pm.match_patterns(sentence_list=sentences, patterns=patterns)
        # 第四步，从上一步得到的instance中获取到新的api knowledge，作为下一轮匹配的种子
        new_seed = sb.extract_api_knowledge_from_instances(matched_instance)
        print("*" * 10)
        for seed in new_seed:
            print(seed)

    def test_extract_pattern_from_instances(self):
        sentence_dict = [
            {
                "post_id": 29508992,
                "sentence": "Calling stringBuffer is thread_safe.",
                "api": "com.sun.javafx.scene.control.skin.VirtualFlow.ArrayLinkedList.removeFirst()"
            },
            {
                "post_id": 5694471,
                "sentence": "Use the listFiles() to retrieve an array of File objects for each file in the directory, "
                            "and then call the getName() method to get the filename.",
                "api": "java.io.File.listFiles()"

            },
            {
                "post_id": 25433848,
                "sentence": "Collections.sort() will help you to compare values of different kinds of objects with "
                            "each collection implementing java.util.Comparator would be a good possible option!",
                "api": "java.util.Comparator"
            },
            # 以下是没有对应知识的句子
            {
                "post_id": 59710690,
                "sentence": "You must iterate, one way or another So now without iterating I want to set all the "
                            "isActive flag to true, is it possible in java?",
                "api": "javax.swing.text.DefaultCaret.isActive()"
            },
            {
                "post_id": 45190206,
                "sentence": "On the other hand, seeing that your Fruit is an interface rather than a base class, you"
                            " can have each of the classes which implement that interface have a getName() method "
                            "returning a different value.",
                "api": "org.w3c.dom.html.HTMLTextAreaElement.getName()"
            },
            {
                "post_id": 19718656,
                "sentence": "This Graphics g = panel.getGraphics(); is not how custom painting is done.",
                "api": "java.awt.Graphics.Graphics()"
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
        instance_result = sm.extract_api_knowledge_instances(sentences, knowledge)
        sb = Snowball()
        patterns = sb.extract_pattern_from_instances(instance_result)
        for p in patterns:
            print(p)