import copy
from typing import TypeVar, Union, Set, Optional

from component.model.api_knowledge import APIKnowledge

T = TypeVar('T', bound='Pattern')
E = TypeVar('E', bound='ScopeText')


class ScopeText:
    """
    描述了句子里面一定范围的文本
    """

    def __init__(self, name, start, end, text, lemma_text):
        self.name = name
        self.start = start
        self.end = end
        self.text = text
        self.lemma_text = lemma_text

    def __repr__(self):
        return "<ScopeText name=%s [%r,%r), text=%r lemma=%r>" % (
            self.name, self.start, self.end, self.text, self.lemma_text)

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, ScopeText):
            return False
        if self.name != other.name or self.start != other.start or self.end != other.end or self.text != other.text:
            return False
        return True

    def contains_other(self, scope_text: E):
        if self.start <= scope_text.start and self.end >= scope_text.end:
            return True
        return False

    def overlap_other(self, scope_text: E):
        if self.contains(scope_text.start) or self.contains(scope_text.end - 1):
            return True
        return False

    def contains(self, index):
        if self.start <= index < self.end:
            return True
        return False

    def __hash__(self):
        return hash(str(self))

    def len(self):
        return self.end - self.start

    def get_range(self):
        return self.start, self.end


class PatternArgumentInfo:
    """
    封装了和Task有关的多个argument的信息和实际的pattern的的关联。
    比如原来pattern的  “how to (action)[read] a (object1)[] in [object2](Java)”
    中的有个名字叫做action的argument，它的值是read，位置是[2,3],
    这个类允许有多个变量的存在。
    """

    def __init__(self):
        self.argument_info_map = {}
        self.variable_argument_names = set()

    def has_variable(self):
        if len(self.variable_argument_names) == 0:
            return False
        return True

    def has_argument(self, argument_name):
        if argument_name in self.argument_info_map.keys():
            return True
        return False

    def delete_argument(self, argument_name):
        if not self.has_argument(argument_name):
            return set()
        tmp = self.argument_info_map[argument_name]
        del self.argument_info_map[argument_name]
        self.variable_argument_names = self.variable_argument_names - {argument_name}
        return tmp

    def get_variable_arguments(self) -> Set[str]:
        """
        获取所有的变量
        :return:
        """
        return self.variable_argument_names

    def add_argument_instance(self, argument_instance: ScopeText):
        if argument_instance.name not in self.argument_info_map.keys():
            self.argument_info_map[argument_instance.name] = set()
        self.argument_info_map[argument_instance.name].add(argument_instance)

    def get_argument_instances(self, argument_name) -> Set[ScopeText]:
        return self.argument_info_map.get(argument_name, set())

    def get_first_argument_instance(self, argument_name) -> Optional[ScopeText]:
        """
        每个变量可能在模式里面有多个提及，这个方法只返回第一个提及的位置，正常情况下调用这个方法就够了
        :param argument_name: 变量的名字
        :return: None，如果找不到对应的变量实例
        """
        scope_text_set = self.get_argument_instances(argument_name=argument_name)
        if len(scope_text_set) == 0:
            return None
        return list(scope_text_set)[0]

    def get_variable_start(self, variable_name):
        if not self.has_variable():
            return -1
        argument_instance = self.get_first_argument_instance(argument_name=variable_name)
        if argument_instance is None:
            return -1
        return argument_instance.start

    def get_variable_max_len(self, variable_name):
        if not self.has_variable():
            return 0
        return self.get_argument_len(argument_name=variable_name)

    # 目前默认参数的最短长度为1
    def get_variable_min_len(self):
        if not self.has_variable():
            return 0
        return 1

    def get_variable_end(self, variable_name):
        if self.hasnot_variable():
            return -1
        argument_instance = self.get_first_argument_instance(argument_name=variable_name)
        if argument_instance is None:
            return -1
        return argument_instance.end

    def hasnot_variable(self):
        has_variable_ = not self.has_variable()
        return has_variable_

    def __repr__(self):
        return "<PatternArgumentInfo variable=%r %r>" % (self.variable_argument_names, str(self.argument_info_map))

    def get_all_argument_names(self):
        return self.argument_info_map.keys()

    def get_all_fixed_argument_names(self):
        names = self.get_all_argument_names()
        if self.has_variable():
            return names - self.get_variable_arguments()
        return names

    def is_variable(self, argument_name):
        if argument_name in self.variable_argument_names:
            return True
        return False

    def make_argument_variable(self, argument_name):
        """
        将一个固定值的参数，泛化成为一个可以匹配任意实体的参数
        :param argument_name:
        :return:
        """
        if not self.has_argument(argument_name):
            return

        self.variable_argument_names.add(argument_name)

    def get_argument_info(self, index, argument_name=None):
        if argument_name is None:
            argument_names = self.get_all_argument_names()
            for n in argument_names:
                instance = self.get_argument_info(index=index, argument_name=n)
                if instance is not None:
                    return instance
            return None

        argument_instances = self.get_argument_instances(argument_name=argument_name)
        for instance in argument_instances:
            if instance.contains(index):
                return instance

        return None

    def contains(self, index, argument_name=None):
        if self.get_argument_info(index=index, argument_name=argument_name) is not None:
            return True
        return False

    def get_all_object_names(self):
        return set(self.get_all_argument_names()) - {APIKnowledge.API}

    def get_argument_len(self, argument_name):
        argument_instance = self.get_first_argument_instance(argument_name=argument_name)
        if argument_instance is None:
            return -1
        return argument_instance.len()

    def get_argument_value(self, argument_name):
        if self.is_variable(argument_name):
            return None

        instances = self.get_argument_instances(argument_name)
        if len(instances) == 0:
            return None

        return list(instances)[0].text

    def get_argument_info_representation(self, argument_name):
        if not self.has_argument(argument_name=argument_name):
            return ""
        argument_value = self.get_argument_value(argument_name=argument_name)
        argument_len = self.get_argument_len(argument_name=argument_name)
        simple_argument_name = argument_name
        if simple_argument_name != APIKnowledge.API:
            simple_argument_name = simple_argument_name[:-1]
        if self.is_variable(argument_name):
            return "(%s)[]<1...%d>" % (simple_argument_name, argument_len)
        return "(%s)[%s]<%d>" % (simple_argument_name, argument_value, argument_len)

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, PatternArgumentInfo):
            return False
        if self.argument_info_map != other.argument_info_map or \
                self.variable_argument_names != other.variable_argument_names:
            return False
        return True

    def __hash__(self):
        return hash(str(self))

    def argument_num(self):
        return len(self.argument_info_map.keys())

    def fixed_argument_num(self):
        return self.argument_num() - self.variable_argument_num()

    def variable_argument_num(self):
        return len(self.variable_argument_names)

    def check_scopes_overlap(self):
        for start_argument_name in self.get_all_argument_names():
            start_scope_text_set = self.get_argument_instances(argument_name=start_argument_name)
            for end_argument_name in self.get_all_argument_names():
                end_scope_text_set = self.get_argument_instances(argument_name=end_argument_name)
                if start_argument_name == end_argument_name:
                    continue
                for s_scope in start_scope_text_set:
                    for e_scope in end_scope_text_set:
                        if s_scope.overlap_other(e_scope):
                            return True
        return False


