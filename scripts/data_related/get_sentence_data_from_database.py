"""
从远端数据库获取SO数据，并保存到本地json文件
"""
import json
import tqdm
from component.sentence_data_manager.sentence_data_manager import SentenceDataManager
from util.path_util import PathUtil
import signal
from contextlib import contextmanager

# 以下TimeoutException和time_limit()是为了在超时的时候直接跳过，这段代码在windows平台无法使用，只能在unix平台使用。


# class TimeoutException(Exception): pass
#
#
# @contextmanager
# def time_limit(seconds):
#     def signal_handler(signum, frame):
#         raise TimeoutException("Timed out!")
#     signal.signal(signal.SIGALRM, signal_handler)
#     signal.alarm(seconds)
#     try:
#         yield
#     finally:
#         signal.alarm(0)


class GetPostDataFromDatabase:
    @staticmethod
    def run(host, user, password, db, sql, port=3306, charset="utf8", score=0, path=PathUtil.post_data_json()):
        manager = SentenceDataManager()
        manager.get_connection(host=host,
                               port=port,
                               user=user,
                               password=password,
                               db=db,
                               charset=charset)
        data = manager.execute_sql(sql)
        temp_data = []
        for each in data:
            if each[1] > score:
                temp_dict = {
                    "id": each[0],
                    "score": each[1],
                    "body": each[2],
                    "title": each[3]
                }
                temp_data.append(temp_dict)
        SentenceDataManager.write_list_to_json(temp_data, path)

    @staticmethod
    def process_data_with_spacy_model(post_data_path, new_data_path):
        # todo: 用spacy处理保存下来的post_data.json
        with open(post_data_path, encoding="utf-8") as f:
            post_data = json.load(f)
            post_data = post_data[4000:5000]
            sentence_data = []
            wrong_num = 0
            for post in tqdm.tqdm(post_data):
                # try:
                #     with time_limit(1):

                clean_post = SentenceDataManager.clean_html_tags(post["body"])
                if SentenceDataManager.contains_api_name(clean_post):
                    sentence_list = SentenceDataManager.clean_post_split_to_sentence(clean_post)
                    for sentence in sentence_list:
                        if len(sentence) <= 200:
                            contains_api = SentenceDataManager.contains_api_name(sentence)
                            if contains_api is not None:
                                temp_dict = {
                                    "id": post["id"],
                                    "score": post["score"],
                                    "sentence": sentence,
                                    "title": post["title"],
                                    "qualified_name": contains_api["qualified_name"]
                                }
                                sentence_data.append(temp_dict)
                # except TimeoutException as msg:
                #     wrong_num += 1
                #     print("Time out")

            SentenceDataManager.write_list_to_json(sentence_data, new_data_path)
            print(wrong_num)


if __name__ == "__main__":
    HOST = '10.176.34.89'
    USER = 'root'
    PASSWORD = '123456'
    DB = 'stackoverflow_2021'

    SQL = "SELECT t1.Id, t1.Score, t1.Body, t2.Title FROM stackoverflow_2021.posts AS t1 JOIN " \
          "stackoverflow_2021.posts AS t2 ON t1.parentId = t2.ID WHERE  t2.tags LIKE '%<java>%' " \
          "AND t1.posttypeid = 2 AND t1.score>0 LIMIT 100;"

    GetPostDataFromDatabase.process_data_with_spacy_model(PathUtil.post_data_from_java_answer(),
                                                          PathUtil.sentence_data_json())
    # GetPostDataFromDatabase.run(host=HOST,
    #                             user=USER,
    #                             password=PASSWORD,
    #                             db=DB,
    #                             sql=SQL,
    #                             path=PathUtil.test_data_json())
