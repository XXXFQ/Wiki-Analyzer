from ..common import SQLiteHandler, TableHandlerInterface
from ..constants import (
    WIKI_PAGES_TABLE,
    WIKI_PAGES_PRIMARY_KEY,
    WIKI_PAGES_TITLE_KEY,
    WIKI_PAGES_URL_KEY
)

class WikiPagesTableHandler(TableHandlerInterface):
    '''
    Handler for the "Pages" table, which stores basic page information.
    '''
    def __init__(self, db_connection: SQLiteHandler):
        '''
        Initialize the WikiPagesTableHandler class.

        Parameters
        ----------
        db_connection : SQLiteHandler
            Database connection handler.
        '''
        table_name = WIKI_PAGES_TABLE
        columns_with_types = {
            WIKI_PAGES_PRIMARY_KEY: 'INTEGER PRIMARY KEY',
            WIKI_PAGES_TITLE_KEY: 'TEXT',
            WIKI_PAGES_URL_KEY: 'TEXT'
        }
        
        super().__init__(db_connection, table_name, columns_with_types, WIKI_PAGES_PRIMARY_KEY)
    
    def insert_page(self, page_id: int, url: str, title: str):
        '''
        Insert page information into the database.

        Parameters
        ----------
        page_id : int
            Page ID.
        url : str
            URL of the page.
        title : str
            Title of the page.
        '''
        columns, placeholders = self._prepare_columns_and_placeholders(self.columns_with_types)
        query = f"REPLACE INTO {self.table_name} ({columns}) VALUES ({placeholders})"
        self.db_connection.execute_query(query, (page_id, url, title))
