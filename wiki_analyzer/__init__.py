import glob

from .wiki_text_processor import WikiTextProcessor
from .database.wiki_table_manager import WikiTableManager
from .config import DB_PATH

def main():
    '''
    メイン関数
    '''
    # Wikipediaのデータのパスを取得
    wiki_data_paths = sorted(glob.iglob("data/text/*/wiki_*"))
    
    # Wikipediaのデータを処理するクラスを初期化
    processor = WikiTextProcessor(DB_PATH)
    
    # データベースを初期化
    processor.setup_database(wiki_data_paths)
    
    # Wikipediaの記事を形態素解析
    processor.parse_wiki_text()

__all__ = [
    'main',
]