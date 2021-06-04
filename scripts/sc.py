import csv
from util.path_util import PathUtil
import json

if __name__ == "__main__":
    csv_reader = csv.reader(open(PathUtil.unlabeled_sentence_data_csv(), encoding="utf-8"))
    labeled_sentence = []
    for row in csv_reader:
        labeled_sentence.append(row[3])

    json_obj = json.dumps(list(set(labeled_sentence)), indent=4)
    file_object = open(PathUtil.labeled_sentence_cache(), 'w')
    file_object.write(json_obj)
    file_object.close()
