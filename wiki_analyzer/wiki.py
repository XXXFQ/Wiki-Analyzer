import time
import glob
import sqlite3

ID_KEY = 'id'
TITLE_KEY = 'title'
DOCUMENT_KEY = 'document'
DB_PATH = 'wiki.db'
wiki_out_path = 'wiki_out'
wiki_data_paths = sorted(glob.iglob("text/*/wiki_*"))

def insert_titles(connection: sqlite3.Connection):
    cursor = connection.cursor()
    insert_titles_sql = f'REPLACE INTO wiki_table ({ID_KEY}, {TITLE_KEY}) VALUES(?, ?)'
    
    with open(wiki_out_path, 'r', encoding='UTF-8') as infile:
        data = [line.strip().split('\t') for line in infile.readlines()]
        cursor.executemany(insert_titles_sql, data)
    
    connection.commit()

if __name__ == '__main__':
    start = time.time()
    end = time.time()
    time_diff = end - start  # 処理完了後の時刻から処理開始前の時刻を減算する
    print(time_diff)
    
    sql = f"""SELECT COUNT(*) FROM wiki_table
    WHERE title LIKE '%群馬県%'
    """