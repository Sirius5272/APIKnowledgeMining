from component.fast_text_classifier.api_sentence_classifier import APISentenceClassifier
from util.path_util import PathUtil


def run():
    classifier = APISentenceClassifier()
    classifier.train(PathUtil.api_sentence_classifier_train_data(date="0715_placeholder"))
    classifier.save(PathUtil.api_sentence_classifier_model(date="0715_placeholder"))
    classifier.test(PathUtil.api_sentence_classifier_test_data(date="0715_placeholder"))


if __name__ == "__main__":
    run()
