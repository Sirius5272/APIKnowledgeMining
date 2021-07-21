from typing import TypeVar, Iterable, Set, List

from kgdt.utils import SaveLoad
from spacy.matcher.matcher import Matcher

from component.model.pattern import Pattern
from util.spacy_util import NLPUtil

T = TypeVar('T', bound='PatternCollection')


class PatternCollection(SaveLoad):
    """
    储存总结出来的pattern的集合
    """

    def __init__(self):
        self.name2pattern_map = {}
        self.pattern_set = set([])
        self.id2pattern = {}
        self.pattern2id = {}
        self.max_id = 0

    def add(self, pattern: Pattern):
        """
        返回添加的pattern的id，保证自增不重复
        :param pattern:
        :return:添加的pattern的id
        """
        if pattern == None:
            return -1
        if pattern in self.pattern2id:
            return self.pattern2id[pattern]

        self.pattern_set.add(pattern)
        pattern_name = pattern.get_name()
        self.name2pattern_map[pattern_name] = pattern

        pattern_id = self.max_id
        self.id2pattern[pattern_id] = pattern
        self.pattern2id[pattern] = pattern_id

        self.max_id = pattern_id + 1
        return pattern_id

    def to_id(self, pattern: Pattern) -> int:
        if pattern == None:
            return -1
        if pattern not in self.pattern_set:
            return -1
        return self.pattern2id[pattern]

    def to_pattern(self, id: int) -> Pattern:
        return self.id2pattern.get(id, None)

    def to_patterns(self, ids: Iterable[int]) -> List[Pattern]:
        result = []
        for id in set(ids):
            instance = self.to_pattern(id)
            if instance == None:
                continue
            result.append(instance)
        return result

    def get_patterns(self):
        return self.pattern_set

    def add_all(self, patterns: Iterable[Pattern]):
        for p in patterns:
            self.add(p)

    def get_pattern(self, name) -> Pattern:
        return self.name2pattern_map.get(name, None)

    def size(self):
        return len(self.pattern_set)

    def __len__(self):
        return self.size()

    def include(self, pattern: Pattern):
        if pattern == None:
            return False
        return pattern in self.pattern_set

    def __repr__(self):
        return "<PatternCollection size=%d max_id=%d>" % (self.size(), self.max_id)

    def simple_repr(self):
        return "<PatternCollection size=%r" % (self.size())

    def __iter__(self):
        for p in self.pattern_set:
            yield p

    def new(self, patterns: Iterable[Pattern]) -> Set[Pattern]:
        return set(self) - set(patterns)

    def get_patterns_sort_by_conf(self) -> List[Pattern]:
        return sorted(self.pattern_set, key=lambda item: item.confidence, reverse=True)

    def print_by_conf(self):
        for p in self.get_patterns_sort_by_conf():
            print(self.to_id(pattern=p), p.confidence, p)


class MatcherHelper(SaveLoad):
    """
    储存用来匹配的Pattern
    """

    def __init__(self, pattern_collection: PatternCollection = None):
        self.matcher = NLPUtil.get_spacy_matcher()
        if pattern_collection is None:
            pattern_collection = PatternCollection()
        self.pattern_collection = pattern_collection

    def get_pattern_collection(self) -> PatternCollection:
        return self.pattern_collection

    def add_pattern(self, pattern: Pattern):
        self.pattern_collection.add(pattern=pattern)
        pattern_name = pattern.get_name()
        pattern_list = pattern.get_token_pattern_list()
        if len(pattern_list) <= 1:
            return
        self.matcher.add(pattern_name, [pattern_list])

    def add_patterns(self, patterns):
        for p in patterns:
            if p is not None:
                self.add_pattern(p)

    def get_pattern(self, name) -> Pattern:
        return self.pattern_collection.get_pattern(name)

    def get_matcher(self) -> Matcher:
        return self.matcher

    def size(self):
        return self.pattern_collection.size()

    def __iter__(self):
        for p in self.pattern_collection:
            yield p

    def __repr__(self):
        return "<MatcherHelper size=%d>" % (self.size())
