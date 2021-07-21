import copy
from typing import List
from nltk.corpus import wordnet
from component.model.factory.api_knowledge_mutator.api_knowledge_mutator import APIKnowledgeMutator
from component.model.api_knowledge import APIKnowledge


class APIKnowledgeSynonymMutator(APIKnowledgeMutator):
    def mutate(self, api_knowledge: APIKnowledge) -> List[APIKnowledge]:
        name_list = api_knowledge.get_all_object_names()
        result = []
        for name in name_list:
            value = api_knowledge.get_object_by_key(name)
            for syn in wordnet.synsets(value):
                for lm in syn.lemmas():
                    new_knowledge = copy.deepcopy(api_knowledge)
                    new_knowledge.update_argument(name, lm.name())
                    result.append(new_knowledge)
        return list(set(result))
