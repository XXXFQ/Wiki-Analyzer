from .database.wiki_table_manager import WikiTableManager
from .database.constants import (
    CONTENTS_TABLE,
    CONTENTS_TEXT_KEY,
    DB_PATH
)

class SQLiteCorpus:
    def __init__(self, db_path):
        self.db_path = db_path

    def __iter__(self):
        sql = f'''SELECT {CONTENTS_TEXT_KEY} FROM {CONTENTS_TABLE}'''
        wiki_db = WikiTableManager(DB_PATH)
        
        for row in wiki_db.execute_query(sql):
            yield row[0]