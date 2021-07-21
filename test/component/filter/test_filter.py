from unittest import TestCase
from component.filter.filter import Filter
from component.model.api_knowledge import APIKnowledge


class TestFilter(TestCase):
    def test_filter_patterns_by_invalid_object(self):
        _filter = Filter()
        api_knowledge_dicts = [
            {
                "api": "NativeWebRequest",
                "objects": {
                    "object1": "-api-",
                    "object2": "the"
                }
            },
            {
                "api": "getView()",
                "objects": {
                    "object1": "in",
                    "object2": "the"
                }
            },
            {
                "api": "java.time.Duration",
                "objects": {
                    "object1": "directly",
                    "object2": "store",
                    "object3": "automatically"
                }
            },
            {
                "api": "getErrorCode()",
                "objects": {
                    "object1": "SQLException",
                    "object2": "returns",
                    "object3": "failure"
                }
            }
        ]
        knowledge = [APIKnowledge.from_dict(d) for d in api_knowledge_dicts]
        for k in knowledge:
            print(_filter.is_valid_api_knowledge(k))
