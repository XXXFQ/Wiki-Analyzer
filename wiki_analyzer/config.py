from pathlib import Path

# データの保存ディレクトリ
DATA_DIR = Path('./data')
DATA_DIR.mkdir(exist_ok=True)

# Wikipediaのデータベースのパス
DB_PATH = DATA_DIR / 'wikipedia.db'

# モデルの保存先
WIKI_MODEL_PATH = DATA_DIR / 'word2vec.model'
WORD2_VEC_MODEL_PATH = DATA_DIR / 'word2vec.model.pt'