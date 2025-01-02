import glob

from .config import DB_PATH
from .database_initializer import DatabaseInitializer
from .wiki_text_processor import WikiTextProcessor

def main():
    '''
    Main function for processing Wikipedia data.
    '''
    # Get paths to Wikipedia data files
    wiki_data_paths = sorted(glob.iglob("data/text/*/wiki_*"))

    # Initialize WikiTextProcessor with the database path
    processor = WikiTextProcessor(DB_PATH)

    # Initialize the database and insert Wikipedia data
    db_initializer = DatabaseInitializer()
    db_initializer.initialize()

    processor.setup_database(wiki_data_paths)

    # Perform morphological analysis on Wikipedia articles
    processor.parse_wiki_text()

__all__ = [
    'main',
]