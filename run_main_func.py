# Allow direct execution
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import wiki_analyzer

if __name__ == '__main__':
    wiki_analyzer.main()