class Pattern:
    """
    封装了一个用来匹配的模式，例子，如何表示一个模式, 小括号表示这里匹配的实体的名字，中括号表示匹配的对应的名字的实体的实际值。
    其中空的中括号表示这里可以任意实体。特点是当前这个模式支持多个变量。

    对于以下模式：
    “how to (Action)[read] a (object1)[] in [Object2](Java)”
    我们写出来让Spacy去匹配的模式是，注意具体匹配技术是token级别的匹配，用Matcher这个类（from spacy.matcher import Matcher）。
    具体参考网页：https://nightly.spacy.io/usage/rule-based-matching#matcher。

    token_pattern_list = [
        {"LEMMA": "how"},
        {"LEMMA": "to"},
        {"LEMMA": "read"},
        {"LEMMA": "a"},
        {"LEMMA": "file"}
    ]。

    PS: 目前保证pattern里面只会最多有一个地方对应着是一个任意匹配的实体。例如
    token_pattern_list = [
        {"LEMMA": "how"},
        {"LEMMA": "to"},
        {"LEMMA": "read"},
        {},
        {"OP": "?"},
    ]。
           {}表示匹配一个任意token。 {"OP": "?"}表示是匹配0或者1个任意token。连续的n个{"OP": "?"}表示匹配长度为0-n的一个连续的字符串表示的实体，那么
           {},{"OP": "?"}表示匹配长度为1-2的长度的实体。

    """

    DEFAULT_VARIABLE_ENTITY_LEN = 6  # 一个表示可变实体的长度限制， 目前设置为6. todo：测试看看这个长度限制是否合理。

    def __init__(self,
                 api_knowledge: APIKnowledge,
                 token_pattern_list: [],
                 source_sentence: str = None,
                 confidence=0.0):
        """
        构造一个pattern对象。

        token_pattern_list的样例，一个列表：
        token_pattern_list = [
            {"LEMMA": "how"},
            {"LEMMA": "to"},
            {"LEMMA": "read"},
            {"LEMMA": "a"},
            {"LEMMA": "file"}
        ]

        :param api_knowledge:
        :param token_pattern_list:
        :param source_sentence: 总结出当前pattern的原始句子
        """
        self.api_knowledge = copy.deepcopy(api_knowledge)
        self.token_pattern_list = token_pattern_list

        self.source_sentence = source_sentence
        self.pattern_argument_info = PatternArgumentInfo()
        self.pattern_representation = ""

        self.confidence = confidence

    def set_confidence(self, confidence):
        """
        设计pattern的置信度
        :param confidence:
        :return:
        """
        self.confidence = confidence

    def to_dict(self):
        return {
            "pattern_representation": self.pattern_representation,
            "api_knowledge": self.api_knowledge.to_dict(),
            "token_patterns": self.token_pattern_list,

        }

    def is_valid(self):
        if len(self.pattern_argument_info.get_all_argument_names()) == 1:
            return False
        if APIKnowledge.API not in self.pattern_argument_info.get_all_argument_names():
            return False

        overlap = self.pattern_argument_info.check_scopes_overlap()
        if overlap is True:
            return False
        pattern_rep = str(self)
        for argument_name in self.pattern_argument_info.get_all_argument_names():
            if self.is_variable(argument_name=argument_name):
                if "[]" not in pattern_rep:
                    return False
        return True

    def get_name(self):
        return self.get_pattern_representation()

    def print(self, ):
        print(self)

    def print_arguments(self):
        t = [self.pattern_argument_info.get_argument_info_representation(argument_name=name) for name in
             self.get_all_argument_names()]
        print(" ".join(t))

    def get_fixed_string_in_scope(self, start, end):
        """
        只获取指定范围内固定常量的部分，如果是可以变的变量词（占位符），截断
        :param start:
        :param end:
        :return:
        """
        if start < 0:
            start = 0
        if end > self.pattern_len():
            end = self.pattern_len()
        if start > end:
            return ""
        words = []

        while start < end:
            if "LEMMA" in self.token_pattern_list[start]:
                break
            start = start + 1
            continue

        for token in self.token_pattern_list[start:end]:
            if "LEMMA" in token and type(token["LEMMA"]) != dict:
                words.append(token["LEMMA"])
            else:
                # 只获取不是变量部分的string
                break

        return " ".join(words)

    def get_argument_with_left_context(self, argument_name, context_word_num=1):
        if self.is_variable(argument_name):
            return ""
        argument_value = self.get_argument_value(argument_name)
        instance_scope_text_set = self.pattern_argument_info.get_argument_instances(argument_name=argument_name)
        if len(instance_scope_text_set) == 0:
            return argument_value
        argument_instance_scope_text: ScopeText = list(instance_scope_text_set)[0]
        context_start = argument_instance_scope_text.start - context_word_num
        return self.get_fixed_string_in_scope(start=context_start, end=argument_instance_scope_text.end)

    def get_argument_with_right_context(self, argument_name, context_word_num=1):
        if self.is_variable(argument_name):
            return ""
        argument_value = self.get_argument_value(argument_name)
        instance_scope_text_set = self.pattern_argument_info.get_argument_instances(argument_name=argument_name)
        if len(instance_scope_text_set) == 0:
            return argument_value
        argument_instance_scope_text: ScopeText = list(instance_scope_text_set)[0]
        context_end = argument_instance_scope_text.end + context_word_num
        return self.get_fixed_string_in_scope(start=argument_instance_scope_text.start, end=context_end)

    def get_argument_with_context(self, argument_name, context_word_num=1):
        if self.is_variable(argument_name):
            return ""
        argument_value = self.get_argument_value(argument_name)
        instance_scope_text_set = self.pattern_argument_info.get_argument_instances(argument_name=argument_name)
        if len(instance_scope_text_set) == 0:
            return argument_value
        argument_instance_scope_text: ScopeText = list(instance_scope_text_set)[0]
        context_start = argument_instance_scope_text.start - context_word_num
        context_end = argument_instance_scope_text.end + context_word_num
        return self.get_fixed_string_in_scope(start=context_start, end=context_end)

    def get_word_in_pattern(self, index):
        """
         返回一个完整的pattern中某个位置的token的pattern的字符串
        :param index:
        :return:
        """
        token_info = self.get_token_pattern(index=index)
        pos_ = token_info.get("POS", "")
        if pos_ == "ADP":
            return "<adp>"
        if pos_ == "NUM":
            return "<num?>"
        if pos_ == "PRON":
            return "<pron?>"

        if "IS_PUNCT" in token_info.keys():
            return "<punct?>"

        lemma_ = token_info.get("LEMMA", "")
        if type(lemma_) == dict:
            return "<det?>"
        return lemma_

    def get_pattern_representation(self) -> str:
        """
        或者整个pattern的字符串表示，如果两个pattern的字符串表示一样，认为是同一个pattern
        :return:
        """
        if self.pattern_representation != "":
            return self.pattern_representation
        words = []
        current_token_index = 0
        while current_token_index <= len(self.token_pattern_list) - 1:
            argument_instance: ScopeText = self.pattern_argument_info.get_argument_info(index=current_token_index)
            if argument_instance is None:
                words.append(self.get_word_in_pattern(current_token_index))
                current_token_index = current_token_index + 1
                continue
            argument_rep = self.pattern_argument_info.get_argument_info_representation(argument_instance.name)
            words.append(argument_rep)
            current_token_index = current_token_index + argument_instance.len()

        self.pattern_representation = " ".join(words)
        return self.pattern_representation

    def get_token_pattern_list(self):
        return self.token_pattern_list

    def is_variable(self, argument_name):
        return self.pattern_argument_info.is_variable(argument_name=argument_name)

    def has_variable(self):
        """
        检查当前模式是否已经存在一个可变实体
        :return:
        """
        return self.pattern_argument_info.has_variable()

    def has_not_variable(self):
        """
        检查当前模式是否已经存在一个可变实体
        :return:
        """
        return not self.pattern_argument_info.has_variable()

    def has_argument(self, argument_name):
        return self.pattern_argument_info.has_argument(argument_name)

    def replace_pattern_argument(self, replaced_argument_name,
                                 new_argument_token_pattern: [],
                                 new_argument_value,
                                 new_argument_value_lemma=None) -> T:
        """
        将pattern中 对应的参数部分，替换成为一个新的token的pattern。例如，将对应于Action的token_pattern {"LEMMA":"read"} 替换成为{"LEMMA":"write"}.

        :param replaced_argument_name: 要替换的参数的名字，如”action“
        :param new_argument_token_pattern: 用来替换的对应的pattern，是个列表，里面每个是一个词对应的token的pattern
        :param new_argument_value:
        :param new_argument_value_lemma:
        :return: 返回一个新的pattern
        """

        new_pattern_token_list = []

        current_token_index = 0
        new_token_pattern_current_index = 0

        if new_argument_value_lemma is None:
            new_argument_value_lemma = new_argument_value

        new_pattern_argument_info = PatternArgumentInfo()

        new_argument_token_pattern_len = len(new_argument_token_pattern)

        while current_token_index <= len(self.token_pattern_list) - 1:
            argument_instance: ScopeText = self.pattern_argument_info.get_argument_info(index=current_token_index)
            if argument_instance is None:
                new_pattern_token_list.append(self.token_pattern_list[current_token_index])
                current_token_index = current_token_index + 1
                new_token_pattern_current_index = new_token_pattern_current_index + 1
                continue

            if argument_instance.name == replaced_argument_name:
                new_pattern_token_list.extend(new_argument_token_pattern)
                new_argument_scope_text = ScopeText(name=argument_instance.name, start=new_token_pattern_current_index,
                                                    end=new_token_pattern_current_index + new_argument_token_pattern_len,
                                                    text=new_argument_value,
                                                    lemma_text=new_argument_value_lemma)
                new_pattern_argument_info.add_argument_instance(new_argument_scope_text)

                current_token_index = current_token_index + argument_instance.len()
                new_token_pattern_current_index = new_token_pattern_current_index + new_argument_token_pattern_len
                continue

            new_pattern_token_list.extend(self.token_pattern_list[argument_instance.start:argument_instance.end])
            new_pattern_argument_info.add_argument_instance(
                ScopeText(name=argument_instance.name, start=new_token_pattern_current_index,
                          end=new_token_pattern_current_index + argument_instance.len(), text=argument_instance.text,
                          lemma_text=argument_instance.lemma_text))

            current_token_index = current_token_index + argument_instance.len()
            new_token_pattern_current_index = new_token_pattern_current_index + argument_instance.len()

        new_task = copy.deepcopy(self.api_knowledge)
        new_task.update_argument(name=replaced_argument_name, value=new_argument_value)

        new_pattern = Pattern(api_knowledge=new_task, token_pattern_list=new_pattern_token_list,
                              source_sentence=self.source_sentence)

        # 将原来的pattern中是变量的的argument名字进行继承，以支持多变量
        for var_name in self.pattern_argument_info.get_variable_arguments():
            new_pattern_argument_info.make_argument_variable(argument_name=var_name)
        # new_pattern_argument_info.make_argument_variable(argument_name=argument_name)
        new_pattern.set_pattern_argument_info(new_pattern_argument_info)
        return new_pattern

    def replace_argument_with_variable(self, argument_name, max_len=DEFAULT_VARIABLE_ENTITY_LEN) -> Union[T, None]:

        # todo: action 的变量添加对应的模式特殊一点
        if not self.has_argument(argument_name):
            return None
        replace_variable_token = [{}] + [{"OP": "?"}] * (max_len - 1)
        new_pattern = self.replace_pattern_argument(
            replaced_argument_name=argument_name, new_argument_token_pattern=replace_variable_token,
            new_argument_value="", new_argument_value_lemma=""
        )
        new_pattern.pattern_argument_info.make_argument_variable(argument_name=argument_name)
        return new_pattern

    def replace_action_with_variable(self, ):
        """
        将action对应的位置替换成为变量，约定可以支持动词+介词作为action，所有action对应的变量的长度是1-2.
        :return:
        """
        argument_name = APIKnowledge.API
        if not self.has_argument(argument_name):
            return None
        replace_variable_token = [{'POS': 'VERB'},
                                  {'OP': '?', 'POS': 'ADP'}]

        new_pattern = self.replace_pattern_argument(
            replaced_argument_name=argument_name, new_argument_token_pattern=replace_variable_token,
            new_argument_value="", new_argument_value_lemma=""
        )
        new_pattern.pattern_argument_info.make_argument_variable(argument_name=argument_name)
        return new_pattern

    def get_before_variable_pattern(self, variable_name):
        if not self.has_variable():
            return None

        variable_start = self.pattern_argument_info.get_variable_start(variable_name)
        return self.token_pattern_list[:variable_start]

    def get_after_variable_pattern(self, variable_name):
        if not self.has_variable():
            return None

        variable_end = self.pattern_argument_info.get_variable_end(variable_name)
        return self.token_pattern_list[variable_end:]

    def get_variable_argument_names(self):
        """
        获得所有变量的名字
        :return:
        """
        return self.pattern_argument_info.get_variable_arguments()

    @staticmethod
    def from_dict():
        # todo : 完善这个方法
        return None

    def pattern_len(self):
        return len(self.token_pattern_list)

    def get_token_pattern(self, index) -> dict:
        """
        根据给定的下标获取对应的token的pattern描述dict
        :param index:  下标
        :return: e.g.,{"LOWER": "hello"}。 如果下标非法，返回None
        """
        if index < 0 or index >= self.pattern_len():
            return {}
        return self.token_pattern_list[index]

    def __repr__(self):
        return "<Pattern %s" % (self.get_pattern_representation())

    def add_argument_instance(self, scope_text: ScopeText):
        self.pattern_argument_info.add_argument_instance(scope_text)

    def get_all_argument_names(self):
        return self.pattern_argument_info.get_all_argument_names()

    def get_all_object_names(self):
        return self.pattern_argument_info.get_all_object_names()

    def get_all_fixed_argument_names(self):
        names = self.pattern_argument_info.get_all_fixed_argument_names()
        return names

    def get_all_fixed_argument_values(self):
        names = self.pattern_argument_info.get_all_fixed_argument_names()
        values = set()
        for name in names:
            v = self.get_argument_value(name)
            values.add(v)
        return values

    def set_pattern_argument_info(self, new_pattern_argument_info: PatternArgumentInfo):
        self.pattern_argument_info = new_pattern_argument_info

    def get_argument_value(self, name):
        return self.pattern_argument_info.get_argument_value(name)

    def __eq__(self, other):
        # todo: 这个两个模式如何算一样需要考虑一下
        if other is None:
            return False
        if not isinstance(other, Pattern):
            return False
        if self.get_pattern_representation() != other.get_pattern_representation():
            return False
        return True

    def __hash__(self):
        return hash(str(self))

    def get_api_knowledge(self):
        return self.api_knowledge

    def argument_num(self):
        return self.pattern_argument_info.argument_num()

    def precise_score(self):
        """
        评估一个模式的准确程度，和参数数目和是否有变量有关系，=固定参数数目/参数总数
        :return: 0-1
        """
        if not self.has_variable():
            return 1.0
        num = self.pattern_argument_info.argument_num()
        return (num - self.variable_argument_num()) / num

    def fixed_argument_num(self):
        return self.pattern_argument_info.fixed_argument_num()

    def variable_argument_num(self):
        """
        获取当前模式里面变量的数目
        :return:
        """
        return self.pattern_argument_info.variable_argument_num()

    def get_scope_text(self, argument_name):
        """
        获取某个变量对应的所有信息
        :param argument_name:
        :return:
        """
        return self.pattern_argument_info.get_first_argument_instance(argument_name)

    def get_variable_max_len(self, variable_name):
        return self.pattern_argument_info.get_variable_max_len(variable_name)

    def get_all_fixed_words(self):
        # type(t.get("LEMMA"))!=dict 这个主要应对，冠词的lemma对应着是一些可以选择的词
        return set([t.get("LEMMA") for t in self.token_pattern_list if "LEMMA" in t and type(t.get("LEMMA")) != dict])

    def fixed_words_number(self):
        return len(self.get_all_fixed_words())

    def get_fixed_argument_word_num(self):
        num = 0
        for argument in self.get_all_fixed_argument_values():
            num = num + len(argument.split())
        return num


