import sqlite3

from .config import (
    WIKI_TITLE_TABLE,
    ID_KEY,
    TITLE_KEY,
    WIKI_DOCUMENT_TABLE,
    DOCUMENT_KEY,
    POS_TABLE,
    POS_ID_KEY,
    POS_KEY,
    WORD_TABLE,
    WID_KEY,
    WORD_KEY,
    ANALYSIS_TABLE
)

class WikiDatabase:
    def __init__(self, db_path: str):
        # データベースに接続する
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        
        # データベースにテーブルがない場合は作成する
        self._create_wiki_title_table()
        self._create_wiki_document_table()
        self._create_pos_table()
        self._create_word_table()
        self._create_analysis_table()

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
    
    def _create_pos_table(self):
        '''
        データベースに品詞テーブルを作成する
        '''
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {POS_TABLE} (
            {POS_ID_KEY} INTEGER PRIMARY KEY,
            {POS_KEY} TEXT)'''
        )
        self.connection.commit()
    
    def _create_word_table(self):
        '''
        データベースに単語テーブルを作成する
        '''
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {WORD_TABLE} (
            {WID_KEY} INTEGER PRIMARY KEY AUTOINCREMENT,
            {WORD_KEY} TEXT)'''
        )
        self.connection.commit()
    
    def _create_analysis_table(self):
        '''
        データベースに解析用テーブルを作成する
        '''
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {ANALYSIS_TABLE} (
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
    
    def insert_pos(self, pos_id : str, pos : str):
        '''
        データベースに品詞を挿入する
        '''
        insert_pos_sql = f'INSERT INTO pos_table (pos_id, pos) VALUES(?, ?)'
        self.cursor.execute(insert_pos_sql, (pos_id, pos))
    
    def insert_word(self, wid : str, word : str):
        '''
        データベースに単語を挿入する
        '''
        insert_word_sql = f'INSERT INTO word_table (wid, word) VALUES(?, ?)'
        self.cursor.execute(insert_word_sql, (wid, word))
    
    def insert_analysis(self, id : str, document : str):
        '''
        データベースに解析用のデータを挿入する
        '''
        insert_analysis_sql = f'REPLACE INTO {ANALYSIS_TABLE} ({ID_KEY}, {DOCUMENT_KEY}) VALUES(?, ?)'
        self.cursor.execute(insert_analysis_sql, (id, document))
    
    def get_titles(self):
        '''
        データベースからタイトルを取得する
        '''
        get_titles_sql = f'SELECT {ID_KEY}, {TITLE_KEY} FROM {WIKI_TITLE_TABLE}'
        self.cursor.execute(get_titles_sql)
        return self.cursor.fetchall()