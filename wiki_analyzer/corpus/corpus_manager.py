from ..database import SQLiteHandler
from ..database.constants import (
    WIKI_TOKENIZED_TABLE,
    WIKI_TOKENIZED_WAKATI_TEXT_KEY
)

class SQLiteCorpus:
    '''
    A class to create an iterable corpus from a SQLite database containing Wikipedia data.
    '''
    def __init__(self, database_path: str):
        '''
        Constructor for SQLiteCorpus.

        Parameters
        ----------
        database_path : str
            Path to the SQLite database containing Wikipedia data.

        Attributes
        ----------
        db_connection : SQLiteHandler
            Database connection handler.
        '''
        self.db_connection = SQLiteHandler(database_path)

    def __iter__(self):
        '''
        Returns an iterator that yields tokenized text from the database.

        Each line of tokenized text is split into tokens and yielded one by one.

        Yields
        ------
        list of str
            A list of tokens from each row of tokenized text in the database.
        '''
        # Query to retrieve tokenized text from the database
        query = f"SELECT {WIKI_TOKENIZED_WAKATI_TEXT_KEY} FROM {WIKI_TOKENIZED_TABLE}"
        rows = self.db_connection.execute_query(query)

        # Process each row and yield the tokenized text
        for row in rows.fetchall():
            yield row[0].split()
