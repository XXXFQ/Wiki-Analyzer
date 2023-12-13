import sqlite3

from .config import (
    ID_KEY,
    TITLE_KEY,
    WIKI_TITLE_TABLE,
    DOCUMENT_KEY,
    WIKI_DOCUMENT_TABLE
)

class WikiDatabase:
    def __init__(self, db_path: str):
        # データベースに接続する
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        
        # データベースにテーブルがない場合は作成する
        self._create_wiki_title_table()
        self._create_wiki_document_table()

    def __del__(self):
        '''
        データベースを閉じる
        '''
        self.connection.close()
   
    def _create_wiki_title_table(self):
        '''
        データベースにタイトルテーブルを作成する
        '''  
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {WIKI_TITLE_TABLE} (
            {ID_KEY} INTEGER PRIMARY KEY,
            {TITLE_KEY} TEXT)'''
        )
        self.connection.commit()
    
    def _create_wiki_document_table(self):
        '''
        データベースにドキュメントテーブルを作成する
        '''
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {WIKI_DOCUMENT_TABLE} (
            {ID_KEY} INTEGER PRIMARY KEY,
            {DOCUMENT_KEY} TEXT,
            FOREIGN KEY({ID_KEY}) REFERENCES {WIKI_TITLE_TABLE}({ID_KEY}))'''
        )
        self.connection.commit()
    
    def insert_titles(self, id : str, title : str):
        '''
        データベースにタイトルを挿入する
        '''
        insert_titles_sql = f'REPLACE INTO {WIKI_TITLE_TABLE} ({ID_KEY}, {TITLE_KEY}) VALUES(?, ?)'
        self.cursor.execute(insert_titles_sql, (id, title))
    
    def insert_wiki_texts(self, id : str, document : str):
        '''
        データベースにドキュメントを挿入する
        '''
        insert_titles_sql = f'REPLACE INTO {WIKI_DOCUMENT_TABLE} ({ID_KEY}, {DOCUMENT_KEY}) VALUES(?, ?)'
        self.cursor.execute(insert_titles_sql, (id, document))
    
    def get_titles(self):
        '''
        データベースからタイトルを取得する
        '''
        get_titles_sql = f'SELECT {ID_KEY}, {TITLE_KEY} FROM {WIKI_TITLE_TABLE}'
        self.cursor.execute(get_titles_sql)
        return self.cursor.fetchall()