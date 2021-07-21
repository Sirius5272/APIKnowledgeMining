from abc import abstractmethod
from typing import List

from component.model.api_knowledge import APIKnowledge


class APIKnowledgeMutator:
    """
    基类。负责根据给定的一个Task进行变换，得到新的task. 这个是基类，根据需要，可以写不同的子类，使用不同的task变异方法负责生成不同的task实例。
    """

    def get_name(self):
        return self.__class__

    def __hash__(self):
        return hash(self.get_name())

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, TaskMutator):
            return False
        return self.get_name() == other.get_name()

    @abstractmethod
    def mutate(self, api_knowledge: APIKnowledge) -> List[APIKnowledge]:
        """

        :param api_knowledge: 要进行变异的基础api_knowledge
        :return: 返回一系列变异后的api_knowledge
        """
        return []
