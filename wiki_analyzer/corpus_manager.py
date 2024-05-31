from .database.wiki_table_manager import WikiTableManager
from .database.constants import (
    WAKATI_TABLE,
    WAKATI_TEXT_KEY
)

class SQLiteCorpus:
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

    def __iter__(self):
        '''
        コーパスをイテレータとして返す
        '''
        with WikiTableManager(self.db_path) as wiki_db:
            # データベースに接続しクエリを実行
            sql = f"SELECT {WAKATI_TEXT_KEY} FROM {WAKATI_TABLE}"
            rows = wiki_db.execute_query(sql)
            
            # 結果を1行ずつ処理し、形態素解析結果を返す
            for row in rows.fetchall():
                yield row[0].split()