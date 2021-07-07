from typing import Iterable, Set, List
from kgdt.utils import SaveLoad
from component.model.api_knowledge import APIKnowledge, APIKnowledgeCollection
from component.model.api_knowledge_instance import APIKnowledgeInstance, APIKnowledgeInstanceCollection


class SeedSelector(SaveLoad):
    def __init__(self):
        self.selected_api_knowledge_collection = APIKnowledgeCollection()
        self.selected_api_knowledge_instance_collection = APIKnowledgeInstanceCollection()
        self.api_knowledge_step = 1  # 用来标注这是第几轮存下来的
        self.api_knowledge_instance_step = 1
        self.step_to_selected_api_knowledge_map = {}
        self.step_to_selected_instance_map = {}
        self.selected_api_knowledge_str = set()

    def select_new_seed_api_knowledge_list(self,
                                           api_knowledge_collection: Iterable[APIKnowledge]) -> Set[APIKnowledge]:
        available_api_knowledge_set = set(api_knowledge_collection) - set(self.selected_api_knowledge_collection)
        if len(available_api_knowledge_set) == 0:
            return set([])
        # 这里本来有根据得分筛选的。目前没有得分，所以直接返回。
        # todo:后面看需不需要加上得分
        self.add_used_api_knowledge(available_api_knowledge_set)
        self.step_to_selected_api_knowledge_map[self.api_knowledge_step] = available_api_knowledge_set
        self.api_knowledge_step += 1
        return available_api_knowledge_set

    def select_new_seed_instance_list(self,
                                      instance_collection: Iterable[APIKnowledgeInstance]) -> Set[APIKnowledgeInstance]:
        available_instance_set = set(instance_collection) - set(self.selected_api_knowledge_instance_collection)
        if len(available_instance_set) == 0:
            return set([])
        # 同上 没有得分筛选直接返回。
        # todo:后面看需不需要加上得分
        self.add_used_instance(available_instance_set)
        self.step_to_selected_instance_map[self.api_knowledge_instance_step] = available_instance_set
        self.api_knowledge_instance_step += 1
        return available_instance_set

    def filter_used_api_knowledge(self, api_knowledge_list: Iterable[APIKnowledge]) -> List[APIKnowledge]:
        api_knowledge_list = self.filter_in_given_set(api_knowledge_list)
        api_knowledge_list = self.filter_by_history(api_knowledge_list)
        return api_knowledge_list

    @staticmethod
    def filter_in_given_set(api_knowledge_list: Iterable[APIKnowledge]) -> List[APIKnowledge]:
        # 去重
        existing_set = set()
        result = []
        for each in api_knowledge_list:
            simple_str = each.to_str()
            if simple_str in existing_set:
                continue
            existing_set.add(simple_str)
            result.append(each)
        return result

    def filter_by_history(self, api_knowledge_list: Iterable[APIKnowledge]) -> List[APIKnowledge]:
        result = []
        for t in api_knowledge_list:
            simple_str = t.to_str()
            if simple_str in self.selected_api_knowledge_str:
                continue
            result.append(t)
        return result

    def add_used_api_knowledge(self, api_knowledge_list: Iterable[APIKnowledge]):
        self.selected_api_knowledge_collection.add_all(api_knowledge_list)
        for api_knowledge in api_knowledge_list:
            self.selected_api_knowledge_str.add(api_knowledge.to_str())

    def add_used_instance(self, instance_list: Iterable[APIKnowledgeInstance]):
        self.selected_api_knowledge_instance_collection.add_all(instance_list)
