from unittest import TestCase
from component.sentence_data_manager.sentence_data_manager import SentenceDataManager


class TestSentenceDataManager(TestCase):
    def test_contains_api_name(self):
        sentences = [
            "this is a sentence contains a kind of class mention like org.omg.PortableInterceptor. ",
            "or this is another sentence contains a API mention of method like isInt(). ",
            "perhaps there are some API mentions like Float.toString(float). ",
            "maybe contains parameter like toString(float)",
            "or full API name like java.lang.Float.toHexString(float)"
        ]
        for sentence in sentences:
            print(SentenceDataManager.contains_api_name(sentence))

    def test_replace_api_with_placeholder(self):
        text = "Call addObserver() on AccountManager for each of the GUI classes."
        new_text = SentenceDataManager.replace_api_with_placeholder(text)
        print(new_text)
