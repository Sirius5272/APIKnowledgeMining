from component.model.factory.api_knowledge_mutator.delete_object_mutator import DeleteObjectAPIKnowledgeMutator
from component.model.factory.api_knowledge_mutator.synonym_mutator import APIKnowledgeSynonymMutator
from util.log_util import LogUtil
from component.model.api_knowledge import APIKnowledge
from typing import Set, Iterable


class APIKnowledgeMutateManager:
    def __init__(self):
        self.mutators = [
            DeleteObjectAPIKnowledgeMutator(),
            APIKnowledgeSynonymMutator()
        ]

    def mutate(self, api_knowledge: APIKnowledge) -> Set[APIKnowledge]:
        new_knowledge = set()
        if api_knowledge is None:
            return set()
        for mutator in self.mutators:
            mutated_knowledge = mutator.mutate(api_knowledge)
            new_knowledge.update(mutated_knowledge)
        return new_knowledge

    def mutate_knowledge_list(self, knowledge_set: Iterable[APIKnowledge]) -> Set[APIKnowledge]:
        new_knowledge = set()
        for knowledge in knowledge_set:
            new_knowledge.update(self.mutate(knowledge))
        return new_knowledge

