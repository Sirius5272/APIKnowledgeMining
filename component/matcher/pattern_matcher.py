import copy
from typing import Iterable, Tuple, List, Dict, Optional
from component.model.sentence import Sentence
from component.model.pattern import Pattern, PatternMatchingResultRecorder
from component.matcher.matcher_helper import MatcherHelper
from component.model.api_knowledge_instance import APIKnowledgeInstance
from util.log_util import LogUtil
from component.model.factory.pattern_factory import PatternFactory
from util.nlp_cache import NLPCache
from util.spacy_util import NLPUtil
from spacy.matcher.matcher import Matcher
from spacy.tokens.span import Span


class PatternMatcher:
    """
    基于pattern对句子进行匹配，抽取出匹配的instance实例
    """
    BEFORE_PATTERN_NAME = "before_variable_pattern"
    AFTER_PATTERN_NAME = "after_variable_pattern"

    def __init__(self):
        self.log = LogUtil.get_log_util()

    def match_patterns(self, sentence_list: Iterable[Sentence], patterns: Iterable[Pattern],
                       matcher_helper: MatcherHelper = None) -> List[Tuple[Pattern, APIKnowledgeInstance]]:
        """
        在一堆SO 帖子集合上用，以下pattern尝试去匹配，并且抽取出对应的TaskInstance。
        :param sentence_list: 句子列表
        :param patterns: 模式列表
        :param matcher_helper: MatcherHelper实例对象，包含了要匹配的pattern的一些信息，可以自己构造并且传入，可以加速。
        没有传入就根据当前的pattern列表进行加速。
        :return: 抽取出来的实例和对应的抽取用的pattern。
        """

        # new_patterns, new_sentence_list = self.filter_sentences_and_patterns(sentence_list=sentence_list,
        #                                                                      patterns=patterns)

        if matcher_helper is None:
            matcher_helper = PatternFactory.build_matcher_helper(patterns)

        #  先收集所有能够匹配的pattern，每个pattern能够匹配的SO post集合
        pattern2sentences = {}
        for sentence in sentence_list:
            matcher_recorder = self.get_match_result(matcher_helper, sentence.sentence)
            if matcher_recorder.size() == 0:
                continue
            for pattern_name in matcher_recorder.get_pattern_names():
                pattern = matcher_helper.get_pattern(name=pattern_name)
                if pattern is None:
                    continue

                if pattern not in pattern2sentences.keys():
                    pattern2sentences[pattern] = []
                pattern2sentences[pattern].append(sentence)

        # 里面，里面的每个元素是(pattern, task_instance), 表示pattern能够抽取出task_instance
        pattern_with_task_instance_relations = []
        for pattern, sentences in pattern2sentences.items():
            task_instance_list = self.extract_task_instance_from_matching_posts(pattern=pattern,
                                                                                sentence_list=sentences)
            for task_instance in task_instance_list:
                pattern_with_task_instance_relations.append((pattern, task_instance))

        return pattern_with_task_instance_relations

    def filter_sentences_and_patterns(self, sentence_list: Iterable[Sentence], patterns: Iterable[Pattern]):
        pattern_fixed_words = set()
        pattern_all_fixed_argument_values = set()
        pattern_fixed_words_list = []
        pattern_all_fixed_argument_values_list = []
        for p in patterns:
            pattern_words = p.get_all_fixed_words()
            pattern_fixed_words.update(pattern_words)

            fixed_argument_values = p.get_all_fixed_argument_values()
            pattern_all_fixed_argument_values.update(fixed_argument_values)

            pattern_fixed_words_list.append(pattern_words)
            pattern_all_fixed_argument_values_list.append(fixed_argument_values)
        new_sentence_list = []
        for sentence in sentence_list:
            text = sentence.sentence
            post_words = set(text.split(" "))
            if len(post_words & pattern_fixed_words) == 0:
                continue

            match_one = False
            for p_index, p in enumerate(patterns):
                pattern_words = pattern_fixed_words_list[p_index]
                tmp = post_words & pattern_words
                if len(post_words & pattern_words) >= len(pattern_words):
                    phrases = pattern_all_fixed_argument_values_list[p_index]

                    contain_phrase_num = 0
                    for phrase in phrases:
                        if phrase in text:
                            contain_phrase_num = contain_phrase_num + 1
                    if contain_phrase_num == len(phrases):
                        match_one = True
                        break

            if match_one is False:
                continue
            new_sentence_list.append(sentence)
        new_patterns = []
        for p_index, pattern in enumerate(patterns):
            match_one = False
            pattern_words = pattern_fixed_words_list[p_index]

            for sentence in sentence_list:
                text = sentence.sentence
                post_words = set(text.split(" "))
                if len(post_words & pattern_fixed_words) == 0:
                    continue

                if len(post_words & pattern_words) >= len(pattern_words):
                    phrases = pattern_all_fixed_argument_values_list[p_index]

                    contain_phrase_num = 0
                    for phrase in phrases:
                        if phrase in text:
                            contain_phrase_num = contain_phrase_num + 1
                    if contain_phrase_num == len(phrases):
                        match_one = True
                        break

            if match_one is False:
                continue
            new_patterns.append(pattern)
        self.log.log_num(hint="original sentence number", number=len(list(sentence_list)))
        self.log.log_num(hint="left sentence number with overlapping words", number=len(new_sentence_list))
        self.log.log_num(hint="original pattern number", number=len(list(patterns)))
        self.log.log_num(hint="left pattern number with overlapping words", number=len(new_patterns))
        return new_patterns, new_sentence_list

    def get_match_result(self, matcher_helper: MatcherHelper, sentence: str) -> PatternMatchingResultRecorder:
        matcher_recorder = PatternMatchingResultRecorder()
        try:
            # clean_sentence = NLPUtil.clean_sentence(sentence=sentence)
            doc = NLPCache.get_doc(sentence)
            matcher = matcher_helper.get_matcher()

            matches = matcher(doc)
            for match_id, start, end in matches:
                # pattern_name = self.nlp.vocab.strings[match_id]  # Get string representation
                pattern_name = NLPUtil.get_spacy_nlp_vocab().strings[match_id]  # Get string representation

                span = doc[start:end]  # The matched span
                matcher_recorder.add_new_matching_result(pattern_name=pattern_name, start=start, end=end,
                                                         text=span.text)
        except Exception:
            self.log.error_matching_sentence_pattern()
        return matcher_recorder

    def extract_task_instance_from_matching_posts(self, pattern: Pattern, sentence_list: Iterable[Sentence]) -> \
            List[APIKnowledgeInstance]:
        """
        从匹配的一些post中抽取出taskInstance实例，如果sentence_id为-1,表示不从id区分据，两个完全相同的句子就是同一个。如果是SO post，
        sentence_id就可以是post_id

        :param pattern: 与句子匹配的模式
        :param sentence_list: 与模式匹配的帖子列表，保证是肯定能匹配上的
        :return: 从匹配的帖子中抽取出啦对应的task实例
        """
        if pattern is None:
            return []

        if not pattern.has_variable():
            self.log.log_patterns_info([pattern], "error: pattern without variable")
            return []

        task_instance_list = self.extract_task_instances_for_variable_pattern(sentence_list=sentence_list,
                                                                              pattern=pattern)
        return task_instance_list

    def extract_task_instances_for_variable_pattern(self, pattern: Pattern,
                                                    sentence_list: Iterable[Sentence],
                                                    ) -> List[APIKnowledgeInstance]:
        instance_list = []

        var2matcher_map = self.generate_all_variable_matchers(pattern=pattern)
        api_knowledge = copy.deepcopy(pattern.get_api_knowledge())
        for sentence in sentence_list:
            var2value_map = self.extract_all_variables_for_posts(pattern=pattern, sentence=sentence,
                                                                 var2matcher_map=var2matcher_map)
            if len(var2value_map.keys()) != pattern.variable_argument_num():
                self.log.info("invalid extract var2value %r : extracted from post=%s p=%s" % (
                    var2value_map, sentence.sentence, pattern))
                continue
            api_knowledge.set_api(sentence.api)
            instance = APIKnowledgeInstance(sentence=sentence, api_knowledge=api_knowledge)
            instance.update_arguments(**var2value_map)
            instance_list.append(instance)

            self.log.info("extracted from sentence=%s" % sentence)
            self.log.log_api_knowledge_info(api_knowledge, hint="the knowledge of the pattern")
            self.log.log_pattern_info(pattern, hint="extracted instance with variable pattern")
            self.log.log_instance_info(instance, hint="extracted task instance with variable pattern")
            self.log.log_api_knowledge_info(instance.get_api_knowledge(),
                                            hint="the task of the extracted task instance")

        return instance_list

    def generate_all_variable_matchers(self, pattern: Pattern) -> Dict[str, Matcher]:
        variable_argument_names = pattern.get_variable_argument_names()
        var2matcher_map = {}
        for variable_argument_name in variable_argument_names:
            variable_argument_matcher = self.generate_variable_matcher(pattern=pattern,
                                                                       variable_name=variable_argument_name)
            var2matcher_map[variable_argument_name] = variable_argument_matcher
        return var2matcher_map

    def generate_variable_matcher(self, pattern: Pattern, variable_name: str) -> Matcher:
        """
        生成一个用来识别一个具体的句子里面变量出现位置的一个特殊的matcher
        :param variable_name:
        :param pattern:
        :return: 一个spacy Matcher 对象
        """
        before_variable_pattern = pattern.get_before_variable_pattern(variable_name=variable_name)
        after_variable_pattern = pattern.get_after_variable_pattern(variable_name=variable_name)
        # matcher = Matcher(self.nlp.vocab)
        matcher = Matcher(NLPUtil.get_spacy_nlp_vocab())

        if len(before_variable_pattern) > 0:
            matcher.add(self.BEFORE_PATTERN_NAME, [before_variable_pattern])
        if len(after_variable_pattern) > 0:
            matcher.add(self.AFTER_PATTERN_NAME, [after_variable_pattern])
        return matcher

    def extract_all_variables_for_posts(self, pattern: Pattern, sentence: Sentence, var2matcher_map=None) -> \
            Optional[Dict[str, str]]:

        if var2matcher_map is None:
            var2matcher_map = self.generate_all_variable_matchers(pattern=pattern)

        variable_name2value_map = {}

        for var_name, matcher in var2matcher_map.items():
            try:
                variable_argument_value = self.get_variable_argument_value(pattern,
                                                                           sentence.sentence,
                                                                           var_name,
                                                                           matcher=matcher)
                self.log.info("final variable value [%s] for sentence (%s) by pattern %s" % (
                    variable_argument_value, sentence.sentence, pattern))
            except Exception:
                self.log.error_get_variable_argument_value()
                continue

            if variable_argument_value is None or len(variable_argument_value) == 0:
                continue
            variable_name2value_map[var_name] = variable_argument_value
        return variable_name2value_map

    def get_variable_argument_value(self, pattern: Pattern, sentence: str, variable_name,
                                    matcher: Matcher = None) -> Optional[str]:
        """
        根据给定的pattern，匹配给定的句子，获取变量的值，假定pattern是具有变量的，并且pattern和句子保证是能匹配上的才会调用
        :param variable_name:
        :param matcher: 一个Matcher对象，用来获取指定句子里面的变量。
        :param pattern:
        :param sentence:
        :return: None，表示发现的匹配的变量不是不是合法的，#
        """

        variable_span = self.extract_original_variable_span_by_pattern(pattern=pattern, sentence=sentence,
                                                                       variable_name=variable_name, matcher=matcher)

        self.log.log_span(variable_span,
                          hint="following is the original span extracted from %s" % sentence)
        return variable_span.lemma_
        # if variable_name == Task.ACTION:
        #     if not self.ARGUMENT.is_valid_action(span=variable_span):
        #         self.log.log_span(hint="invalid action", span=variable_span)
        #         return None
        #     else:
        #         variable_ = variable_span.lemma_
        #         return variable_
        #
        # if not self.ARGUMENT.is_valid_object(span=variable_span):
        #     self.log.log_span(hint="invalid object", span=variable_span)
        #     variable_ = self.ARGUMENT.clean_object(variable_span)
        #     self.log.info("cleaned variable %r" % variable_)
        #     return self.ARGUMENT.get_lemma_for_object(variable_)
        # else:
        #     return self.ARGUMENT.get_lemma_for_object(variable_span)

    def extract_original_variable_span_by_pattern(self, pattern: Pattern, sentence: str,
                                                  variable_name: str,
                                                  matcher: Matcher = None) -> Optional[Span]:
        """
        从句子中，按照给定的pattern，抽取出变量的具体的span，这个span是原始的没有经过清理的。给定的句子确保一定回合pattern是能够匹配的。
        :param variable_name:
        :param pattern: 和句子匹配的pattern。
        :param sentence: 句子
        :param matcher: 一个Matcher对象，用来获取指定句子里面的变量。由给定的pattern构造出来。如果给定就不会重新构造，能够节省时间。
        :return:Span对象或者None
        """
        if not pattern.has_variable():
            return None
        # clean_sentence = NLPUtil.clean_sentence(sentence=sentence)
        doc = NLPCache.get_doc(sentence)

        if matcher is None:
            matcher = self.generate_variable_matcher(pattern, variable_name)
        matches = matcher(doc)

        matcher_recorder = PatternMatchingResultRecorder()
        for match_id, start, end in matches:
            # pattern_name = self.nlp.vocab.strings[match_id]  # Get string representation
            pattern_name = NLPUtil.get_spacy_nlp_vocab().strings[match_id]  # Get string representation

            if start == end:
                continue

            span = doc[start:end]  # The matched span
            matcher_recorder.add_new_matching_result(pattern_name=pattern_name, start=start, end=end,
                                                     text=span.text)

        variable_max_len = pattern.get_variable_max_len(variable_name)
        before_variable_scope_text = matcher_recorder.get_match_result(self.BEFORE_PATTERN_NAME)
        if before_variable_scope_text is None:
            variable_start = 0
        else:
            variable_start = before_variable_scope_text.end

        after_variable_scope_text = matcher_recorder.get_match_result(self.AFTER_PATTERN_NAME)
        if after_variable_scope_text is None:
            variable_end = len(doc)
        else:
            variable_end = after_variable_scope_text.start

        if variable_start >= variable_end:
            return None

        if variable_end - variable_start > variable_max_len:
            # 特殊情况，变量取到的范围比变量的最大长度大。
            if after_variable_scope_text is None:
                variable_end = variable_start + variable_max_len
            if before_variable_scope_text is None:
                variable_start = variable_end - variable_max_len
        if variable_start >= variable_end:
            return None
        variable_span = doc[variable_start:variable_end]
        return variable_span
