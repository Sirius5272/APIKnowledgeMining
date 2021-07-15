from util.path_util import PathUtil
from kgdt.models.graph import GraphData
from kgdt.models.doc import MultiFieldDocument, MultiFieldDocumentCollection
import random
from typing import List


class PositiveDataGenerator:
    @staticmethod
    def generate_data_from_kg(kg_path=PathUtil.jdk_graph(), dc_path=PathUtil.jdk_dc()):
        graph: GraphData = GraphData.load(kg_path)
        dc: MultiFieldDocumentCollection = MultiFieldDocumentCollection.load(dc_path)
        method_node_ids = graph.get_node_ids_by_label("method")
        class_node_ids = graph.get_node_ids_by_label("class")
        node_ids = []
        # node_ids.extend(method_node_ids)
        node_ids.extend(class_node_ids)
        result = []
        random.shuffle(node_ids)
        for node_id in node_ids:
            node = graph.get_node_info_dict(node_id=node_id)
            doc: MultiFieldDocument = dc.get_by_id(node_id)
            if node is not None and doc is not None:
                if doc.get_doc_text_by_field("sentence_description"):
                    # node_name = ''
                    # for alias in node["properties"]["alias"]:
                    #     if ' ' not in alias:
                    #         node_name = alias
                    #         break
                    sentence = doc.get_doc_text_by_field("sentence_description")[0]
                    sentence = PositiveDataGenerator.clean_html_tag(sentence)
                    # sentence = PositiveDataGenerator.change_first_char_to_lowercase(sentence)
                    # result.append(node_name + "() " + sentence + '\t' + "__label__1\n")
                    if len(sentence.split(" ")) > 3:
                        result.append(sentence + '\t' + "__label__1\n")
                if len(result) >= 1000:
                    break
        PositiveDataGenerator.write_to_txt(result)
        return result

    @staticmethod
    def change_first_char_to_lowercase(sentence):
        first_char = sentence[0:1]
        other_part = sentence[1:]
        return first_char.lower() + other_part

    @staticmethod
    def clean_html_tag(sentence: str):
        sentence = sentence.replace("<noun>", '')
        sentence = sentence.replace("</noun>", '')
        return sentence

    @staticmethod
    def write_to_txt(result: List[str]):
        with open(PathUtil.positive_data_from_kg(), 'w', encoding='utf-8') as f:
            f.writelines(result)


if __name__ == "__main__":
    PositiveDataGenerator.generate_data_from_kg()

