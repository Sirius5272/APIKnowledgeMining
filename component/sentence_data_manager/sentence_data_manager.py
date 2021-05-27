"""
一个用于从服务器上的数据库里获取Stack Overflow上的句子数据的类。
从服务器上获取到post的body后，进行分句，然后存在本地json中。
"""
import json
from bs4 import BeautifulSoup
import re
import pymysql
from component.sentence_data_manager.spacy_model import spacy_model


class SentenceDataManager:
    connection = None

    def __init__(self, host, user, password, db, charset="utf8", port=3306):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.charset = charset
        self.nlp = spacy_model()

    def get_connection(self):
        self.connection = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.db,
            charset=self.charset
        )

    def execute_sql(self, sql):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def close_connection(self):
        if self.connection:
            self.connection.close()

    @staticmethod
    def write_list_to_json(data, file_name):
        json_obj = json.dumps(data, indent=4)
        file_object = open(file_name, 'w')
        file_object.write(json_obj)
        file_object.close()

    def clean_post_split_to_sentence(self, clean_post):
        """
        使用spacy将post解析，切割成句子
        :return:
        """
        doc = self.nlp(clean_post)
        sentences = doc.sents
        return [item.text for item in sentences]

    @staticmethod
    def clean_html_tags(post):
        """
        使用beautiful soup解析post，去除html标签
        :return:
        """
        bs = BeautifulSoup(post, "html.parser")

        for pre in bs.find_all("pre"):
            for code in pre.find_all("code"):
                code.replace_with("_CODE_")
        string_list = bs.stripped_strings
        return ' '.join(string_list).replace("\n", "")

    @staticmethod
    def clean_code_part(post):
        """
        把post里的code标签替换成_CODE_.用bs做还是字符串匹配？
        :param post:
        :return:
        """

        pass

    @staticmethod
    def contains_api_name(post):
        # 直接匹配API会匹出代码部分，要先把post里的<code>部分删掉？
        re_1 = r'[a-zA-Z]([a-z]+)([A-Z][a-z]+)+'
        re_2 = r'[a-zA-Z][a-z]+(\.[a-z]+)+'
        search_obj_1 = re.search(re_1, post)
        search_obj_2 = re.search(re_2, post)
        if search_obj_1 and search_obj_2:
            return True
        return False
