import re
import unicodedata

import MeCab
from tqdm import tqdm
from bs4 import BeautifulSoup

from .database.wiki_table_manager import WikiTableManager
from .database.constants import CONTENTS_TABLE

# MeCabの初期化
_MECAB_TAGGER = MeCab.Tagger('-Owakati -d "C:/Program Files (x86)/MeCab/dic/ipadic" -u "C:/Program Files (x86)/MeCab/dic/NEologd/NEologd.20200910-u.dic"')

class WikiTextProcessor:
    def __init__(self, db_path):
        '''
        コンストラクタ
        
        Parameters
        ----------
        db_path : str
            Wikipediaのデータベースのパス
        
        Attributes
        ----------
        db_path : str
            Wikipediaのデータベースのパス
        '''
        self.db_path = db_path

    def setup_database(self, wiki_data_paths : list = None):
        '''
        データベースを初期化する
        
        Parameters
        ----------
        wiki_data_paths : list
            データベースに追加するWikipediaのデータのパス
        '''
        with WikiTableManager(self.db_path) as wiki_db:
            wiki_db.create_tables()
            wiki_db.create_indexes()
        
            # データベースにWikipediaのデータを追加
            for wiki_data in tqdm(wiki_data_paths, desc="Inserting wiki data"):
                with open(wiki_data, 'r', encoding='UTF-8') as infile:
                    xml_text = infile.read()
                
                soup = BeautifulSoup(xml_text, 'lxml')
                docs = soup.find_all('doc')
                
                # ページごとにデータベースに追加
                for doc in docs:
                    text = re.sub(r'^\n.+\n\n', '', doc.text) # ページの先頭にある不要な文字列を削除
                    wiki_db.insert_page(doc['id'], doc['url'], doc['title'])
                    wiki_db.insert_contents(doc['id'], text)
            
            # コミット
            wiki_db.commit()

    def parse_wiki_text(self):
        '''
        Wikipediaの記事を形態素解析する
        '''
        sql = f"SELECT * FROM {CONTENTS_TABLE}"
        
        with WikiTableManager(self.db_path) as wiki_db:
            rows = wiki_db.execute_query(sql)

            for page_id, document in tqdm(rows.fetchall(), desc="Parsing wiki text"):
                normalized_text = unicodedata.normalize('NFKC', document)
                wakati_text = self._mecab_analyze(text=normalized_text)
                cleaned_text = self._remove_symbols("\t".join(wakati_text))
                wiki_db.insert_wakati(page_id, cleaned_text)
            
            wiki_db.commit()

    def _mecab_analyze(self, text: str) -> list:
        '''
        形態素解析を行う
        
        Parameters
        ----------
        text : str
            入力テキスト
        
        Returns
        -------
        list
            形態素解析されたトークンのリスト
        '''
        wakati_text = _MECAB_TAGGER.parse(text).strip().split()
        return wakati_text
    
    def _remove_symbols(self, text: str) -> str:
        '''
        文章から記号を除去する
        
        Parameters
        ----------
        text : str
            文章
        
        Returns
        -------
        str
            記号を除去した文章
        '''
        remove_symbols_pattern = r'[!"#$%&\'\\()*+,-./:;<=>?@[\\]^_`{|}~「」〔〕“”〈〉『』【】＆＊・（）＄＃＠。、？！｀＋￥％\uFF01-\uFF0F\uFF1A-\uFF20\uFF3B-\uFF40\uFF5B-\uFF65\u3000-\u303F]'
        cleaned_text = re.sub(remove_symbols_pattern, '', text)
        return cleaned_text