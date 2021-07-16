import nlpaug.augmenter.word as naw
import csv
from util.path_util import PathUtil
import random
import tqdm
from component.sentence_data_manager.sentence_data_manager import SentenceDataManager
# aug = naw.SynonymAug(aug_src='wordnet')
# text = 'The quick brown fox jumps over the lazy dog .'
# augmented_text = aug.augment(text, 2)
# print("Original:")
# print(text)
# print("Augmented Text:")
# print(augmented_text)


def expand_positive_data_from_so():
    csv_reader = csv.reader(open(PathUtil.labeled_data(date="0713"), encoding='utf-8'))
    aug = naw.SynonymAug(aug_src='wordnet')
    new_list = []
    for line in csv_reader:
        if line[5] == "1":
            new_list.append(SentenceDataManager.replace_api_with_placeholder(line[4]) + "\t" + "__label__1\n")
        elif line[5] == "2":
            new_list.append(SentenceDataManager.replace_api_with_placeholder(line[4]) + '\t' + "__label__0\n")
    random.shuffle(new_list)
    test_data = new_list[:int(len(new_list) * 0.3)]
    train_data = new_list[int(len(new_list) * 0.3):]
    print("start expand")
    new_train_data = []

    for sentence in tqdm.tqdm(train_data):
        new_train_data.append(sentence)
        if "__label__1" in sentence:
            new_sentences = aug.augment(sentence, 2)
            for new_sentence in new_sentences:
                new_train_data.append(new_sentence+'\n')

    print("end expand")
    print(len(new_train_data))
    print(len(test_data))
    random.shuffle(new_train_data)

    with open(PathUtil.api_sentence_classifier_train_data(date="0716_expand_placeholder"), 'w', encoding='utf-8') as f2:
        f2.writelines(new_train_data)
    with open(PathUtil.api_sentence_classifier_test_data(date="0716_expand_placeholder"), 'w', encoding='utf-8') as f3:
        f3.writelines(test_data)


if __name__ == "__main__":
    expand_positive_data_from_so()
