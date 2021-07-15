"""
用来把post_data.json数据转化成fast text 模型训练需要的数据格式
"""
import random

from util.path_util import PathUtil
from util.tool import Tool
import json
import csv
from scripts.data_related.generate_positive_data_from_kg import PositiveDataGenerator
from component.sentence_data_manager.sentence_data_manager import SentenceDataManager


# 把标注好的csv数据转换成训练数据
def csv_to_txt_data():
    csv_reader = csv.reader(open(PathUtil.labeled_data(date="0713"), encoding='utf-8'))

    new_list = []
    for line in csv_reader:
        if line[5] == "1":
            new_list.append(SentenceDataManager.replace_api_with_placeholder(line[4]) + "\t" + "__label__1\n")
        elif line[5] == "2":
            new_list.append(SentenceDataManager.replace_api_with_placeholder(line[4]) + '\t' + "__label__0\n")
    random.shuffle(new_list)
    test_data = new_list[:int(len(new_list) * 0.2)]
    train_data = new_list[int(len(new_list) * 0.2):]
    with open(PathUtil.api_sentence_classifier_train_data(date="0715_placeholder"), 'w', encoding='utf-8') as f2:
        f2.writelines(train_data)
    with open(PathUtil.api_sentence_classifier_test_data(date="0715_placeholder"), 'w', encoding='utf-8') as f3:
        f3.writelines(test_data)


def mix_data_with_extra_positive_data():
    csv_reader = csv.reader(open(PathUtil.labeled_data(date="0713"), encoding='utf-8'))
    new_list = []
    for line in csv_reader:
        if line[5] == "1":
            new_list.append(line[4] + "\t" + "__label__1\n")
        elif line[5] == "2":
            new_list.append(line[4] + '\t' + "__label__0\n")
    new_list.extend(PositiveDataGenerator.generate_data_from_kg())
    random.shuffle(new_list)
    test_data = new_list[:int(len(new_list) * 0.2)]
    train_data = new_list[int(len(new_list) * 0.2):]
    with open(PathUtil.api_sentence_classifier_train_data(date="0714"), 'w', encoding='utf-8') as f2:
        f2.writelines(train_data)
    with open(PathUtil.api_sentence_classifier_test_data(date="0714"), 'w', encoding='utf-8') as f3:
        f3.writelines(test_data)


def generate_train_test_data_from_exist_positive_data():
    csv_reader = csv.reader(open(PathUtil.labeled_data(date="0713"), encoding='utf-8'))
    new_list = []
    for line in csv_reader:
        if line[5] == "1":
            new_list.append(line[4] + "\t" + "__label__1\n")
        elif line[5] == "2":
            new_list.append(line[4] + '\t' + "__label__0\n")
    random.shuffle(new_list)
    test_data = new_list[:int(len(new_list) * 0.3)]
    train_data = new_list[int(len(new_list) * 0.3):]

    positive_data = open(PathUtil.positive_data_from_kg(), 'r', encoding='utf-8').readlines()
    train_data.extend(positive_data)
    with open(PathUtil.api_sentence_classifier_train_data(date="0714_test_data_no_mix"), 'w', encoding='utf-8') as f2:
        f2.writelines(train_data)
    with open(PathUtil.api_sentence_classifier_test_data(date="0714_test_data_no_mix"), 'w', encoding='utf-8') as f3:
        f3.writelines(test_data)


if __name__ == "__main__":
    csv_to_txt_data()
