"""
从远端数据库获取SO数据，并保存到本地json文件
"""
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
                clean_post = SentenceDataManager.clean_html_tags(each[2])
                if SentenceDataManager.contains_api_name(clean_post):
                    sentences_list = manager.clean_post_split_to_sentence(clean_post)
                    sentence_list = list(set(sentences_list).difference({" "}))

                    temp_dict = {
                        "id": each[0],
                        "score": each[1],
                        "body": sentence_list,
                        "title": each[3]
                    }
                    temp_data.append(temp_dict)
        SentenceDataManager.write_list_to_json(temp_data, PathUtil.post_data_json())


if __name__ == "__main__":
    HOST = '10.176.34.89'
    USER = 'root'
    PASSWORD = '123456'
    DB = 'stackoverflow_2021'

    SQL = "SELECT Id, Score, Body, Title FROM stackoverflow_2021.posts WHERE Tags LIKE '%<java>%' LIMIT 100"

    GetPostDataFromDatabase.run(host=HOST,
                                user=USER,
                                password=PASSWORD,
                                db=DB,
                                sql=SQL)
