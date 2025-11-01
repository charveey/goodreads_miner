# Goodreads Miner

A Python CLI tool and module for scraping book information from Goodreads lists and saving it into CSV files.

---

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

---

## Introduction

Currently, Goodreads **does not allow importing books directly from a list** into your account.  
This tool solves that problem by:

- Fetching one or multiple book lists  
- Generating a CSV that can be imported into your Goodreads account  

In short, it automates the tedious process of adding books manually.

This project provides a Python package and CLI script for scraping detailed information about books from Goodreads. It includes functions to:

- Retrieve book URLs from a Goodreads page
- Extract book details such as title, author, ISBN, and ratings
- Process multiple Goodreads list URLs from a file
- Save all collected data into CSV files

---

## Features

- Fetch books from a single list or multiple lists
- Generate a CSV ready for import into Goodreads
- Save scraped data into CSV files
- Unit tests covering edge cases and file handling

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/charveey/goodreads-miner.git
cd goodreads-miner
```

2. Install dependencies using UV:

```bash
uv install
```

## Usage

### CLI (Recommended)

Run the main script using `uv`:

```bash
uv run goodread_miner.main --file data/list.txt
```

### CLI Options

- `--url <goodreads_list_url>` : Scrape a single Goodreads list URL
- `--file <file_with_goodreads_lists_urls>` : Scrape multiple lists from a file
- `--test` : Run a predefined test URL

Example :

```bash
uv run goodread_miner.main --url https://www.goodreads.com/list/show/195641.Books_to_read_on_Kashmir
```

Output:

- The script generates a CSV file for each list in the `data/` folder.
- Filenames are derived from the list name, e.g., `195641 - Books_to_read_on_Kashmir.csv`.

### Module Usage

You can also use the package directly in Python:

```python
from goodread_miner.scraper import get_books, scrape_book
from goodread_miner.save_csv import save_import

books = get_books("https://www.goodreads.com/list/show/195641.Books_to_read_on_Kashmir")
data = [scrape_book(url, "2025-11-01") for url in books]
save_import(data, "data/list.csv")
```

## Documentation

Detailed docstrings are included in the code for all functions and classes in:

- `goodread_miner/scraper.py`
- `goodread_miner/save_csv.py`
- `goodread_miner/main.py`

## Running Tests

Run all tests using pytest:

```bash
pytest tests
```

- Mocks are used for network calls and file reads
- Edge cases for parsing, scraping, and CSV saving are fully covered

## TO-DO

- Allow specifying which Bookshelf to add the books to in Goodreads
- Add a `--output_dir` option to specify where the CSV file should be saved


## Contributing

Feel free to contribute to the project by opening issues or submitting pull requests. Contributions are always welcome!

## License

This script is licensed under the [MIT License](LICENSE).
