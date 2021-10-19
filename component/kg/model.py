from kgdt.utils import SaveLoad
from component.model.snowball_result import SnowBallResult
from util.path_util import PathUtil
import json
from typing import List
import functools


def cmp(a, b):
    if a[1] < b[1]:
        return 1
    if a[1] > b[1]:
        return -1
    return 0


class APIKnowledgeKG(SaveLoad):
    api_recognize_data = {}

    def __init__(self, snowball_result: SnowBallResult):
        self.snowball_result = snowball_result
        self.api_2_api_knowledge_id_map = {}
        self.api_2_instance_id_map = {}
        self.api_recognize_data = json.load(open(PathUtil.api_name_from_jdk_graph_new(), 'r', encoding='utf-8'))

    def build_api_2_instance_map(self):
        for instance in self.snowball_result.get_instance_collection().api_knowledge_instance_set:
            api_mention = instance.get_sentence().api
            instance_id = self.snowball_result.get_instance_id(instance)
            if api_mention in self.api_recognize_data.keys():
                api_full_name = self.find_api_full_name(api_mention)

                if api_full_name in self.api_2_instance_id_map.keys():
                    self.api_2_instance_id_map[api_full_name].append(instance_id)
                else:
                    self.api_2_instance_id_map[api_full_name] = [instance_id]
            else:
                if api_mention in self.api_2_instance_id_map.keys():
                    self.api_2_instance_id_map[api_mention].append(instance_id)
                else:
                    self.api_2_instance_id_map[api_mention] = [instance_id]

    def build_api_2_knowledge_map(self):
        for api_knowledge in self.snowball_result.get_api_knowledge_collection().APIKnowledge_set:
            api_mention = api_knowledge.get_api()
            knowledge_id = self.snowball_result.get_api_knowledge_id(api_knowledge)
            if api_mention in self.api_recognize_data.keys():
                api_full_name = self.find_api_full_name(api_mention)
                if api_full_name in self.api_2_api_knowledge_id_map.keys():
                    self.api_2_api_knowledge_id_map[api_full_name].append(knowledge_id)
                else:
                    self.api_2_api_knowledge_id_map[api_full_name] = [knowledge_id]
            else:
                if api_mention in self.api_2_api_knowledge_id_map.keys():
                    self.api_2_api_knowledge_id_map[api_mention].append(knowledge_id)
                else:
                    self.api_2_api_knowledge_id_map[api_mention] = [knowledge_id]

    def get_instances_by_api(self, api):
        if api not in self.api_2_instance_id_map.keys():
            return []
        id_list = self.api_2_instance_id_map[api]
        result = []
        for instance_id in id_list:
            instance = self.snowball_result.to_instance(instance_id)
            result.append(instance)
        return result

    def get_knowledge_by_api(self, api):
        if api not in self.api_2_api_knowledge_id_map.keys():
            return []
        id_list = self.api_2_api_knowledge_id_map[api]
        result = []
        for knowledge_id in id_list:
            api_knowledge = self.snowball_result.get_api_knowledge(knowledge_id)
            result.append(api_knowledge)
        return result

    def get_api_2_instance_number_list(self):
        api_list = self.api_2_instance_id_map.keys()
        result = []
        for api in api_list:
            result.append([api, len(self.api_2_instance_id_map[api])])
        result = sorted(result, key=functools.cmp_to_key(cmp))
        return result

    def find_api_full_name(self, api_mention) -> str:
        # 除了一些特殊的，名字短的优先匹配，
        # 特殊的有：toString hashCode
        # nextLine getName getClass readLine toArray
        # date() 这个大写是对的，小写是错的
        if api_mention in self.api_recognize_data.keys():
            return self.api_recognize_data[api_mention][0]
        else:
            return api_mention

    def print_simple(self):
        print("<Knowledge Graph \n APIDescriptiveKnowledgeCollection size=26552"
              "\n APIDescriptiveKnowledgeInstanceCollection size=42409>")


