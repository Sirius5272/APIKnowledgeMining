"""
生成一些数据用于标注
"""
import csv
import json
import random

from util.path_util import PathUtil

if __name__ == "__main__":
    with open(PathUtil.sentence_data_from_answer_json(), encoding='utf-8') as f:
        sentence_data = json.load(f)
        sampled_sentence = random.sample(sentence_data, 2000)
        header = ["id", "title", "score", "containsAPI", "sentence"]
        rows = []
        labeled_sentence = json.load(open(PathUtil.labeled_sentence_cache(), encoding='utf-8'))
        for sentence in sampled_sentence:
            if sentence not in labeled_sentence:
                row = {
                    "id": sentence["id"],
                    "title": sentence["title"],
                    "score": sentence["score"],
                    "sentence": sentence["sentence"],
                    "containsAPI": sentence["qualified_name"]
                }
                rows.append(row)
        with open(PathUtil.unlabeled_sentence_data_csv(data="0617"), 'w', newline='', encoding='utf-8') as f2:
            f_csv = csv.DictWriter(f2, header)
            f_csv.writeheader()
            f_csv.writerows(rows)
