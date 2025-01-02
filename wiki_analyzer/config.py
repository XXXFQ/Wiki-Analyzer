import platform
from pathlib import Path

# OSの種類
_pf = platform.system()

# MeCabの辞書のパスを、OSによって変更
if _pf == 'Windows':
    MECAB_NEOLOGD_PATH = Path(r"C:\Program Files (x86)\MeCab\dic\mecab-ipadic-neologd")
else:
    MECAB_NEOLOGD_PATH = Path("/var/lib/mecab/dic/mecab-ipadic-neologd")

# データの保存ディレクトリ
DATA_DIR = Path('./data')
DATA_DIR.mkdir(exist_ok=True)

# Wikipediaのデータベースのパス
DB_PATH = DATA_DIR / 'wikipedia.db'

# モデルの保存先
WIKI_MODEL_PATH = DATA_DIR / 'word2vec.model'
WORD2_VEC_MODEL_PATH = DATA_DIR / 'word2vec.model.pt'