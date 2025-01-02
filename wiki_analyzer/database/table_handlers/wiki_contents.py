from ..common import SQLiteHandler, TableHandlerInterface
from ..constants import (
    WIKI_PAGES_TABLE,
    WIKI_PAGES_PRIMARY_KEY,
    WIKI_CONTENTS_TABLE,
    WIKI_CONTENTS_PRIMARY_KEY,
    WIKI_CONTENTS_TEXT_KEY,
)

class WikiContentsTableHandler(TableHandlerInterface):
    def __init__(self, db_connection: SQLiteHandler):
        '''
        Initialize the WikiContentsTableHandler class.

        Parameters
        ----------
        db_connection : SQLiteHandler
            Database connection handler.
        '''
        table_name = WIKI_CONTENTS_TABLE
        columns_with_types = {
            WIKI_CONTENTS_PRIMARY_KEY: 'INTEGER PRIMARY KEY',
            WIKI_CONTENTS_TEXT_KEY: 'TEXT'
        }
        foreign_keys = [
            f'FOREIGN KEY ({WIKI_CONTENTS_PRIMARY_KEY}) REFERENCES {WIKI_PAGES_TABLE}({WIKI_PAGES_PRIMARY_KEY}) ON UPDATE CASCADE ON DELETE CASCADE',
        ]
        
        super().__init__(db_connection, table_name, columns_with_types, WIKI_CONTENTS_PRIMARY_KEY, foreign_keys)
    
    def insert_contents(self, page_id: int, text: str):
        '''
        Insert page content into the database.

        Parameters
        ----------
        page_id : int
            Page ID.
        text : str
            Content of the page.
        '''
        columns, placeholders = self._prepare_columns_and_placeholders(self.columns_with_types)
        query = f"REPLACE INTO {self.table_name} ({columns}) VALUES ({placeholders})"
        self.db_connection.execute_query(query, (page_id, text))
