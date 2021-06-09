from pathlib import Path
from definitions import DATA_DIR, OUTPUT_DIR


class PathUtil:
    @classmethod
    def post_data_json(cls, filename="post_data.json"):
        path = Path(DATA_DIR)
        path.mkdir(exist_ok=True)
        return str(path / "{filename}".format(filename=filename))

    @classmethod
    def sentence_data_json(cls, filename="sentence_data.json"):
        path = Path(DATA_DIR)
        path.mkdir(exist_ok=True)
        return str(path / "{filename}".format(filename=filename))

    @classmethod
    def unlabeled_sentence_data_csv(cls, filename="unlabeled_sentence", data=""):
        path = Path(DATA_DIR)
        path.mkdir(exist_ok=True)
        return str(path / "{filename}_{data}.csv".format(filename=filename, data=data))

    @classmethod
    def labeled_sentence_cache(cls, filename="labeled_sentence.json"):
        path = Path(DATA_DIR)
        path.mkdir(exist_ok=True)
        return str(path / "{filename}".format(filename=filename))

    @classmethod
    def api_sentence_classifier_model(cls, filename="api_sentence_model.bin"):
        path = Path(DATA_DIR)
        path.mkdir(exist_ok=True)
        return str(path / "{filename}".format(filename=filename))

    @classmethod
    def api_sentence_classifier_train_data(cls, filename="api_sentence_train.txt"):
        path = Path(DATA_DIR)
        path.mkdir(exist_ok=True)
        return str(path / "{filename}".format(filename=filename))

    @classmethod
    def api_name_json(cls, filename="api_name.json"):
        path = Path(DATA_DIR)
        path.mkdir(exist_ok=True)
        return str(path / "{filename}".format(filename=filename))
