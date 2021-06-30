from component.model.sentence import Sentence
from component.model.api_knowledge import APIKnowledge
import copy
from kgdt.utils import SaveLoad


class APIKnowledgeInstance:
    def __init__(self, sentence: Sentence, api_knowledge: APIKnowledge):
        self.sentence = copy.deepcopy(sentence)
        self.api_knowledge = copy.deepcopy(api_knowledge)

    def __hash__(self):
        return hash(str(self.sentence) + str(self.api_knowledge))

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, APIKnowledgeInstance):
            return False
        if self.sentence != other.sentence or self.api_knowledge != other.api_knowledge:
            return False
        return True

    def __repr__(self):
        return "<APIKnowledgeInstance [sentence: %s] [api knowledge: %s]" % (self.sentence.to_str(),
                                                                             self.api_knowledge.to_str())

    def get_sentence(self):
        return self.sentence

    def get_api_knowledge(self):
        return self.api_knowledge

    @staticmethod
    def from_dict(data: dict):
        sentence = Sentence.from_dict(data["sentence"])
        api_knowledge = APIKnowledge.from_dict(data["api_knowledge"])
        return APIKnowledgeInstance(sentence=sentence, api_knowledge=api_knowledge)

    def to_dict(self):
        r = {
            "sentence": self.sentence.to_dict(),
            "api_knowledge": self.api_knowledge.to_dict()
        }
        return r


class APIKnowledgeInstanceCollection(SaveLoad):
    def __init__(self):
        self.api_knowledge_instance_set = set([])
        self.api_knowledge_instance2id = {}
        self.id2api_knowledge_instance = {}
        self.max_id = 0

    def add(self, instance: APIKnowledgeInstance):
        if instance is None:
            return -1
        if instance in self.api_knowledge_instance2id:
            return self.api_knowledge_instance2id[instance]

        self.api_knowledge_instance_set.add(instance)
        instance_id = self.max_id
        self.api_knowledge_instance2id[instance] = instance_id
        self.id2api_knowledge_instance[instance_id] = instance
        self.max_id = instance_id + 1
        return instance_id

    def remove(self, instance: APIKnowledgeInstance):
        if instance is None:
            return
        if instance in self.api_knowledge_instance_set:
            self.api_knowledge_instance_set.remove(instance)
        if instance in self.api_knowledge_instance2id.keys():
            instance_id = self.api_knowledge_instance2id.pop(instance)
            if instance_id in self.id2api_knowledge_instance.keys():
                self.id2api_knowledge_instance.pop(instance_id)

    def remove_by_id(self, instance_id: int):
        api_knowledge = self.get_id_by_instance(instance_id)
        self.remove(api_knowledge)

    def get_instance_by_id(self, instance_id):
        return self.id2api_knowledge_instance.get(instance_id, None)

    def get_id_by_instance(self, instance):
        if instance is None:
            return -1
        if instance not in self.api_knowledge_instance_set:
            return -1
        return self.api_knowledge_instance2id.get(instance, -1)
