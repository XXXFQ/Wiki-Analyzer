import re
import unicodedata

from tqdm import tqdm
from bs4 import BeautifulSoup

from .text_processing import TextTokenizer
from .database.constants import WIKI_CONTENTS_TABLE
from .database import (
    SQLiteHandler,
    WikiContentsTableHandler,
    WikiPagesTableHandler,
    WikiTokenizedTableHandler
)
from .utils import Logger

logger = Logger.get_logger(__name__)

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
        db_connection : SQLiteHandler
            Database connection handler.
        '''
        self.db_connection = SQLiteHandler(database_path)

    def setup_database(self, wiki_data_paths: list=None):
        '''
        Initialize the database and insert Wikipedia data.

        Parameters
        ----------
        wiki_data_paths : list
            List of file paths containing Wikipedia data to insert into the database.
        '''
        wiki_contents_table_handler = WikiContentsTableHandler(self.db_connection)
        wiki_pages_table_handler = WikiPagesTableHandler(self.db_connection)
        
        # Insert Wikipedia data into the database
        logger.info("Inserting Wikipedia data into the database.")
        for data_path in tqdm(wiki_data_paths, desc="Inserting Wikipedia data"):
            with open(data_path, 'r', encoding='UTF-8') as file:
                xml_content = file.read()

            wiki_docs = BeautifulSoup(xml_content, 'lxml').find_all('doc')

            # Add each document to the database
            for doc in wiki_docs:
                text_content = re.sub(r'^\n.+\n\n', '', doc.text) # Remove unwanted leading text
                wiki_pages_table_handler.insert_page(doc['id'], doc['url'], doc['title'])
                wiki_contents_table_handler.insert_contents(doc['id'], text_content)

        # Commit changes
        self.db_connection.commit()
        logger.info("Wikipedia data inserted successfully.")

    def parse_wiki_text(self):
        '''
        Perform morphological analysis on Wikipedia articles and store the results.
        '''
        wiki_tokenized_table_handler = WikiTokenizedTableHandler(self.db_connection)
        text_tokenizer = TextTokenizer(use_neologd=True)
        query = f"SELECT * FROM {WIKI_CONTENTS_TABLE}"
        rows = self.db_connection.execute_query(query)
        
        logger.info("Parsing Wikipedia text.")
        for page_id, content in tqdm(rows.fetchall(), desc="Parsing Wikipedia text"):
            normalized_text = unicodedata.normalize('NFKC', content)
            tokenized_text = text_tokenizer.tokenize(normalized_text)
            cleaned_text = text_tokenizer.remove_symbols("\t".join(tokenized_text))
            wiki_tokenized_table_handler.insert_wakati(page_id, cleaned_text)

        self.db_connection.commit()
        logger.info("Wikipedia text parsed successfully.")
