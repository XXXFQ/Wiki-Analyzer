import re
import glob
import unicodedata

import MeCab
from tqdm import tqdm
from bs4 import BeautifulSoup
from gensim.models import Word2Vec, KeyedVectors

from .corpus_manager import SQLiteCorpus
from .database.wiki_table_manager import WikiTableManager
from .database.constants import (
    CONTENTS_TABLE,
    DB_PATH,
)

# MeCabの初期化
_tagger = MeCab.Tagger("-Owakati")

def setup_database(wiki_db : WikiTableManager, wiki_data_paths : list = None):
    '''
    データベースを初期化する
    
    Parameters
    ----------
    wiki_db : WikiTableManager
        WikiTableManagerオブジェクト
    wiki_data_paths : list
        データベースに追加するWikipediaのデータのパス
    '''
    wiki_db.create_tables()
    wiki_db.create_indexes()
    
    # データベースにWikipediaのデータを追加
    for wiki_data in tqdm(wiki_data_paths):
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

def parse_wiki_text(wiki_db : WikiTableManager):
    '''
    Wikipediaの記事を形態素解析する
    
    Parameters
    ----------
    wiki_db : WikiTableManager
        WikiTableManagerオブジェクト
    '''
    sql = f"SELECT * FROM {CONTENTS_TABLE}"
    rows = wiki_db.execute_query(sql)
    
    for page_id, document in tqdm(rows.fetchall()):
        normalized_text = unicodedata.normalize('NFKC', document)
        wakati = _mecab_analyzer(text=normalized_text)
        wiki_db.insert_wakati(page_id, "\t".join(wakati))
    
    wiki_db.commit()

def _mecab_analyzer(text: str) -> list:
    '''
    テキストを形態素解析する
    
    Parameters
    ----------
    text : str
        テキスト
    
    Returns
    -------
    list
        形態素解析結果
    '''
    global _tagger
    node = _tagger.parseToNode(text)
    tokens = []
    while node:
        surface = node.surface
        if surface != "":
            tokens.append(surface)
        node = node.next
    return tokens

def main():
    wiki_db = WikiTableManager(DB_PATH)
    wiki_data_paths = sorted(glob.iglob("data/text/*/wiki_*"))
    
    # データベースを初期化
    # setup_database(wiki_db, wiki_data_paths)
    
    # Wikipediaの記事を形態素解析
    parse_wiki_text(wiki_db)
    
    # コーパスを読み込む
    corpus = SQLiteCorpus(DB_PATH)

    # Word2Vecモデルの訓練
    model = Word2Vec(sentences=corpus, vector_size=200, window=15, min_count=20, workers=4)

    # モデルを保存する
    model.save("wiki.model")

    # モデルのロードとテスト
    model = Word2Vec.load("wiki.model")
    
    wv = KeyedVectors.load_word2vec_format('wiki.model', binary=True)
    results = wv.most_similar(positive='アンパサンド')
    for result in results:
        print(result)

__all__ = [
    'main',
]