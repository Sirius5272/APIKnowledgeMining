from util.path_util import PathUtil
import json
from component.model.sentence import Sentence
from component.model.api_knowledge import APIKnowledge


class DataUtil:
    @classmethod
    def write_list_to_json(cls, data, file_name):
        json_obj = json.dumps(data, indent=4)
        file_object = open(file_name, 'w')
        file_object.write(json_obj)
        file_object.close()

    @classmethod
    def sentence_data(cls, path=PathUtil.all_sentence_dict()):
        with open(path, 'r', encoding='utf-8') as f:
            sentence_dict_list = json.load(f)
            seed_sentence = []
            for sentence in sentence_dict_list:
                seed_sentence.append(Sentence.from_dict(sentence))
            return seed_sentence

    @classmethod
    def seed_api_knowledge_data(cls, path=PathUtil.seed_api_knowledge_list()):
        with open(path, 'r') as f:
            api_knowledge_list = json.load(f)
            result = []
            for api_knowledge in api_knowledge_list:
                result.append(APIKnowledge.from_dict(api_knowledge))
            return result

    @classmethod
    def seed_sentence_data(cls, path=PathUtil.seed_sentence_list()):
        with open(path, 'r', encoding='utf-8') as f:
            sentence_dict_list = json.load(f)
            seed_sentence = []
            for sentence in sentence_dict_list:
                seed_sentence.append(Sentence.from_dict(sentence))
            return seed_sentence
