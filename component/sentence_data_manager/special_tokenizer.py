import re
import spacy
from spacy.lang.char_classes import ALPHA_LOWER, ALPHA_UPPER, CONCAT_QUOTES, LIST_ELLIPSES, LIST_ICONS, ALPHA
from spacy.symbols import ORTH
from spacy.tokenizer import Tokenizer
from spacy.util import compile_infix_regex


class SpecialTokenizer:
    @staticmethod
    def modified_hyphen_segmentation(nlp):
        infix = (
                LIST_ELLIPSES
                + LIST_ICONS
                + [
                    r"(?<=[0-9])[+\-\*^](?=[0-9-])",
                    r"(?<=[{al}{q}])\.(?=[{au}{q}])".format(
                        al=ALPHA_LOWER, au=ALPHA_UPPER, q=CONCAT_QUOTES
                    ),
                    r"(?<=[{a}]),(?=[{a}])".format(a=ALPHA),
                    r"(?<=[{a}0-9])[:<>=/](?=[{a}])".format(a=ALPHA),
                ]
        )
        infix_re = compile_infix_regex(infix)
        nlp.tokenizer.infix_finditer = infix_re.finditer
        return nlp

    @staticmethod
    def custom_tokenizer(nlp):
        special_cases = {":)": [{"ORTH": ":)"}]}
        prefix_re = re.compile(r'''^[\[\("']''')
        suffix_re = re.compile(r'''[\]\)"']$''')
        infix_re = re.compile(r'''[~]''')
        simple_url_re = re.compile(r'''^https?://''')
        return Tokenizer(nlp.vocab, rules=special_cases,
                         prefix_search=prefix_re.search,
                         suffix_search=suffix_re.search,
                         infix_finditer=infix_re.finditer,
                         url_match=simple_url_re.match)

    @staticmethod
    def modified_sign_segmentation(nlp):
        """
        处理 eg:  org.w3c.dom.Document -> "org.w3c.dom", ".", "Document"
                 *nix -> "*", "nix"
                 C# -> 'C' '#'
        """
        nlp.tokenizer = SpecialTokenizer.custom_tokenizer(nlp)
        return nlp

    @staticmethod
    def modified_brackets_segmentation(nlp):
        """
        处理字符后括号问题
        eg:   super() -> 'super'   '('   ')'
              System.exit(1) ->"System.exit(1", ")"
              List<Integer> -> "List","<","Integer", ">"
        """
        suffixes = list(nlp.Defaults.suffixes)
        suffixes.remove("\\)")
        suffixes.remove("\\]")
        suffixes.remove(">")
        suffix_regex = spacy.util.compile_suffix_regex(suffixes)
        nlp.tokenizer.suffix_search = suffix_regex.search
        return nlp
