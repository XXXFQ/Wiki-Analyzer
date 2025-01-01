from .database.wiki_table_manager import WikiTableManager
from .database.constants import (
    WAKATI_TABLE,
    WAKATI_TEXT_KEY
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
        db_path : str
            Stores the path to the SQLite database.
        '''
        self.db_path = database_path

    def __iter__(self):
        '''
        Returns an iterator that yields tokenized text from the database.

        Each line of tokenized text is split into tokens and yielded one by one.

        Yields
        ------
        list of str
            A list of tokens from each row of tokenized text in the database.
        '''
        with WikiTableManager(self.db_path) as db_manager:
            # Query to retrieve tokenized text from the database
            query = f"SELECT {WAKATI_TEXT_KEY} FROM {WAKATI_TABLE}"
            rows = db_manager.execute_query(query)

            # Process each row and yield the tokenized text
            for row in rows.fetchall():
                yield row[0].split()