class PatternMatchingResultRecorder:
    def __init__(self):
        self.name2match_result_map = {}

    def add_new_matching_result(self, pattern_name, start, end, text):
        """
        记录pattern 地一个匹配地实例结果, 并且回合已经匹配地结果进行比较，只保留最好地一个匹配。我们目前地策略是最大匹配。
        :param pattern_name:
        :param start:
        :param end:
        :param text:
        :return:
        """
        scope_text = ScopeText(name=pattern_name, start=start, end=end, text=text, lemma_text=None)
        if not self.has_result(pattern_name=pattern_name):
            self.name2match_result_map[pattern_name] = scope_text
            return

        old_scope_text = self.get_match_result(pattern_name=pattern_name)
        if scope_text.contains_other(old_scope_text):
            # 目前是是一个模式有多个匹配，保留最长地那个，贪婪地
            self.name2match_result_map[pattern_name] = scope_text
        # todo: 完善这个方法

    def get_match_result(self, pattern_name):
        return self.name2match_result_map.get(pattern_name, None)

    def has_result(self, pattern_name):
        return pattern_name in self.name2match_result_map.keys()

    def __repr__(self):
        return "<PatternMatchingResultRecorder size=%d>" % self.size() + "\n" + "\n".join(
            ["%r:%r" % (k, v) for k, v in self.name2match_result_map.items()])

    def simple_repr(self):
        return "<PatternMatchingResultRecorder size=%r" % (self.size())

    def size(self):
        return len(self.name2match_result_map.keys())

    def get_pattern_names(self):
        return self.name2match_result_map.keys()

    def __iter__(self):
        for name, result in self.name2match_result_map.items():
            yield result
