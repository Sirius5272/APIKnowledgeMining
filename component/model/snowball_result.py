from typing import Iterable, TypeVar, Tuple, Set, List

from kgdt.utils import SaveLoad

from component.matcher.matcher_helper import PatternCollection
from component.model.pattern import Pattern
from component.model.api_knowledge import APIKnowledgeCollection, APIKnowledge
from component.model.api_knowledge_instance import APIKnowledgeInstance, APIKnowledgeInstanceCollection

T = TypeVar('T', bound='SnowBallResult')


class SnowBallResult(SaveLoad):
    """
    储存滚雪球的结果。
    """

    def __init__(self,
                 pattern_collection: PatternCollection = None,
                 api_knowledge_collection: APIKnowledgeCollection = None,
                 instance_collection: APIKnowledgeInstanceCollection = None
                 ):
        if instance_collection is None:
            instance_collection = APIKnowledgeInstanceCollection()
        self.instance_collection = instance_collection

        if api_knowledge_collection is None:
            api_knowledge_collection = APIKnowledgeCollection()
        self.api_knowledge_collection = api_knowledge_collection

        if pattern_collection is None:
            pattern_collection = PatternCollection()
        self.pattern_collection = pattern_collection

        # 以下的几个map存的是pattern，api_knowledge，api_knowledge_instance之间的关系，这里利用id来存，提高查询效率。
        self.pattern_2_instance_map = {}
        self.instance_2_pattern_map = {}

        self.api_knowledge_2_instance_map = {}
        self.instance_2_api_knowledge_map = {}

        # 和api_knowledge有关的缓存
        self.api_2_api_knowledge_map = {}
        self.object_2_api_knowledge_map = {}
        self.argument_2_api_knowledge_map = {}
        self.argument_tuple_2_api_knowledge_map = {}

        # 和api_knowledge_instance有关的缓存
        self.api_2_instance_map = {}
        self.object_2_instance_map = {}
        self.argument_2_instance_map = {}
        self.argument_tuple_2_instance_map = {}

        self.word_2_argument_map = {}
        self.word_2_api_knowledge_map = {}
        self.word_2_instance_map = {}

    def __add_instance_cache(self, instance: APIKnowledgeInstance):
        instance_id = self.instance_collection.to_id(instance=instance)
        if instance_id == -1:
            return
        api_knowledge = instance.get_api_knowledge()
        api_knowledge_id = self.get_api_knowledge_id(api_knowledge)
        if api_knowledge_id == -1:
            return

        self.__add_cache_between_api_knowledge_and_instance(api_knowledge_id, instance_id)

        api = api_knowledge.get_api()
        # 增加api,api_knowledge 的map
        if api not in self.api_2_instance_map:
            self.api_2_instance_map[api] = set()
        self.api_2_instance_map[api].add(instance_id)

        # 增加object,api_knowledge 的map
        # todo: 这里的object和argument不一样啊 得看看
        for object in api_knowledge.get_all_argument_values():
            if object not in self.object_2_instance_map:
                self.object_2_instance_map[object] = set()
            self.object_2_instance_map[object].add(instance_id)

        # 增加argument,api_knowledge 的map
        for argument in api_knowledge.get_all_argument_values():
            if argument not in self.argument_2_instance_map:
                self.argument_2_instance_map[argument] = set()
            self.argument_2_instance_map[argument].add(instance_id)

            words = set(argument.split())
            for word in words:
                if word not in self.word_2_argument_map.keys():
                    self.word_2_argument_map[word] = set()
                if word not in self.word_2_instance_map.keys():
                    self.word_2_instance_map[word] = set()

                self.word_2_argument_map[word].add(argument)
                self.word_2_instance_map[word].add(instance_id)

        for argument_tuple in api_knowledge.get_possible_argument_combination():
            if argument_tuple not in self.argument_tuple_2_instance_map:
                self.argument_tuple_2_instance_map[argument_tuple] = set()
            self.argument_tuple_2_instance_map[argument_tuple].add(instance_id)

    def __add_cache_between_api_knowledge_and_instance(self, api_knowledge_id, instance_id):
        if api_knowledge_id not in self.api_2_instance_map:
            self.api_2_instance_map[api_knowledge_id] = set()
        if instance_id not in self.instance_2_api_knowledge_map:
            self.instance_2_api_knowledge_map[instance_id] = set()
        self.api_knowledge_2_instance_map[api_knowledge_id].add(instance_id)
        self.instance_2_api_knowledge_map[instance_id].add(api_knowledge_id)

    def __add_api_knowledge_cache(self, api_knowledge: APIKnowledge):
        api_knowledge_id = self.get_api_knowledge_id(api_knowledge)
        if api_knowledge_id == -1:
            return
        api = api_knowledge.get_api()
        # 增加action,api_knowledge 的map
        if api not in self.api_2_api_knowledge_map:
            self.api_2_api_knowledge_map[api] = set()
        self.api_2_api_knowledge_map[api].add(api_knowledge_id)

        # 增加object,api_knowledge 的map
        for object in api_knowledge.get_all_argument_values():
            if object not in self.object_2_api_knowledge_map:
                self.object_2_api_knowledge_map[object] = set()
            self.object_2_api_knowledge_map[object].add(api_knowledge_id)

        # 增加argument,api_knowledge 的map
        for argument in api_knowledge.get_all_argument_values():
            if argument not in self.argument_2_api_knowledge_map:
                self.argument_2_api_knowledge_map[argument] = set()
            self.argument_2_api_knowledge_map[argument].add(api_knowledge_id)

            words = set(argument.split())
            for word in words:
                if word not in self.word_2_argument_map.keys():
                    self.word_2_argument_map[word] = set()
                self.word_2_argument_map[word].add(argument)
                if word not in self.word_2_api_knowledge_map.keys():
                    self.word_2_api_knowledge_map[word] = set()
                self.word_2_api_knowledge_map[word].add(api_knowledge_id)

        for argument_tuple in api_knowledge.get_possible_argument_combination():
            if argument_tuple not in self.argument_tuple_2_api_knowledge_map:
                self.argument_tuple_2_api_knowledge_map[argument_tuple] = set()
            self.argument_tuple_2_api_knowledge_map[argument_tuple].add(api_knowledge_id)

    def get_api_knowledge_id(self, api_knowledge: APIKnowledge):
        return self.api_knowledge_collection.to_id(api_knowledge)

    def get_instance_id(self, instance: APIKnowledgeInstance):
        return self.instance_collection.to_id(instance)

    def get_pattern_id(self, pattern: Pattern):
        return self.pattern_collection.to_id(pattern)

    def __repr__(self):
        return "<SnowBallResult \n%r\n%r\n%r>" % (
            self.api_knowledge_collection, self.instance_collection, self.pattern_collection)

    def simple_repr(self):
        return "<SnowBallResult \n%r\n%r\n%r>" % (
            self.api_knowledge_collection.simple_repr(), self.instance_collection.simple_repr(),
            self.pattern_collection.simple_repr())

    def add_pattern(self, pattern: Pattern) -> int:
        if pattern is None:
            return -1
        pattern_id = self.pattern_collection.add(pattern)
        return pattern_id

    def add_api_knowledge(self, api_knowledge: APIKnowledge) -> int:
        if api_knowledge is None:
            return -1
        api_knowledge_id = self.api_knowledge_collection.add(api_knowledge)
        self.__add_api_knowledge_cache(api_knowledge)
        return api_knowledge_id

    def add_instance(self, instance: APIKnowledgeInstance) -> int:
        if instance is None:
            return -1
        self.add_api_knowledge(instance.get_api_knowledge())
        instance_id = self.instance_collection.add(instance=instance)
        self.__add_instance_cache(instance)
        return instance_id

    def add_instances(self, instance_list: Iterable[APIKnowledgeInstance]):
        for instance in instance_list:
            self.add_instance(instance)

    def add_api_knowledge_list(self, api_knowledge_list: Iterable[APIKnowledge]):
        for t in api_knowledge_list:
            self.add_api_knowledge(api_knowledge=t)

    def add_patterns(self, patterns: Iterable[Pattern]):
        for t in patterns:
            self.add_pattern(t)

    def get_instance_collection(self):
        return self.instance_collection

    def get_pattern_collection(self):
        return self.pattern_collection

    def get_api_knowledge_collection(self):
        return self.api_knowledge_collection

    def add_all(self, result: T):
        self.add_patterns(result.get_pattern_collection())
        self.add_instances(result.get_instance_collection())
        self.add_api_knowledge_list(result.get_api_knowledge_collection())
        self.add_pattern_with_instance_relations(result.get_pattern_with_instance_relations())

    def add_pattern_with_instance(self, pattern: Pattern, instance: APIKnowledgeInstance):
        p_id = self.add_pattern(pattern)
        if p_id < 0:
            return
        instance_id = self.add_instance(instance)
        if instance_id < 0:
            return
        self.__add_cache_between_pattern_and_instance(instance_id, p_id)

    def __add_cache_between_pattern_and_instance(self, instance_id, p_id):
        if p_id not in self.pattern_2_instance_map:
            self.pattern_2_instance_map[p_id] = set([])
        if instance_id not in self.instance_2_pattern_map:
            self.instance_2_pattern_map[instance_id] = set([])
        self.pattern_2_instance_map[p_id].add(instance_id)
        self.instance_2_pattern_map[instance_id].add(p_id)

    def add_pattern_with_instance_relations(self, relations: Iterable[Tuple[Pattern, APIKnowledgeInstance]]):
        for pattern, instance in relations:
            self.add_pattern_with_instance(pattern=pattern, instance=instance)

    def get_pattern_with_instance_relations(self, ) -> Iterable[Tuple[Pattern, APIKnowledgeInstance]]:
        result = []
        for pattern_id, instance_id_set in self.pattern_2_instance_map.items():
            for instance_id in instance_id_set:
                result.append((self.pattern_collection.to_pattern(pattern_id),
                               self.instance_collection.to_instance(instance_id)))
        return result

    # 对于pattern, api_knowledge, api_knowledge_instance 之间关系的查询
    def get_instance_ids_by_pattern(self, pattern: Pattern):
        p_id = self.pattern_collection.add(pattern)
        if p_id < 0:
            return set([])
        return self.pattern_2_instance_map.get(p_id, set([]))

    # 对于pattern, api_knowledge, api_knowledge_instance 之间关系的查询

    # 对于pattern, api_knowledge, api_knowledge_instance 之间关系的查询
    def get_pattern_ids_by_instance(self, instance: APIKnowledgeInstance):
        instance_id = self.instance_collection.to_id(instance)
        if instance_id < 0:
            return set([])
        return self.instance_2_pattern_map.get(instance_id, set([]))

    def get_instances_by_pattern(self, pattern: Pattern):
        instance_ids = self.get_instance_ids_by_pattern(pattern=pattern)
        return self.instance_collection.to_instances(instance_ids)

    def get_api_knowledge_ids_by_pattern(self, pattern: Pattern) -> Set[int]:
        instance_ids = self.get_instance_ids_by_pattern(pattern=pattern)
        api_knowledge_ids = set()
        for instance_id in instance_ids:
            temp_ids = self.instance_2_api_knowledge_map.get(instance_id, set())
            api_knowledge_ids.update(temp_ids)
        return api_knowledge_ids

    def get_patterns_by_instance(self, instance: APIKnowledgeInstance):
        pattern_ids = self.get_pattern_ids_by_instance(instance=instance)
        return self.pattern_collection.to_patterns(pattern_ids)

    def get_instances_num_by_pattern(self, pattern: Pattern):
        instance_ids = self.get_instance_ids_by_pattern(pattern=pattern)
        return len(instance_ids)

    def get_api_knowledge_by_instance(self, instance: APIKnowledgeInstance):
        api_knowledge_id = self.api_knowledge_collection.add(instance.get_api_knowledge())
        return self.api_knowledge_collection.to_api_knowledge(api_knowledge_id)

    def has_api_knowledge(self, api_knowledge: APIKnowledge):
        return self.api_knowledge_collection.include(api_knowledge)

    def has_pattern(self, pattern: Pattern):
        return self.pattern_collection.include(pattern)

    def new_patterns(self, final_snowball_result: T) -> Set[Pattern]:
        return self.pattern_collection.new(final_snowball_result.get_pattern_collection())

    def new_api_knowledge(self, final_snowball_result: T) -> Set[APIKnowledge]:
        return self.api_knowledge_collection.new(final_snowball_result.get_api_knowledge_collection())

    def new_api_knowledge_instance(self, final_snowball_result: T) -> Set[APIKnowledgeInstance]:
        return self.instance_collection.new(final_snowball_result.get_instance_collection())

    def find_api_knowledge_by_api_object(self, api: str, object: str) -> List[APIKnowledge]:
        if api > object:
            api_object_tuple = (api, object)
        else:
            api_object_tuple = (object, api)
        id_set = self.argument_tuple_2_api_knowledge_map.get(api_object_tuple, set())
        api_knowledge_set = self.api_knowledge_collection.to_api_knowledge_list(id_set)
        return api_knowledge_set

    def find_api_knowledge_by_api(self, api: str) -> List[APIKnowledge]:
        id_set = self.api_2_api_knowledge_map.get(api, set())
        api_knowledge_set = self.api_knowledge_collection.to_api_knowledge_list(id_set)
        return api_knowledge_set

    def find_api_knowledge_by_object(self, object: str) -> List[APIKnowledge]:
        api_knowledge_id_set = self.object_2_api_knowledge_map.get(object, set())
        api_knowledge_set = self.api_knowledge_collection.to_api_knowledge_list(api_knowledge_id_set)
        return api_knowledge_set

    def get_instance_number_by_api_knowledge(self, api_knowledge: APIKnowledge) -> int:
        api_knowledge_id = self.get_api_knowledge_id(api_knowledge)
        instance_set = self.api_knowledge_2_instance_map.get(api_knowledge_id, set())
        return len(instance_set)

    def get_instance_number_by_api_knowledge_id(self, api_knowledge_id: int) -> int:
        instance_set = self.api_knowledge_2_instance_map.get(api_knowledge_id, set())
        return len(instance_set)

    def get_instances_by_api_knowledge(self, api_knowledge: APIKnowledge) -> List[APIKnowledgeInstance]:
        api_knowledge_id = self.get_api_knowledge_id(api_knowledge)
        instance_set = self.api_knowledge_2_instance_map.get(api_knowledge_id, set())
        return self.instance_collection.to_instances(instance_set)

    def get_instance_number_by_api_knowledge_list(self, api_knowledge_list: Iterable[APIKnowledge]) -> int:
        number = 0
        for api_knowledge in api_knowledge_list:
            n = self.get_instance_number_by_api_knowledge(api_knowledge)
            number = number + n
        return number

    def to_api_knowledge_list(self, ids: Iterable[int]) -> List[APIKnowledge]:
        return self.api_knowledge_collection.to_api_knowledge_list(ids)

    def get_instance_num_by_argument(self, argument: str) -> int:
        return len(self.argument_2_instance_map.get(argument, set()))

    def get_instance_num_by_word(self, word: str) -> int:
        return len(self.word_2_instance_map.get(word, set()))

    def get_api_knowledge_list_by_argument(self, argument) -> List[APIKnowledge]:
        api_knowledge_ids = self.argument_2_api_knowledge_map.get(argument, set())
        api_knowledge_list = self.api_knowledge_collection.to_api_knowledge_list(api_knowledge_ids)
        return api_knowledge_list

    def get_api_knowledge_ids_by_argument(self, argument) -> Set[int]:
        return self.argument_2_api_knowledge_map.get(argument, set())

    def to_api_knowledge_ids(self, api_knowledge_list: Iterable[APIKnowledge]) -> Set[int]:
        return self.api_knowledge_collection.to_ids(api_knowledge_list)

    def get_api_knowledge(self, api_knowledge_id):
        return self.api_knowledge_collection.to_api_knowledge(api_knowledge_id)

    def to_instance(self, instance_id):
        return self.instance_collection.to_instance(instance_id)

    def get_instance_ids_by_api_knowledge(self, api_knowledge_id: int) -> Set[int]:
        instance_set = self.api_2_instance_map.get(api_knowledge_id, set())
        return instance_set

    def get_instance_number_by_api(self, api):
        return len(self.api_2_instance_map.get(api, set()))

    def get_instance_ids_by_api(self, api):
        return self.api_2_instance_map.get(api, set())
