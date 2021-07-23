import csv
import functools

from util.path_util import PathUtil
from component.sentence_data_manager.sentence_data_manager import SentenceDataManager
import json
from component.model.snowball_result import SnowBallResult
import random
from nltk.corpus import stopwords
from component.filter.filter import Filter
from component.matcher.matcher_helper import PatternCollection
from component.model.api_knowledge import APIKnowledgeCollection
from component.model.api_knowledge_instance import APIKnowledgeInstanceCollection
from util.log_util import LogUtil
from util.data_util import DataUtil


def cmp(a: str, b: str):
    if len(a) < len(b):
        return -1
    elif len(a) > len(b):
        return 1
    return 0


if __name__ == "__main__":
    new_jdk_api_name_data = json.load(open(PathUtil.api_name_from_jdk_graph_new()))
    new_data = {}
    for key, value in new_jdk_api_name_data.items():
        value = sorted(value, key=functools.cmp_to_key(cmp))
        new_data[key] = value
    DataUtil.write_list_to_json(new_data, PathUtil.api_name_from_jdk_graph_new())
    # input_path = PathUtil.snowball_result_after_filter()
    # snr: SnowBallResult = SnowBallResult.load(input_path)
    # instance_collection = snr.get_instance_collection()
    # instance_set = instance_collection.api_knowledge_instance_set
    # api_name_map = json.load(open(PathUtil.api_name_from_jdk_graph_new()))
    # in_count = 0
    # not_in_count = 0
    # for instance in instance_set:
    #     api_name = instance.get_sentence().api
    #     if api_name in api_name_map.keys():
    #         in_count += 1
    #     else:
    #         not_in_count += 1
    # print(in_count)
    # print(not_in_count)
    # input_path = PathUtil.snowball_result()
    # snr: SnowBallResult = SnowBallResult.load(input_path)
    # print(snr.simple_repr())
    # log_util = LogUtil.get_log_util()
    # instance_collection = snr.get_instance_collection()
    # instance_list = list(instance_collection.api_knowledge_instance_set)
    # rs = random.sample(instance_list, 100)
    # for each in rs:
    #     print(each)
    # _filter = Filter()
    # pattern_collection = snr.get_pattern_collection()
    # instance_collection = snr.get_instance_collection()
    # api_knowledge_collection = snr.get_api_knowledge_collection()
    # new_pc = PatternCollection()
    # new_ic = APIKnowledgeInstanceCollection()
    # new_ac = APIKnowledgeCollection()
    # for pattern in pattern_collection.pattern_set:
    #     if _filter.is_valid_api_knowledge(pattern.get_api_knowledge()):
    #         new_pc.add(pattern)
    # for instance in instance_collection.api_knowledge_instance_set:
    #     if _filter.is_valid_api_knowledge(instance.get_api_knowledge()):
    #         new_ic.add(instance)
    # for knowledge in api_knowledge_collection.APIKnowledge_set:
    #     if _filter.is_valid_api_knowledge(knowledge):
    #         new_ac.add(knowledge)
    # new_snr = SnowBallResult(pattern_collection=new_pc, instance_collection=new_ic, api_knowledge_collection=new_ac)
    # print(new_snr.simple_repr())
    # new_snr.save(PathUtil.snowball_result_after_filter())
