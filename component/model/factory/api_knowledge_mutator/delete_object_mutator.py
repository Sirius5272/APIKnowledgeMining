import copy
from typing import List

from component.model.factory.api_knowledge_mutator.api_knowledge_mutator import APIKnowledgeMutator
from component.model.api_knowledge import APIKnowledge


class DeleteObjectAPIKnowledgeMutator(APIKnowledgeMutator):
    """
    删除某个object进行变异
    """

    def __init__(self):
        super().__init__()

    def mutate(self, knowledge: APIKnowledge) -> List[APIKnowledge]:
        """
        这个方法目前只会删除一个不是直接宾语的对象。
        :param knowledge:
        :return:
        """
        result = []
        object_name_list = list(knowledge.get_all_object_names())
        if len(object_name_list) > 2:
            for argument_name in object_name_list:
                new_knowledge = copy.deepcopy(knowledge)
                new_knowledge.delete_object_by_name(argument_name)
                result.append(new_knowledge)
        return result
