from pathlib import Path

# テーブル名
PAGES_TABLE = 'pages'
CONTENTS_TABLE = 'contents'
WAKATI_TABLE = 'wakati'
TOKENS_TABLE = 'tokens'

# カラム名
PAGES_PRIMARY_KEY  = 'page_id'
PAGES_URL_KEY = 'url'
PAGE_TITLE_KEY = 'title'

CONTENTS_PRIMARY_KEY = 'page_id'
CONTENTS_TEXT_KEY = 'text'

WAKATI_PRIMARY_KEY = 'page_id'
WAKATI_TEXT_KEY = 'wakati'

DATA_DIR = Path('data')
DB_PATH = DATA_DIR / 'wikipedia.db'