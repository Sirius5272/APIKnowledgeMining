from typing import List, Iterable
from component.model.api_knowledge import APIKnowledge
from component.model.api_knowledge_instance import APIKnowledgeInstance
import copy
from util.log_util import LogUtil
from component.model.factory.pattern_factory import PatternFactory
from component.model.factory.pattern_mutator import PatternMutator


class Snowball:
    """
    滚雪球程序的入口类
    """
    def __init__(self):
        self.log = LogUtil.get_log_util()
        self.factory = PatternFactory()
        self.pattern_mutator = PatternMutator()
        pass

    def run_for_one_step(self) -> List[APIKnowledge]:
        """
        第一步：获得种子API Knowledge，并使用这些api knowledge去句子库里匹配，得到api knowledge instance。√
        第二步：从上一步得到的api knowledge instance提取出pattern，并对基础pattern进行变异，得到新的pattern。√
        第三步：使用得到的新的pattern去句子库里匹配，得到匹配的api knowledge instance。
        第四步：使用基于pattern抽取出的instance总结出对应的api knowledge，作为下一轮的起点。√
        :return: 下一轮的api knowledge种子。
        """

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

