import itertools
from typing import List

from component.model.pattern import Pattern
from component.model.api_knowledge import APIKnowledge


class PatternMutator:
    """
    最简单的生成模式的方法，根据原来的模式，将原来的模式的一些实体替换成可以匹配任意实体的占位符。
    """
    def get_name(self):
        return self.__class__

    def mutate(self, pattern: Pattern) -> List[Pattern]:
        result = []
        if pattern.has_variable():
            # 目前的实现一个句子只能有一个可以改变的变量
            return result
        # todo： 目前只有n-1 个argument会变成变量，之后结合数据考虑一下是否n个argument都可以变成变量呢
        for num in range(1, pattern.argument_num()+1):
            new_patterns = self.mutate_with_multiple_holder(pattern=pattern, variable_num=num)
            result.extend(new_patterns)
        return result

    def mutate_pattern_with_variable(self, argument_name, pattern):
        new_pattern = pattern.replace_argument_with_variable(argument_name)
        return new_pattern

    def mutate_with_multiple_holder(self, pattern: Pattern, variable_num):
        argument_names = pattern.get_all_object_names()
        cc = list(itertools.combinations(argument_names, variable_num))  # 组合
        result = []
        for variable_names in cc:
            new_pattern = pattern
            for var_name in variable_names:
                new_pattern=self.mutate_pattern_with_variable(var_name, pattern=new_pattern)
            result.append(new_pattern)
        return result
