from unittest import TestCase
from component.model.pattern import Pattern
from component.model.api_knowledge import APIKnowledge
from component.model.sentence import Sentence


class TestPattern(TestCase):
    def test_get_mutated_regular_expression(self):
        sentence_dict = {
            "post_id": 29508992,
            "sentence": "removeFirst() : Remove the first element in the list.",
            "api": "com.sun.javafx.scene.control.skin.VirtualFlow.ArrayLinkedList.removeFirst()"
        }
        api_knowledge_dict = {
            "api": "com.sun.javafx.scene.control.skin.VirtualFlow.ArrayLinkedList.removeFirst()",
            "objects": {
                "object1": "Remove"
            }
        }




