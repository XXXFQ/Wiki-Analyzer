import re
import glob
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

def main():
    wiki_database = WikiDatabase(DB_PATH)
    # init_db(wiki_database)
    
    sql = f"""SELECT COUNT(*) FROM {WIKI_DOCUMENT_TABLE}
    WHERE {DOCUMENT_KEY} LIKE '%群馬県%'
    """
    
    wiki_database.cursor.execute(sql)
    res = wiki_database.cursor.fetchall()
    
    pass

__all__ = [
    'main'
]