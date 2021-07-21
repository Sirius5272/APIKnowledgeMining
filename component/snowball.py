from pathlib import Path
from typing import List, Iterable, Set, Tuple
from component.model.api_knowledge import APIKnowledge
from component.model.api_knowledge_instance import APIKnowledgeInstance
from component.model.pattern import Pattern
from component.model.sentence import Sentence
from component.model.snowball_result import SnowBallResult
import copy
from util.log_util import LogUtil
from component.model.factory.pattern_factory import PatternFactory
from component.model.factory.pattern_mutator import PatternMutator
from component.selector.seed_selector import SeedSelector
from component.matcher.sentence_matcher import SentenceMatcher
from component.matcher.pattern_matcher import PatternMatcher
from util.nlp_cache import NLPCache
from component.filter.filter import Filter
from component.model.factory.api_knowledge_mutator.mutate_manager import APIKnowledgeMutateManager


class Snowball:
    """
    滚雪球程序的入口类
    """
    def __init__(self):
        self.log = LogUtil.get_log_util()
        self.factory = PatternFactory()
        self.pattern_mutator = PatternMutator()
        self.seed_selector = SeedSelector()
        self.sentence_matcher = SentenceMatcher()
        self.pattern_matcher = PatternMatcher()
        self.filter = Filter()
        self.mutate_manager = APIKnowledgeMutateManager()

    def run(self,
            seed_api_knowledge_list: List[APIKnowledge],
            sentence_list: List[Sentence],
            max_step,
            save_by_step,
            seed_selector_path=None,
            previous_snowball_result_path=None,
            output_path=None
            ):
        """
        完整的调用入口，
        :param output_path: 保存sbr的路径
        :param seed_api_knowledge_list:种子列表
        :param sentence_list:句子库
        :param max_step:最大迭代轮次
        :param save_by_step:每隔多少步保存一次
        :param seed_selector_path:用来记录哪些种子和instance已被抽取过的工具类
        :param previous_snowball_result_path:之前的抽取结果缓存，如果给定可以接着上次的结果抽取
        :return:
        """
        # 构造seed_selector。这应该是一个类变量
        # 构造返回的SBR，如果previous SBR存在就load，不存在就new一个
        # 把初始种子加入seed_selector的已使用种子和结果SBR中
        # 把sentence的句子清理一下
        # 过滤sentence（这一步目前没有）
        # 循环 for 1， max_step+1,如果当前是第一轮，seed是传入的seed list，如果不是第一轮，置为none，因为会从上一轮的SBR中得到种子。
        # 如果达到了保存步数则保存SBR和seed selector
        # 结束循环，保存SBR和seed selector。保存NLP cache
        # 返回SBR
        if seed_selector_path is None or Path(seed_selector_path).exists() is False:
            self.seed_selector = SeedSelector()
        else:
            self.seed_selector: SeedSelector = SeedSelector.load(seed_selector_path)

        if previous_snowball_result_path is None or Path(previous_snowball_result_path).exists() is False:
            final_snowball_result = SnowBallResult()
        else:
            final_snowball_result: SnowBallResult = SnowBallResult.load(previous_snowball_result_path)

        self.log.log_api_knowledge_list_info(self.seed_selector.selected_api_knowledge_collection,
                                             hint="used seed api knowledge list")
        self.log.log_instances_list_info(self.seed_selector.selected_api_knowledge_instance_collection,
                                         hint="used instance list")
        final_snowball_result.add_api_knowledge_list(seed_api_knowledge_list)
        self.seed_selector.add_used_api_knowledge(seed_api_knowledge_list)
        # 加上一步清理sentence的过程，主要是清理掉一些不合法的api，被识别成API的doc网址。
        sentence_list = self.filter.filter_sentence_by_api(sentence_list)
        self.log.log_num("original sentence number", len(sentence_list))
        for step in range(1, max_step + 1):
            if step == 1:
                current_api_knowledge_seed_set = set(seed_api_knowledge_list)
                # 加了一步筛选
                current_api_knowledge_seed_set = self.filter.filter_api_knowledge_by_invalid_object(
                    current_api_knowledge_seed_set)
            else:
                current_api_knowledge_seed_set = None
            new_snowball_result = self.run_for_one_step(sentence_list=sentence_list,
                                                        previous_snowball_result=final_snowball_result,
                                                        current_api_knowledge_seed_set=current_api_knowledge_seed_set)

            self.log.log_snowball_result_info(new_snowball_result,
                                              hint="run_for_one_step snowball result step=%d" % step)
            if save_by_step != -1 and step % save_by_step == 0:
                if output_path is not None:
                    final_snowball_result.save(output_path)
                if seed_selector_path is not None:
                    self.seed_selector.save(seed_selector_path)

        if output_path is not None:
            final_snowball_result.save(output_path)
        if seed_selector_path is not None:
            self.seed_selector.save(seed_selector_path)
        NLPCache.save_doc()

        # self.log.log_snowball_result_info(final_snowball_result, hint="final snowball result")
        return final_snowball_result

    def run_for_one_step(self,
                         sentence_list: List[Sentence],
                         previous_snowball_result: SnowBallResult,
                         current_api_knowledge_seed_set: Set[APIKnowledge] = None,
                         ) -> SnowBallResult:
        """
        第一步：获得种子API Knowledge，并使用这些api knowledge去句子库里匹配，得到api knowledge instance。√
        第二步：从上一步得到的api knowledge instance提取出pattern，并对基础pattern进行变异，得到新的pattern。√
        第三步：使用得到的新的pattern去句子库里匹配，得到匹配的api knowledge instance。
        第四步：使用基于pattern抽取出的instance总结出对应的api knowledge，作为下一轮的起点。√
        :param sentence_list:
        :param previous_snowball_result:
        :param current_api_knowledge_seed_set:
        :return: 下一轮迭代输入的sbr
        """
        # 首先对抽取的sentence过滤一下，一个Sentence如果在之前被提取过知识，我们就不再使用它了。
        # ——过滤Sentence——
        # 然后从上一轮输出的SBR中拿出本次迭代的种子api knowledge，也过滤一下。被使用过的种子就不用了。
        # ——过滤种子——。这里使用seed_selector类。
        # new一个SBR，作为输出的结果
        # 第一步，使用种子api knowledge去匹配句子，输入的参数是上述被过滤过的sentence_list和seed api knowledge，得到instance_list。
        # 把这些instance先放入结果SBR中。
        # 把instance和它们对应的task的parent task放入previous SBR中（parent task 是什么？）
        # 把抽取出来的instance也筛选一下。同样使用seed_selector类。这里有置信度。
        # 根据筛选出来的instance，总结出pattern并且变异出新的pattern
        # 再用变异出的新patterns去sentence_list里匹配
        # 匹配出来得到的instance_pattern relation加入结果SBR和previous SBR中
        # 根据instance_pattern relation抽取出对应的api knowledge，加入结果SBR和previous SBR中
        # 还有parent api knowledge加入previous SBR
        # 返回结果SBR
        sentence_list = self.filter_used_sentence(sentence_list=sentence_list,
                                                  instance_list=previous_snowball_result.get_instance_collection())
        self.log.log_sentence_list_numbers(sentence_list)
        if current_api_knowledge_seed_set is None:
            current_api_knowledge_seed_set = self.seed_selector.select_new_seed_api_knowledge_list(
                previous_snowball_result.get_api_knowledge_collection()
            )
        # 对种子的筛选放在每一轮的尾部。

        # 步骤0， 对seed api knowledge进行变异
        after_mutated_knowledge = self.mutate_api_knowledge(current_api_knowledge_seed_set)
        new_snowball_result = SnowBallResult()
        # 步骤1， 根据api knowledge从句子库中抽取出api knowledge instance
        api_knowledge_based_instance_list = self.sentence_matcher.extract_api_knowledge_instances(
            sentence_list=sentence_list, api_knowledge_list=after_mutated_knowledge
        )
        # instance在这里先筛选 再加入new sbr
        api_knowledge_based_instance_list = self.filter.filter_instance_by_invalid_object(
            api_knowledge_based_instance_list)

        new_snowball_result.add_instances(api_knowledge_based_instance_list)
        previous_snowball_result.add_instances(api_knowledge_based_instance_list)
        # 这里存疑。parent api knowledge要看看是什么意思
        previous_snowball_result.add_api_knowledge_list(current_api_knowledge_seed_set)
        # 对抽取的句子库过滤。我们认为一个句子被抽取过之后就没有利用价值，下一轮不会再被抽取了。
        sentence_list = self.filter_used_sentence(sentence_list=sentence_list,
                                                  instance_list=previous_snowball_result.get_instance_collection())
        self.log.log_sentence_list_numbers(sentence_list)
        # 挑选出新的seed instance
        seed_instance_for_extract_pattern = self.seed_selector.select_new_seed_instance_list(
            instance_collection=previous_snowball_result.get_instance_collection()
        )

        self.log.log_instances_list_info(seed_instance_for_extract_pattern,
                                         hint="seed instance list for summary pattern")
        # 步骤2， 根据instance，总结出pattern并且变异出新的pattern。
        new_patterns = self.extract_pattern_from_instances(seed_instance_for_extract_pattern)
        # 过滤一次这些变异出来的pattern
        new_patterns = self.filter.filter_patterns_by_invalid_object(new_patterns)

        # 步骤3， 根据变异出来的patterns，从句子库中抽取出匹配的实例instance
        patterns_with_instance_relation = self.extract_instance_based_patterns(pattern_list=new_patterns,
                                                                               sentence_list=sentence_list)
        # 过筛！
        patterns_with_instance_relation = self.filter.filter_relation_between_pattern_and_instance(
            patterns_with_instance_relation)

        new_snowball_result.add_pattern_with_instance_relations(patterns_with_instance_relation)
        previous_snowball_result.add_pattern_with_instance_relations(patterns_with_instance_relation)

        # 步骤4， 根据基于pattern抽取出来的instance，总结出对应的api knowledge
        new_api_knowledge_list = self.extract_api_knowledge_from_instances(patterns_with_instance_relation)
        # 过筛
        new_api_knowledge_list = self.filter.filter_api_knowledge_by_invalid_object(new_api_knowledge_list)
        new_snowball_result.add_api_knowledge_list(new_api_knowledge_list)
        previous_snowball_result.add_api_knowledge_list(new_api_knowledge_list)
        # 一步加入parent api knowledge
        return new_snowball_result

    def extract_api_knowledge_from_instances(self, pattern_with_instance_relations):
        all_knowledge = set([])
        for pattern, instance in pattern_with_instance_relations:
            temp_api_knowledge = instance.get_api_knowledge()
            all_knowledge.add(copy.deepcopy(temp_api_knowledge))

        # todo: 这里可能需要加一道筛选
        self.log.log_num(number=len(all_knowledge), hint="summary knowledge from extracted instances")
        all_knowledge = self.filter.filter_api_knowledge_by_invalid_object(all_knowledge)
        for knowledge in all_knowledge:
            self.log.log_api_knowledge_info(api_knowledge=knowledge,
                                            hint="valid summary knowledge from extracted instances")
        # self.log.log_tasks_info(tasks=filter_tasks, hint="invalid summary tasks from extracted task instances")
        return all_knowledge

    def extract_pattern_from_instances(self, instance_list: Iterable[APIKnowledgeInstance]):
        """
        从instance中生成新的pattern。注意是新的pattern，也就是instance对应的pattern是不在这个返回值里的
        :param instance_list:
        :return:
        """
        new_patterns = set([])
        for instance in instance_list:
            self.log.info(instance)
            pattern = self.factory.get_pattern_from_sentence(instance=instance)
            self.log.log_pattern_info(pattern)
            mutated_patterns = self.pattern_mutator.mutate(pattern)
            new_patterns.update(mutated_patterns)
        return new_patterns

    def filter_used_sentence(self,
                             sentence_list: List[Sentence],
                             instance_list: Iterable[APIKnowledgeInstance]) -> List[Sentence]:
        """
        把用过的sentence给筛选掉
        :param sentence_list:
        :param instance_list:
        :return:
        """
        new_sentence_list = []
        used_sentence_set = set([instance.sentence.api + '\t' + instance.sentence.sentence for instance in instance_list])
        for sentence in sentence_list:
            tmp_sent = sentence.api + '\t' + sentence.sentence
            if tmp_sent in used_sentence_set:
                continue
            new_sentence_list.append(sentence)
        return new_sentence_list

    def extract_instance_based_patterns(self, pattern_list: Iterable[Pattern], sentence_list: List[Sentence]) -> \
            List[Tuple[Pattern, APIKnowledgeInstance]]:
        return self.pattern_matcher.match_patterns(patterns=pattern_list, sentence_list=sentence_list)

    def mutate_api_knowledge(self, current_seed_knowledge_set: Iterable[APIKnowledge]) -> Set[APIKnowledge]:
        self.log.log_api_knowledge_list_info(api_knowledge=current_seed_knowledge_set, hint="original current knowledge")
        mutated_set = self.mutate_manager.mutate_knowledge_list(current_seed_knowledge_set)
        current_seed_knowledge_set = mutated_set | current_seed_knowledge_set
        self.log.log_num(number=len(current_seed_knowledge_set), hint="seed tasks after mutation")
        return set(current_seed_knowledge_set)
