import glob

from .config import DATABASE_PATH
from .database_initializer import DatabaseInitializer
from .wiki_text_processor import WikiTextProcessor

def main():
    '''
    Main function for processing Wikipedia data.
    '''
    # Get paths to Wikipedia data files
    wiki_data_paths = sorted(glob.iglob("data/text/*/wiki_*"))

    # Initialize the database and insert Wikipedia data
    DatabaseInitializer().initialize()

    processor = WikiTextProcessor(DATABASE_PATH)
    processor.setup_database(wiki_data_paths)

    # Perform morphological analysis on Wikipedia articles
    processor.parse_wiki_text()

__all__ = [
    'main',
]