# PatternFactory类用于在变异的时候修改pattern。
from spacy.matcher.phrasematcher import PhraseMatcher
from component.model.pattern import ScopeText
from component.model.sentence import Sentence
from component.model.api_knowledge import APIKnowledge
from component.model.api_knowledge_instance import APIKnowledgeInstance
from component.model.pattern import Pattern
from util.spacy_util import NLPUtil
from util.nlp_cache import NLPCache
from typing import Iterable
from component.matcher.matcher_helper import MatcherHelper
from component.model.api_knowledge_instance import APIKnowledgeInstance


class PatternFactory:
    IGNORE_POS = {"PRON", "NUM"}
    DET_SET = {"a", "an", "the", "this", "that", "these", "those", "such", "many", "some", "any", "one", "all"}

    @staticmethod
    def build_matcher_helper(patterns: Iterable[Pattern]):
        pattern_collection = MatcherHelper()
        pattern_collection.add_patterns(patterns)
        return pattern_collection

    def get_pattern_from_sentence(self, instance: APIKnowledgeInstance) -> Pattern:
        api_knowledge = instance.api_knowledge
        sentence_text = instance.sentence.sentence
        doc = NLPCache.get_doc(sentence_text)
        # NLPUtil.print_info(clean_sentence)

        token_pattern_list = self.doc_2_token_patterns(doc)

        pattern = Pattern(api_knowledge=api_knowledge, token_pattern_list=token_pattern_list, source_sentence=sentence_text)

        matcher = self.get_phrase_matcher_from_api_knowledge(api_knowledge)
        matches = matcher(doc)

        for match_id, start, end in matches:
            string_id = NLPUtil.get_spacy_nlp_vocab().strings[match_id]
            span = doc[start:end]
            scope_text = ScopeText(name=string_id, start=start, end=end, text=span.text, lemma_text=span.lemma_)
            pattern.add_argument_instance(scope_text)

        return pattern

    def doc_2_token_patterns(self, doc):
        """
        将给定的一个经过nlp分析得到的doc变成token的pattern
        :param doc:
        :return:
        """
        token_pattern_list = []
        for token_id, token in enumerate(doc):
            token_pattern = {"LEMMA": token.lemma_}

            if token.is_punct:
                # todo: 原来基础的pattern有些是可以简化的
                token_pattern = {"IS_PUNCT": True, "OP": "?"}
            if token.pos_ in self.IGNORE_POS:
                # todo: 原来基础的pattern有些是可以简化的
                token_pattern = {"POS": token.pos_, "OP": "?"}

            if token.pos_ == "DET" and token.lemma_ in self.DET_SET:
                token_pattern = {"LEMMA": {"IN": list(self.DET_SET)}, "OP": "?"}

            if token.pos_ == "ADP":
                token_pattern = {"POS": "ADP"}
            token_pattern_list.append(token_pattern)
        return token_pattern_list

    def get_phrase_matcher_from_api_knowledge(self, api_knowledge: APIKnowledge):
        matcher = PhraseMatcher(NLPUtil.get_spacy_nlp_vocab(), attr="LEMMA")
        for object_name, object in api_knowledge.get_all_object_items():
            # object = object.lower()
            matcher.add(object_name, [NLPCache.get_doc(object)])
        return matcher