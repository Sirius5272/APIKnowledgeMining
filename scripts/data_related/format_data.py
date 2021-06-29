"""
用来把post_data.json数据转化成fast text 模型训练需要的数据格式
"""
import random

from util.path_util import PathUtil
from util.tool import Tool
import json
import csv


# 把标注好的csv数据转换成训练数据
def csv_to_txt_data():
    csv_reader = csv.reader(open(PathUtil.labeled_data(date="0617"), encoding='utf-8'))

    new_list = []
    for line in csv_reader:
        if line[5] == "1":
            new_list.append(line[4] + "\t" + "__label__1\n")
        elif line[5] == "2":
            new_list.append(line[4] + '\t' + "__label__0\n")
    random.shuffle(new_list)
    test_data = new_list[:int(len(new_list) * 0.2)]
    train_data = new_list[int(len(new_list) * 0.2):]
    with open(PathUtil.api_sentence_classifier_train_data(date="0618"), 'w', encoding='utf-8') as f2:
        f2.writelines(train_data)
    with open(PathUtil.api_sentence_classifier_test_data(date="0618"), 'w', encoding='utf-8') as f3:
        f3.writelines(test_data)


if __name__ == "__main__":
    csv_to_txt_data()
