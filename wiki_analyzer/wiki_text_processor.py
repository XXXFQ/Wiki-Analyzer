import re
import unicodedata

import MeCab
from tqdm import tqdm
from bs4 import BeautifulSoup

from .config import MECAB_NEOLOGD_PATH
from .database.wiki_table_manager import WikiTableManager
from .database.constants import CONTENTS_TABLE

# Initialize MeCab with Neologd dictionary
_MECAB_TAGGER = MeCab.Tagger(f'-Owakati -d "{MECAB_NEOLOGD_PATH}"')

class WikiTextProcessor:
    '''
    A class for processing Wikipedia data, storing it in a database, and performing text preprocessing tasks.
    '''
    def __init__(self, database_path: str):
        '''
        Constructor for WikiTextProcessor

        Parameters
        ----------
        database_path : str
            Path to the Wikipedia database.

        Attributes
        ----------
        db_path : str
            Stores the database path.
        '''
        self.db_path = database_path

    def setup_database(self, wiki_data_paths: list=None):
        '''
        Initialize the database and insert Wikipedia data.

        Parameters
        ----------
        wiki_data_paths : list
            List of file paths containing Wikipedia data to insert into the database.
        '''
        with WikiTableManager(self.db_path) as db_manager:
            db_manager.create_tables()
            db_manager.create_indexes()

            # Insert Wikipedia data into the database
            for data_path in tqdm(wiki_data_paths, desc="Inserting Wikipedia data"):
                with open(data_path, 'r', encoding='UTF-8') as file:
                    xml_content = file.read()

                soup = BeautifulSoup(xml_content, 'lxml')
                wiki_docs = soup.find_all('doc')

                # Add each document to the database
                for doc in wiki_docs:
                    text_content = re.sub(r'^\n.+\n\n', '', doc.text)  # Remove unwanted leading text
                    db_manager.insert_page(doc['id'], doc['url'], doc['title'])
                    db_manager.insert_contents(doc['id'], text_content)

            # Commit changes
            db_manager.commit()

    def parse_wiki_text(self):
        '''
        Perform morphological analysis on Wikipedia articles and store the results.
        '''
        query = f"SELECT * FROM {CONTENTS_TABLE}"

        with WikiTableManager(self.db_path) as db_manager:
            rows = db_manager.execute_query(query)

            for page_id, content in tqdm(rows.fetchall(), desc="Parsing Wikipedia text"):
                normalized_text = unicodedata.normalize('NFKC', content)
                tokenized_text = self._mecab_analyze(text=normalized_text)
                cleaned_text = self._remove_symbols("\t".join(tokenized_text))
                db_manager.insert_wakati(page_id, cleaned_text)

            db_manager.commit()

    def _mecab_analyze(self, text: str) -> list:
        '''
        Perform morphological analysis using MeCab.

        Parameters
        ----------
        text : str
            Input text to analyze.

        Returns
        -------
        list
            List of tokens extracted by morphological analysis.
        '''
        wakati_text = _MECAB_TAGGER.parse(text).strip().split()
        return wakati_text
    
    def _remove_symbols(self, text: str) -> str:
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
