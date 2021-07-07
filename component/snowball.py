from typing import List, Iterable, Set
from component.model.api_knowledge import APIKnowledge
from component.model.api_knowledge_instance import APIKnowledgeInstance
from component.model.sentence import Sentence
from component.model.snowball_result import SnowBallResult
import copy
from util.log_util import LogUtil
from component.model.factory.pattern_factory import PatternFactory
from component.model.factory.pattern_mutator import PatternMutator
from component.selector.seed_selector import SeedSelector
from component.matcher.sentence_matcher import SentenceMatcher
from component.matcher.pattern_matcher import PatternMatcher


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

    def run(self,
            seed_api_knowledge_list: List[APIKnowledge],
            sentence_list: List[Sentence],
            max_step,
            save_by_step,
            seed_selector_path=None,
            previous_snowball_result=None,
            ):
        """
        完整的调用入口，
        :param seed_api_knowledge_list:种子列表
        :param sentence_list:句子库
        :param max_step:最大迭代轮次
        :param save_by_step:每隔多少步保存一次
        :param seed_selector_path:用来记录哪些种子和instance已被抽取过的工具类
        :param previous_snowball_result:之前的抽取结果缓存，如果给定可以接着上次的结果抽取
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

        pass

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

        new_snowball_result = SnowBallResult()
        api_knowledge_based_instance_list = self.sentence_matcher.extract_api_knowledge_instances(
            sentence_list=sentence_list, api_knowledge_list=current_api_knowledge_seed_set
        )
        new_snowball_result.add_instances(api_knowledge_based_instance_list)
        previous_snowball_result.add_instances(api_knowledge_based_instance_list)
        # 这里存疑。parent api knowledge要看看是什么意思
        previous_snowball_result.add_api_knowledge_list(current_api_knowledge_seed_set)
        sentence_list = self.filter_used_sentence(sentence_list=sentence_list,
                                                  instance_list=previous_snowball_result.get_instance_collection())
        self.log.log_sentence_list_numbers(sentence_list)

        seed_instance_for_extract_pattern = self.seed_selector.select_new_seed_instance_list(
            instance_collection=previous_snowball_result.get_instance_collection()
        )
        # todo:这里log_util都没有写复数的instance、api_knowledge的log，因为没有得分，要添加上。
        # self.log.log_instance_info()
        new_patterns = self.extract_pattern_from_instances(seed_instance_for_extract_pattern)

        # todo: 把这个函数封装成本类函数，并且看一下那个helper怎么搞。
        patterns_with_instance_relation = self.pattern_matcher.match_patterns(
            patterns=new_patterns, sentence_list=sentence_list
        )
        new_snowball_result.add_pattern_with_instance_relations(patterns_with_instance_relation)
        previous_snowball_result.add_pattern_with_instance_relations(patterns_with_instance_relation)

        new_api_knowledge_list = self.extract_api_knowledge_from_instances(patterns_with_instance_relation)
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
        used_sentence_set = set([instance.sentence.sentence for instance in instance_list])
        for sentence in sentence_list:
            if sentence.sentence in used_sentence_set:
                continue
            new_sentence_list.append(sentence)
        return new_sentence_list

