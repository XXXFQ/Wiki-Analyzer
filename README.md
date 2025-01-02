# Wiki-Analyzer

Wiki-Analyzer is a program designed to retrieve data from Wikipedia and create a Word2Vec model based on that data.

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/XXXFQ/Wiki-Analyzer.git
   cd Wiki-Analyzer
   ```

2. Install the required packages:

    ```bash
    poetry install
    ```

## Downloading Wikipedia Data

Run the following command to download the latest Japanese Wikipedia data:

```bash
curl https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2 -o jawiki-latest-pages-articles.xml.bz2
```

## Extracting Articles from the Dump Data

Use the following command to extract article content from the downloaded XML data:

```bash
python -m wikiextractor.WikiExtractor jawiki-latest-pages-articles.xml.bz2
```

## Environment Requirements

* **Python**: 3.10

## Copyright

Copyright (C) 2025 ARM