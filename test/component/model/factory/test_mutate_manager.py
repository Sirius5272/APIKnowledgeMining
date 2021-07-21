from unittest import TestCase
from component.model.factory.api_knowledge_mutator.mutate_manager import APIKnowledgeMutateManager
from component.model.api_knowledge import APIKnowledge


class TestAPIKnowledgeMutateManager(TestCase):
    def test_mutate_knowledge_list(self):
        api_knowledge_dicts = [{
            "api": "java.time.Duration",
            "objects": {
                "object1": "directly",
                "object2": "store",
                "object3": "automatically"
            }
        },
            {
                "api": "getErrorCode()",
                "objects": {
                    "object1": "SQLException",
                    "object2": "returns",
                    "object3": "failure"
                }
            }]
        knowledge = [APIKnowledge.from_dict(d) for d in api_knowledge_dicts]
        manager = APIKnowledgeMutateManager()
        new_knowledge = manager.mutate_knowledge_list(knowledge)
        for each in new_knowledge:
            print(each)
        print(len(new_knowledge))
