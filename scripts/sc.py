import csv
from util.path_util import PathUtil
from component.sentence_data_manager.sentence_data_manager import SentenceDataManager
import json

if __name__ == "__main__":
    with open(PathUtil.sentence_data_from_answer_json()) as f:
        data = json.load(f)
        print(len(data))

