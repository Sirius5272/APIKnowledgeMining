# API Knowledge类，储存API知识的多元组
from kgdt.utils import SaveLoad


class APIKnowledge:
    """
    描述一个抽象的API知识，不与具体的API sentence关联
    """
    API = "API"
    OBJECTS = "objects"  # 所有不是API名的知识组成员都认为是objects。后面可能需要细化成action和adj。暂时全部以object概括
    ACTION = "action"
    ADJECTIVE = "adjective"  # 形容词和动词都不一定会出现。暂时先写下来，后面看怎么改。

    def __init__(self, api, **object_map):
        """
        构建一个APIKnowledge对象。保存该知识作用的API全限定名，以及该知识对应的object组成
        :param api:API的全限定名
        :param object_map:所有的object的名字和对应的值，可能会有action、adj等。
        """
        self.api = api
        self.object_map = {}
        self.update_objects(object_map)

    def update_objects(self, object_map):
        for p, v in object_map.items():
            self.object_map[p] = v

    def set_api(self, api):
        self.api = api

    def get_api(self):
        return self.api

    def set_object(self, name, value):
        self.object_map[name] = value

    def has_object(self, name):
        if name in self.object_map.keys():
            return True
        return False

    def get_object_by_key(self, key):
        if key not in self.object_map.keys():
            return None
        return self.object_map[key]

    def get_object_name_by_value(self, object_value):
        for name, value in self.object_map.items():
            if value == object_value:
                return name
        return None

    def change_object_name(self, old_name, new_name):
        if not self.has_object(old_name):
            return
        if self.has_object(new_name):
            return
        value = self.object_map.pop(old_name)
        self.object_map[new_name] = value

    def __hash__(self):
        return hash(
            self.api + " " + " ".join(set(self.object_map.items()))
        )

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, APIKnowledge):
            return False
        if self.api != other.api or set(self.object_map.items()) != set(other.object_map.items()):
            return False
        return True

    def __repr__(self):
        return "<Api knowledge %s>" % (self.to_str())

    def to_str(self):
        return "[api]: %s [objects]: %s" % \
               (self.get_api(),
                ",".join(list(["[%s = %s]" % (name, value) for name, value in self.object_map.items()])))

    @staticmethod
    def from_dict(data: dict):
        t = APIKnowledge(api=data[APIKnowledge.API], **data[APIKnowledge.OBJECTS])
        return t

    def to_dict(self):
        r = {
            APIKnowledge.API: self.api,
            APIKnowledge.OBJECTS: self.object_map
        }
        return r


class APIKnowledgeCollection(SaveLoad):
    def __init__(self):
        self.APIKnowledge_set = set([])
        self.id2APIKnowledge = {}
        self.APIKnowledge2id = {}
        self.max_id = 0

    def add(self, api_knowledge: APIKnowledge):
        """
        返回添加的APIKnowledge的ID，保证ID自增不重复
        :param api_knowledge:
        :return:
        """
        if api_knowledge is None:
            return -1
        if api_knowledge in self.APIKnowledge_set:
            return self.APIKnowledge2id[api_knowledge]

        self.APIKnowledge_set.add(api_knowledge)
        knowledge_id = self.max_id
        self.APIKnowledge2id[api_knowledge] = knowledge_id
        self.id2APIKnowledge[knowledge_id] = api_knowledge
        self.max_id = knowledge_id + 1
        return knowledge_id

    def remove(self, api_knowledge: APIKnowledge):
        if api_knowledge is None:
            return
        if api_knowledge in self.APIKnowledge_set:
            self.APIKnowledge_set.remove(api_knowledge)
        if api_knowledge in self.APIKnowledge2id.keys():
            api_knowledge_id = self.APIKnowledge2id.pop(api_knowledge)
            if api_knowledge_id in self.id2APIKnowledge.keys():
                self.id2APIKnowledge.pop(api_knowledge_id)

    def remove_by_id(self, api_knowledge_id: int):
        api_knowledge = self.get_api_knowledge_by_id(api_knowledge_id)
        self.remove(api_knowledge)

    def get_api_knowledge_by_id(self, api_knowledge_id):
        return self.id2APIKnowledge.get(api_knowledge_id, None)

    def get_id_by_api_knowledge(self, api_knowledge):
        if api_knowledge is None:
            return -1
        if api_knowledge not in self.APIKnowledge_set:
            return -1
        return self.APIKnowledge2id.get(api_knowledge, -1)

    def size(self) -> int:
        return len(self.id2APIKnowledge.keys())

    def __len__(self):
        return self.size()

    def get_all_task(self):
        return self.APIKnowledge_set
