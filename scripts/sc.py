import csv
from util.path_util import PathUtil
from component.sentence_data_manager.sentence_data_manager import SentenceDataManager
import json
from component.model.snowball_result import SnowBallResult


if __name__ == "__main__":
    input_path = PathUtil.snowball_result()
    snr: SnowBallResult = SnowBallResult.load(input_path)
    print(snr.simple_repr())

