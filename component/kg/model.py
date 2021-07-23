from kgdt.utils import SaveLoad
from component.model.snowball_result import SnowBallResult
from util.path_util import PathUtil
import json


class APIKnowledgeKG(SaveLoad):
    api_recognize_data = {}

    def __init__(self, snowball_result: SnowBallResult):
        self.snowball_result = snowball_result
        self.api_2_api_knowledge_id_map = {}
        self.api_2_instance_id_map = {}
        self.api_recognize_data = json.load(PathUtil.api_name_from_jdk_graph_new())

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

    def find_api_full_name(self, api_mention) -> str:
        # 除了一些特殊的，名字短的优先匹配，
        # 特殊的有：toString hashCode
        # nextLine getName getClass readLine toArray
        # date() 这个大写是对的，小写是错的
        pass



