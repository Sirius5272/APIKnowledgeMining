from unittest import TestCase
from component.model.api_knowledge import APIKnowledge
from component.model.factory.api_knowledge_mutator.synonym_mutator import APIKnowledgeSynonymMutator


class TestAPIKnowledgeSynonymMutator(TestCase):

    def test_mutate(self):
        api_knowledge_dict = {
            "api": "java.time.Duration",
            "objects": {
                "object1": "directly",
                "object2": "store",
                "object3": "automatically"
            }
        }
        mutator = APIKnowledgeSynonymMutator()
        new_knowledge = mutator.mutate(APIKnowledge.from_dict(api_knowledge_dict))
        for each in new_knowledge:
            print(each)
        print(len(new_knowledge))
        print(len(set(new_knowledge)))
