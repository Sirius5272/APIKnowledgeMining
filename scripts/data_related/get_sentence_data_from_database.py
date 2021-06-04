"""
从远端数据库获取SO数据，并保存到本地json文件
"""
import json
import tqdm
from component.sentence_data_manager.sentence_data_manager import SentenceDataManager
from util.path_util import PathUtil


class GetPostDataFromDatabase:
    @staticmethod
    def run(host, user, password, db, sql, port=3306, charset="utf8", score=0):
        manager = SentenceDataManager(
            host=host,
            port=port,
            user=user,
            password=password,
            db=db,
            charset=charset
        )
        manager.get_connection()
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
        SentenceDataManager.write_list_to_json(temp_data, PathUtil.post_data_json())

    @staticmethod
    def process_data_with_spacy_model(post_data_path, new_data_path):
        # todo: 用spacy处理保存下来的post_data.json
        with open(post_data_path, encoding="utf-8") as f:
            post_data = json.load(f)
            sentence_data = []
            wrong_num = 0
            for post in tqdm.tqdm(post_data):
                try:
                    clean_post = SentenceDataManager.clean_html_tags(post["body"])
                    if SentenceDataManager.contains_api_name(clean_post):
                        sentence_list = SentenceDataManager.clean_post_split_to_sentence(clean_post)
                        for sentence in sentence_list:
                            temp_dict = {
                                "id": post["id"],
                                "score": post["score"],
                                "sentence": sentence,
                                "title": post["title"]
                            }
                            sentence_data.append(temp_dict)
                except:
                    wrong_num += 1
            SentenceDataManager.write_list_to_json(sentence_data, new_data_path)
            print(wrong_num)

        pass


if __name__ == "__main__":
    HOST = '10.176.34.89'
    USER = 'root'
    PASSWORD = '123456'
    DB = 'stackoverflow_2021'

    SQL = "SELECT Id, Score, Body, Title FROM stackoverflow_2021.posts WHERE Tags LIKE '%<java>%' LIMIT 100"

    GetPostDataFromDatabase.process_data_with_spacy_model(PathUtil.post_data_json(), PathUtil.sentence_data_json())
    # GetPostDataFromDatabase.run(host=HOST,
    #                             user=USER,
    #                             password=PASSWORD,
    #                             db=DB,
    #                             sql=SQL)
