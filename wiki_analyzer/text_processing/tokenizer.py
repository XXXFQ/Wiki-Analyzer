import re
import MeCab

from ..config import MECAB_NEOLOGD_PATH
from ..utils import Logger

logger = Logger.get_logger(__name__)

class TextTokenizer:
    '''
    A utility class for performing morphological analysis using MeCab.
    '''
    def __init__(self, use_neologd: bool=False):
        '''
        Initialize the TextTokenizer with the specified MeCab dictionary.

        Parameters
        ----------
        use_neologd : bool, optional
            If True, use the Neologd dictionary. Default is False.
        '''
        dictionary_option = f' -d "{MECAB_NEOLOGD_PATH}"' if use_neologd else ""
        self.tagger = MeCab.Tagger(f"-Owakati{dictionary_option}")
    
    def tokenize(self, text: str) -> list:
        '''
        Tokenize the text into words.

        Parameters
        ----------
        text : str
            Input text.

        Returns
        -------
        list
            List of tokenized words.
        '''
        return self.tagger.parse(text).strip().split()

    def remove_symbols(self, text: str) -> str:
        '''
        Remove symbols from the input text.

        Parameters
        ----------
        text : str
            Input text.

        Returns
        -------
        str
            Text with symbols removed.
        '''
        symbol_pattern = r'[!"#$%&\'\\()*+,-./:;<=>?@[\\]^_`{|}~「」〔〕“”〈〉『』【】＆＊・（）＄＃＠。、？！｀＋￥％\uFF01-\uFF0F\uFF1A-\uFF20\uFF3B-\uFF40\uFF5B-\uFF65\u3000-\u303F]'
        cleaned_text = re.sub(symbol_pattern, '', text)
        return cleaned_text
