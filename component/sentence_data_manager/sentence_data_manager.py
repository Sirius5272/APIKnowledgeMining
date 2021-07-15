"""
一个用于从服务器上的数据库里获取Stack Overflow上的句子数据的类。
从服务器上获取到post的body后，进行分句，然后存在本地json中。
"""
import json
from bs4 import BeautifulSoup
import re
import pymysql
from util.path_util import PathUtil
from component.sentence_data_manager.spacy_model import spacy_model


class SentenceDataManager:
    nlp = None
    api_alias_to_qualified_name_dict = None

    def __init__(self):
        self.connection = None

    def get_connection(self, host, user, password, db, charset='utf-8', port=3306):
        self.connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            db=db,
            charset=charset
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

    @classmethod
    def clean_post_split_to_sentence(cls, clean_post):
        """
        使用spacy将post解析，切割成句子
        :return:
        """
        if cls.nlp is None:
            cls.nlp = spacy_model()
        doc = cls.nlp(clean_post)
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
                code.replace_with("_CODE_. ")
        string_list = bs.stripped_strings
        return ' '.join(string_list).replace("\n", "")

    @classmethod
    def contains_api_name(cls, _sentence):
        if not cls.api_alias_to_qualified_name_dict:
            cls.load_api_name_dict()
        # 直接匹配API会匹出代码部分，要先把post里的<code>部分删掉？

        re_full_name = r'([a-z]+\.)*[A-Z][a-z]+\.[a-z]+([A-Z][a-z]+)*(\(\S*\))?'
        # 这个表达式可以匹配完整API名，不管带不带参数，既要有包名也要有类名和方法名。带不带参数都可以。
        re_camel_case_name = r'(([A-Za-z][a-z]+)+\.)?[a-z]+[A-Z][a-z]+(\(\S*\))?'
        # 匹配驼峰式命名，匹配方法名+类名，也可能是对象名。类名可能不存在。带不带参数都可以
        re_class_name = r'([a-z]+\.)+([A-Z][a-z]+)+(\(\S*\))?'
        # 带包名的类名提及，带不带参数都可以。带就是构造函数
        re_only_class_name = r'([A-Z][a-z]+)+(\(\S*\))'
        # 不带包名的类名提及，一定要有参数 表示这是个构造函数。

        search_res = [re.search(re_full_name, _sentence),
                      re.search(re_camel_case_name, _sentence),
                      re.search(re_class_name, _sentence),
                      re.search(re_only_class_name, _sentence)]
        for search_obj in search_res:
            if search_obj:
                matched_name = search_obj.group()
                if matched_name in cls.api_alias_to_qualified_name_dict.keys():
                    return {"sentence": _sentence, "qualified_name": cls.api_alias_to_qualified_name_dict[matched_name]}
        return None

    @classmethod
    def load_api_name_dict(cls):
        if not cls.api_alias_to_qualified_name_dict:
            with open(PathUtil.api_name_from_jdk_graph()) as f:
                cls.api_alias_to_qualified_name_dict = json.load(f)

    @classmethod
    def replace_api_with_placeholder(cls, sentence):
        """
        把句子中的API提及给替换成占位符。这个不返回识别到的api，因为这个会吧句子里的所有API都给替换掉。
        :param sentence:
        :return:
        """
        re_full_name = r'([a-z]+\.)*[A-Z][a-z]+\.[a-z]+([A-Z][a-z]+)*(\(\S*\))?'
        # 这个表达式可以匹配完整API名，不管带不带参数，既要有包名也要有类名和方法名。带不带参数都可以。
        re_camel_case_name = r'(([A-Za-z][a-z]+)+\.)?[a-z]+[A-Z][a-z]+(\(\S*\))?'
        # 匹配驼峰式命名，匹配方法名+类名，也可能是对象名。类名可能不存在。带不带参数都可以
        re_class_name = r'([a-z]+\.)+([A-Z][a-z]+)+(\(\S*\))?'
        # 带包名的类名提及，带不带参数都可以。带就是构造函数
        re_only_class_name = r'([A-Z][a-z]+)+(\(\S*\))'
        # 不带包名的类名提及，一定要有参数 表示这是个构造函数。

        rex_list = [
            re_full_name, re_camel_case_name, re_class_name, re_only_class_name
        ]
        for rex in rex_list:
            search_obj = re.search(rex, sentence)
            while search_obj is not None:
                temp_sentence = []
                if search_obj:
                    match_name = search_obj.group()
                    if cls.nlp is None:
                        cls.nlp = spacy_model()
                    doc = cls.nlp(sentence)
                    for token in doc:
                        if match_name in str(token):
                            temp_sentence.append("_api_")
                        else:
                            temp_sentence.append(str(token))
                    sentence = " ".join(temp_sentence)
                search_obj = re.search(rex, sentence)
        return sentence
