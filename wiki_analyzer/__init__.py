import re
import glob
import MeCab
import unicodedata
from tqdm import tqdm
from bs4 import BeautifulSoup

from .wiki_database import WikiDatabase
from .config import (
    DB_PATH,
    ID_KEY,
    TITLE_KEY,
    WIKI_TITLE_TABLE,
    DOCUMENT_KEY,
    WIKI_DOCUMENT_TABLE
)

def init_db(wiki_database : WikiDatabase):
    '''
    データベースを初期化する
    '''
    wiki_data_paths = sorted(glob.iglob("data/text/*/wiki_*"))
    
    for wiki_data in tqdm(wiki_data_paths):
        with open(wiki_data, 'r', encoding='UTF-8') as infile:
            xml_text = infile.read()

        soup = BeautifulSoup(xml_text, 'lxml')
        docs = soup.find_all('doc')
        
        for doc in docs:
            text = re.sub(r'^\n.+\n\n', '', doc.text)
            wiki_database.insert_titles(doc['id'], doc['title'])
            wiki_database.insert_wiki_texts(doc['id'], text)
    
    wiki_database.connection.commit()
    del wiki_database

def morphological_analysis_wiki(wiki_database : WikiDatabase):
    '''
    データベースにあるテキストを形態素解析する
    '''
    sql = f'''SELECT * FROM {WIKI_DOCUMENT_TABLE}'''
    wiki_database.cursor.execute(sql)
    documents = wiki_database.cursor.fetchall()
    tagger = MeCab.Tagger('-ochasen')
    
    for document in tqdm(documents):
        normalized_text = unicodedata.normalize('NFKC', document[1])
        wiki_database.insert_analysis(document[0], tagger.parse(normalized_text))
    
    wiki_database.connection.commit()
    del wiki_database

"""
def morphological_analysis_wiki(wiki_database : WikiDatabase):
    '''
    データベースにあるテキストを形態素解析する
    '''
    sql = f'''SELECT {DOCUMENT_KEY} FROM {WIKI_DOCUMENT_TABLE} LIMIT 1'''
    wiki_database.cursor.execute(sql)
    texts = wiki_database.cursor.fetchall()
    
    tagger = MeCab.Tagger('-ochasen')
    
    for text in tqdm(texts):
        normalized_text = unicodedata.normalize('NFKC', text[0])
        node = tagger.parseToNode(normalized_text)
        doc = []
        pos1 = []
        pos2 = []
        while node:
            doc.append(node.surface)
            pos1.append(node.feature.split(',')[0])
            pos2.append(node.feature.split(',')[1])
            node = node.next
        
        wiki_database.insert_analysis(doc, pos1, pos2)
    
    # wiki_database.connection.commit()
    # del wiki_database
    pass
"""

def main():
    wiki_database = WikiDatabase(DB_PATH)
    
    # データベースを初期化
    # init_db(wiki_database)
    
    # 形態素解析
    morphological_analysis_wiki(wiki_database)
    
    '''
    with open('data/pos-id.def', 'r', encoding='UTF-8') as infile:
        pos_id_def = infile.read()
        
        regex = re.compile(r'^(\D+),(\D+) (\d+)$')
        
        for line in pos_id_def.split('\n'):
            if line == '':
                continue
            
            pos_1, pos_2 = regex.match(line).group(1, 2)
            pos_id = regex.match(line).group(3)
            wiki_database.insert_pos(pos_id, pos_1, pos_2)
    '''
    
    # テスト用
    sql = f'''
    SELECT COUNT(*) FROM {WIKI_DOCUMENT_TABLE}
    WHERE {DOCUMENT_KEY} LIKE '%群馬県%'
    '''

__all__ = [
    'main'
]