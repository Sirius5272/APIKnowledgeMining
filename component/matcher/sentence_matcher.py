# 给定一个API Knowledge，找出有没有包含这个知识中所有成分的句子。找到之后组合成APIKnowledgeInstance，返回。
from typing import Iterable, List, Dict, Set
from component.model.sentence import Sentence
from component.model.api_knowledge import APIKnowledge
from component.model.api_knowledge_instance import APIKnowledgeInstance


class SentenceMatcher:
    # 添加一个缓存机制？

    def extract_api_knowledge_instances(self,
                                        sentence_list: List[Sentence],
                                        api_knowledge_list: Iterable[APIKnowledge]) -> List[APIKnowledgeInstance]:
        argument_to_api_knowledge_map = {}

        api_knowledge_list = list(api_knowledge_list)

        for api_knowledge_index, api_knowledge in enumerate(api_knowledge_list):
            argument_list = api_knowledge.get_all_argument_values()
            for argument in argument_list:
                if argument not in argument_to_api_knowledge_map.keys():
                    argument_to_api_knowledge_map[argument] = [api_knowledge_index]
                else:
                    argument_to_api_knowledge_map[argument].append(api_knowledge_index)
        sentence_to_phrases_map = self.match_sentence_by_phrases(sentence_list, argument_to_api_knowledge_map.keys())

        api_knowledge_sentence_matched_relation = []

        for sentence, phrase_list in sentence_to_phrases_map.items():
            tmp_api_knowledge_list = set()
            for argument in phrase_list:
                tmp_api_knowledge_list.update(argument_to_api_knowledge_map[argument])

            for index in tmp_api_knowledge_list:
                api_knowledge = api_knowledge_list[index]
                if set(api_knowledge.get_all_argument_values()) <= set(phrase_list):
                    api_knowledge_sentence_matched_relation.append((api_knowledge, sentence))

        result = []
        for api_knowledge, sentence in api_knowledge_sentence_matched_relation:
            instance = APIKnowledgeInstance(sentence=sentence, api_knowledge=api_knowledge)
            result.append(instance)
        return result

    @staticmethod
    def match_sentence_by_phrases(
                                  sentence_list: List[Sentence],
                                  phrases_list: Iterable[str]) -> Dict[Sentence, Set[str]]:
        # 先直接用String contains匹配，后面看要不要换成PhrasesMatcher
        # 先不考虑时间复杂度，后面看能不能用缓存优化速度
        result = {}
        for phrase in phrases_list:
            for sentence in sentence_list:
                if phrase in sentence.sentence:
                    if sentence not in result.keys():
                        result[sentence] = {phrase}
                    else:
                        result[sentence].add(phrase)
        return result
