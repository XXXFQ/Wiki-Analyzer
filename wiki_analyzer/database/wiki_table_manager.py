from .database_manager import DatabaseManager
from .constants import (
    PAGES_TABLE,
    CONTENTS_TABLE,
    WAKATI_TABLE,
    PAGES_PRIMARY_KEY,
    PAGES_URL_KEY,
    PAGE_TITLE_KEY,
    CONTENTS_PRIMARY_KEY,
    CONTENTS_TEXT_KEY,
    WAKATI_PRIMARY_KEY,
    WAKATI_TEXT_KEY,
)

class WikiTableManager(DatabaseManager):
    def __init__(self, db_path: str):
        # データベースに接続する
        super().__init__(db_path)
        
        # テーブルの情報
        self.pages_table_info = {
            'name': PAGES_TABLE,
            'columns': {
                PAGES_PRIMARY_KEY: 'INTEGER PRIMARY KEY',
                PAGES_URL_KEY: 'TEXT',
                PAGE_TITLE_KEY: 'TEXT'
            }
        }
        self.contents_table_info = {
            'name': CONTENTS_TABLE,
            'columns': {
                CONTENTS_PRIMARY_KEY: 'INTEGER PRIMARY KEY',
                CONTENTS_TEXT_KEY: 'TEXT'
            },
            'foreign_keys': [
                {'column': CONTENTS_PRIMARY_KEY, 'references': f'PAGES_TABLE({PAGES_PRIMARY_KEY})'}
            ]
        }
        self.wakati_table_info = {
            'name': WAKATI_TABLE,
            'columns': {
                WAKATI_PRIMARY_KEY: 'INTEGER PRIMARY KEY',
                WAKATI_TEXT_KEY: 'TEXT'
            },
            'foreign_keys': [
                {'column': WAKATI_PRIMARY_KEY, 'references': f'PAGES_TABLE({PAGES_PRIMARY_KEY})'}
            ]
        }
    
    def __enter__(self) -> 'WikiTableManager':
        '''
        トランザクションを開始する
        '''
        self.execute_query('BEGIN')
        return self
    
    def create_tables(self):
        '''
        テーブルを作成する
        '''
        self.create_table(self.pages_table_info)
        self.create_table(self.contents_table_info)
        self.create_table(self.wakati_table_info)
    
    def create_table(self, table_info: dict):
        '''
        テーブルを作成する
        
        Parameters
        ----------
        table_info : dict
            テーブルの情報
        '''
        columns = ', '.join([f'{column} {type}' for column, type in table_info['columns'].items()])
        
        # 外部キー定義の文字列を作成（存在する場合）
        foreign_keys = ''
        if 'foreign_keys' in table_info:
            foreign_keys = ', '.join([f"FOREIGN KEY ({fk['column']}) REFERENCES {fk['references']}" for fk in table_info['foreign_keys']])
        
        # テーブル作成クエリの組み立て
        if foreign_keys:
            query = f"CREATE TABLE IF NOT EXISTS {table_info['name']} ({columns}, {foreign_keys})"
        else:
            query = f"CREATE TABLE IF NOT EXISTS {table_info['name']} ({columns})"
        
        # クエリの実行
        self.execute_query(query)
    
    def create_indexes(self):
        '''
        インデックスを作成する
        '''
        self.create_index(PAGES_TABLE, PAGES_URL_KEY)
        self.create_index(CONTENTS_TABLE, CONTENTS_TEXT_KEY)
        self.create_index(WAKATI_TABLE, WAKATI_TEXT_KEY)
    
    def create_index(self, table_name: str, column_name: str):
        '''
        インデックスを作成する
        
        Parameters
        ----------
        table_name : str
            テーブル名
        column_name : str
            カラム名
        '''
        query = f"CREATE INDEX IF NOT EXISTS {table_name}_{column_name}_index ON {table_name} ({column_name})"
        self.execute_query(query)
    
    def insert_page(self, page_id: int, url: str, title: str):
        '''
        ページ情報を挿入する
        
        Parameters
        ----------
        page_id : int
            ページID
        url : str
            URL
        title : str
            タイトル
        '''
        query = f'''
        INSERT OR IGNORE INTO {PAGES_TABLE} (
            {PAGES_PRIMARY_KEY},
            {PAGES_URL_KEY},
            {PAGE_TITLE_KEY}
        ) VALUES (?, ?, ?)'''
        self.execute_query(query, (page_id, url, title))
    
    def insert_contents(self, page_id: int, text: str):
        '''
        本文を挿入する
        
        Parameters
        ----------
        page_id : int
            ページID
        text : str
            本文
        '''
        query = f'''
        INSERT OR IGNORE INTO {CONTENTS_TABLE} (
            {CONTENTS_PRIMARY_KEY},
            {CONTENTS_TEXT_KEY}
        ) VALUES (?, ?)'''
        self.execute_query(query, (page_id, text))
    
    def insert_wakati(self, page_id: int, wakati: str):
        '''
        分かち書きを挿入する
        
        Parameters
        ----------
        page_id : int
            ページID
        wakati : str
            分かち書き
        '''
        query = f'''
        INSERT OR IGNORE INTO {WAKATI_TABLE} (
            {WAKATI_PRIMARY_KEY},
            {WAKATI_TEXT_KEY}
        ) VALUES (?, ?)'''
        self.execute_query(query, (page_id, wakati))