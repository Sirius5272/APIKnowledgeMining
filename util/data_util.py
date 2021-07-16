from util.path_util import PathUtil
import json
from component.model.sentence import Sentence


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
        return sentence
