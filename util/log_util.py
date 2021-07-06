import logging
from typing import List, Iterable, Tuple, Set

from spacy.matcher.matcher import Matcher
from spacy.tokens.span import Span

from component.model.factory.pattern_mutator import PatternMutator

from component.model.pattern import PatternMatchingResultRecorder, Pattern
from component.model.sentence import Sentence
# from taskkg.model.snowball_result import TaskSnowBallResult
from component.model.api_knowledge import APIKnowledge
from component.model.api_knowledge_instance import APIKnowledgeInstance
from util.path_util import PathUtil


class LogUtil:
    __log_util = None  # 单例模式标记
    __log_type = logging.INFO  # log类型
    __if_console = True  # 是否控制台打印

    @classmethod
    def set_log_util(cls, if_console=__if_console, log_type=__log_type,
                     log_file=PathUtil.log_file_named_with_current_time()):
        cls.__log_util: LogUtil = LogUtil(if_console=if_console, log_type=log_type, log_file=log_file)

    @classmethod
    def get_log_util(cls, ):
        if cls.__log_util is None:
            cls.__log_util: LogUtil = LogUtil()
        return cls.__log_util

    def __init__(self, if_console=__if_console, log_type=__log_type,
                 log_file=PathUtil.log_file_named_with_current_time()):
        self.logger = logging.getLogger(log_file)
        self.logger.setLevel(logging.INFO)
        fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')

        # 控制台输出
        if if_console:
            sh = logging.StreamHandler()
            sh.setFormatter(fmt)
            sh.setLevel(log_type)
            self.logger.addHandler(sh)

        # 读入日志文件
        fh = logging.FileHandler(log_file, encoding='utf-8')
        fh.setFormatter(fmt)
        fh.setLevel(log_type)
        self.logger.addHandler(fh)

    def debug(self, *messages):
        for message in messages:
            self.logger.debug(message)

    def info(self, *messages):
        for message in messages:
            self.logger.info(message)

    def war(self, *messages):
        for message in messages:
            self.logger.warning(message)

    def error(self, *messages):
        for message in messages:
            self.logger.error(message, exc_info=True)

    def log_seed_task_list(self, step: int, seed_api_knowledge: Iterable[APIKnowledge]):
        self.info("extract for step %d" % step)
        self.info("current seed tasks: \n %s" % "\n".join([str(t) for t in seed_api_knowledge]))

    def log_task_instance(self, instance: APIKnowledgeInstance, hint="filter taskInstance"):
        self.info(hint)
        self.info(instance)

    def log_filter_task_instance(self, instance: APIKnowledgeInstance):
        self.info("filter instance %r" % instance)

    # def log_extracted_task(self, task_based_task_instance_list: List[TaskInstance]):
    #     self.info("extracted task_based_task_instance_list\n%s" % "\n".join(
    #         [str(instance) for instance in task_based_task_instance_list]))
    #     self.info(task_based_task_instance_list)

    # def log_pattern_after_update(self, pattern_collection: TaskSnowBallResult):
    #     self.info("pattern after update conf")
    #     self.info(pattern_collection.pattern_collection)

    def log_mutate_patterns(self, mutator: PatternMutator, mutate_patterns: Set[Pattern]):
        self.info("mutate by %s number=%d" % (mutator.get_name(), len(mutate_patterns)))
        for p in mutate_patterns:
            self.info(p)

    def log_num(self, hint, number):
        self.info(f"{hint}={number}")

    def log_add_and_all_pattern_number(self, old_pattern_number, new_patterns):
        self.info(
            "add %d pattern and all pattern number=%d " % (len(new_patterns) - old_pattern_number, len(new_patterns)))

    def log_pattern_info(self, pattern: Pattern, hint="summary basic constant pattern"):
        self.info(hint)
        self.info(pattern)

    def log_patterns_info(self, patterns: Iterable[Pattern], hint="all mutated patterns"):
        self.info(hint)
        self.info("number=%d" % len(list(patterns)))
        info = "\n".join([str(p.confidence) + ":" + str(p) for p in patterns])
        self.info(info)

    # def log_api_knowledge_info(self, api_knowledge: Iterable[APIKnowledge], hint="extracted api knowledge"):
    #     self.info(hint)
    #     self.info("number=%d" % len(list(api_knowledge)))
    #     info = "\n".join([str(p.confidence) + ":" + str(p) for p in api_knowledge])
    #     self.info(info)
    #
    # def log_task_instances_info(self, task_instances: Iterable[TaskInstance], hint="extracted task instances"):
    #     self.info(hint)
    #     self.info("number=%d" % len(list(task_instances)))
    #     info = "\n".join([str(p.confidence) + ":" + str(p) for p in task_instances])
    #     self.info(info)

    def log_instance_info(self, instance: APIKnowledgeInstance, hint="extracted instances"):
        self.info(hint)
        self.info(instance)

    def log_original_and_clean_sentence(self, original_sentence: str, clean_sentence: str):
        self.info("original sentence =%r" % original_sentence)
        self.info("clean sentence =%r" % clean_sentence)

    def log_score_detail_tuple(self, hint="pattern score detail", **score_name2_values_map):
        self.info(hint)
        score_name_list = []
        values_list = []
        for score_name, values in score_name2_values_map.items():
            score_name_list.append(score_name)
            values_list.append(values)

        for info_tuple in zip(*values_list):
            line_info = ",".join(
                ["%r=%r" % (score_name, value) for score_name, value in zip(score_name_list, info_tuple)])
            self.info(line_info)

    def log_matching_instance_number(self, matches: Matcher):
        self.info("%" * 50)
        self.info("matching instance number=%d" % len(matches))

    def log_pattern_matching_result_recorder(self, matcher_recorder: PatternMatchingResultRecorder):
        self.info("%" * 50)
        self.info(matcher_recorder)

    # def log_final_snowball_result_info(self, final_snowball_result: TaskSnowBallResult):
    #     self.info("-" * 50)
    #     self.info(final_snowball_result)

    def log_api_knowledge_info(self, api_knowledge: APIKnowledge, hint="try to find sentence containing knowledge"):
        self.info(hint)
        self.info(api_knowledge)

    def log_task_matched_sentence_list(self, matched_sentence_list: List[str]):
        for s in matched_sentence_list:
            self.info("Matching! %r" % s)

    # def log_snowball_result_info(self,
    #                              snowball_result: TaskSnowBallResult,
    #                              onlysize=False,
    #                              hint="TaskSnowballResult"):
    #     self.info(hint)
    #     if onlysize is False:
    #         self.info(snowball_result)
    #     else:
    #         self.info(snowball_result.simple_repr())

    def error_matching_sentence_pattern(self):
        self.error("Error while matching on sentence with pattern")

    def error_get_variable_argument_value(self):
        self.error("Error while getting variable argument value from pattern and matcher")

    def error_clean_object(self):
        self.error("Error while cleaning object", )

    def log_post_list_numbers(self, sentence_list: List[Sentence]):
        self.info("start with on %r sentences" % (len(sentence_list)))

    # def log_load_snowball_result_info(self, snowball_result: TaskSnowBallResult):
    #     self.info("load %d tasks" % snowball_result.task_collection.size())
    #     self.info("load %d patterns" % snowball_result.pattern_collection.size())
    #     self.info("load %d taskInstances" % snowball_result.task_instance_collection.size())

    def log_subclass_map_info(self, subclass_map: map):
        self.info("following is the object concept tree")
        for concept, subclass_set in subclass_map.items():
            self.info(concept, ":", subclass_set)

    def log_supper_class_map_info(self, supper_class_map: map):
        self.info("following is the object concept tree")
        for concept, supper_class_set in supper_class_map.items():
            self.info(concept, ":", supper_class_set)

    def log_pattern_with_instance_relations(self,
                                            pattern_with_task_instance_relations:
                                            List[Tuple[Pattern, APIKnowledgeInstance]]):
        self.info("extract valid %d following task instances with patterns" % len(pattern_with_task_instance_relations))
        for item in pattern_with_task_instance_relations:
            self.info(item)

    def log_refinement_query(self, refinement_query):
        self.info("the refinement query should be:")
        self.info(refinement_query)

    def log_span(self, span: Span, hint: str = None):
        if hint:
            self.info(hint)
        if span is None:
            self.info("span=None")
            return
        pos_list = []
        tag_list = []

        for token in span:
            pos_list.append(token.pos_)
            tag_list.append(token.tag_)
        tag_str = " ".join(tag_list)
        pos_str = " ".join(pos_list)

        self.info("span=%r lemma=%r tag=%r pos=%r" % (span.text, span.lemma_, tag_str, pos_str))
