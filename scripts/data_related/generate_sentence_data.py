from component.sentence_data_manager.sentence_data_manager import SentenceDataManager
from util.data_util import DataUtil
from util.path_util import PathUtil
import json
from component.fast_text_classifier.api_sentence_classifier import APISentenceClassifier


if __name__ == "__main__":
    all_sentence_dict = json.load(open(PathUtil.all_sentence_dict(), 'r'))
    filtered_list = []
    classifier = APISentenceClassifier()
    classifier.load(PathUtil.api_sentence_classifier_model(date="0716_expand_placeholder"))
    for sentence_dict in all_sentence_dict:
        # result = classifier.is_api_sentence(sentence_dict["sentence"])
        score = classifier.get_score(sentence_dict["sentence"])
        if score >= 0.999:
            filtered_list.append(sentence_dict)
    print(len(filtered_list))
    print(len(all_sentence_dict))
    DataUtil.write_list_to_json(filtered_list, PathUtil.filtered_sentence_dict(score=0.999))

