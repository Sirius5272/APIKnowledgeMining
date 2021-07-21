from unittest import TestCase
from component.model.factory.api_knowledge_mutator.delete_object_mutator import DeleteObjectAPIKnowledgeMutator
from component.model.api_knowledge import APIKnowledge


class TestDeleteObjectAPIKnowledgeMutator(TestCase):
    def test_mutate(self):
        api_knowledge_dict = {
                                 "api": "java.time.Duration",
                                 "objects": {
                                     "object1": "directly",
                                     "object2": "store",
                                     "object3": "automatically"
                                 }
        }
        mutator = DeleteObjectAPIKnowledgeMutator()
        new_knowledge = mutator.mutate_on_constraint(APIKnowledge.from_dict(api_knowledge_dict))
        for each in new_knowledge:
            print(each)
