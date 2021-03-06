from pathlib import Path
from definitions import DATA_DIR, OUTPUT_DIR
import time


class PathUtil:
    @classmethod
    def post_data_json(cls, filename="post_data.json"):
        path = Path(DATA_DIR)
        path.mkdir(exist_ok=True)
        return str(path / "{filename}".format(filename=filename))

    @classmethod
    def post_data_with_type_json(cls, filename="post_data_with_posttype.json"):
        path = Path(DATA_DIR)
        path.mkdir(exist_ok=True)
        return str(path / "{filename}".format(filename=filename))

    @classmethod
    def post_data_from_java_answer(cls, filename="post_data_from_answer.json"):
        path = Path(DATA_DIR)
        path.mkdir(exist_ok=True)
        return str(path / "{filename}".format(filename=filename))

    @classmethod
    def sentence_data_json(cls, filename="sentence_data.json"):
        path = Path(DATA_DIR)
        path.mkdir(exist_ok=True)
        return str(path / "{filename}".format(filename=filename))

    @classmethod
    def sentence_data_from_answer_json(cls, filename="sentence_data_from_answer.json"):
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
    def api_sentence_classifier_model(cls, filename="api_sentence_model", date="0618"):
        path = Path(DATA_DIR)
        path.mkdir(exist_ok=True)
        return str(path / "classifier" / "{filename}_{date}.bin".format(filename=filename, date=date))

    @classmethod
    def api_sentence_classifier_train_data(cls, filename="api_sentence_train", date="0617"):
        path = Path(DATA_DIR)
        path.mkdir(exist_ok=True)
        return str(path / "classifier" / "{filename}_{date}.txt".format(filename=filename, date=date))

    @classmethod
    def api_sentence_classifier_test_data(cls, filename="api_sentence_test", date="0617"):
        path = Path(DATA_DIR)
        path.mkdir(exist_ok=True)
        return str(path / "classifier" / "{filename}_{date}.txt".format(filename=filename, date=date))

    @classmethod
    def api_name_json(cls, date, filename="api_name"):
        path = Path(DATA_DIR)
        path.mkdir(exist_ok=True)
        return str(path / "{filename}_{date}.json".format(filename=filename, date=date))

    @classmethod
    def jdk_graph(cls, filename="jdk.v1.graph"):
        path = Path(DATA_DIR)
        path.mkdir(exist_ok=True)
        return str(path / "{filename}".format(filename=filename))

    @classmethod
    def jdk_dc(cls, filename="jdk.v1.dc"):
        path = Path(DATA_DIR)
        path.mkdir(exist_ok=True)
        return str(path / "{filename}".format(filename=filename))

    @classmethod
    def api_name_from_jdk_graph(cls, filename="jdk_api_name.json"):
        path = Path(DATA_DIR)
        path.mkdir(exist_ok=True)
        return str(path / "{filename}".format(filename=filename))

    @classmethod
    def api_name_from_jdk_graph_new(cls, filename="new_jdk_api_name.json"):
        path = Path(DATA_DIR)
        path.mkdir(exist_ok=True)
        return str(path / "{filename}".format(filename=filename))

    @classmethod
    def test_data_json(cls, filename='test.json'):
        path = Path(DATA_DIR)
        path.mkdir(exist_ok=True)
        return str(path / "{filename}".format(filename=filename))

    @classmethod
    def labeled_data(cls, filename="labeled_sentence", date="0617"):
        path = Path(DATA_DIR)
        path.mkdir(exist_ok=True)
        return str(path / "{filename}_{date}.csv".format(filename=filename, date=date))

    @classmethod
    def nlp_doc_cache(cls):
        return str(Path(DATA_DIR) / "nlp_doc_cache.cache")

    @classmethod
    def log_file_named_with_current_time(cls, ):
        """
        ?????????????????????log????????????,???????????????????????????
        :return:
        """
        output_dir_log = Path(OUTPUT_DIR) / "log"
        output_dir_log.mkdir(exist_ok=True, parents=True)
        log_file_name = time.strftime("%Y%m%d-%H-%M", time.localtime())
        return str(output_dir_log / "{name}.log".format(name=log_file_name))

    @classmethod
    def seed_selector(cls):
        """
        selector???????????????
        :return:
        """
        return str(Path(OUTPUT_DIR) / "snowball_result_selector.cache")

    @classmethod
    def snowball_result(cls):
        """
        ????????????snowball_result?????????????????????????????????????????????

        :return:
        """
        return str(Path(OUTPUT_DIR) / "snowball_result.snr")

    @classmethod
    def snowball_result_after_filter(cls):
        return str(Path(OUTPUT_DIR) / "snowball_result_after_filter.snr")

    @classmethod
    def positive_data_from_kg(cls):
        return str(Path(OUTPUT_DIR) / "positive_data_from_kg.txt")

    @classmethod
    def all_sentence_dict(cls):
        return str(Path(DATA_DIR) / "all_sentence_dict.json")

    @classmethod
    def filtered_sentence_dict(cls, score=0.4):
        return str(Path(DATA_DIR) / "filtered_sentence_dict_{score}.json".format(score=score))

    @classmethod
    def seed_api_knowledge_list(cls):
        return str(Path(DATA_DIR) / "seed_api_knowledge.json")

    @classmethod
    def seed_sentence_list(cls):
        return str(Path(DATA_DIR) / "seed_sentence.json")

    @classmethod
    def api_knowledge_kg(cls):
        return str(Path(OUTPUT_DIR) / "api_knowledge_kg.kg")
