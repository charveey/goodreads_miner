# Goodreads Scraper

A Python module and script for scraping book information from Goodreads.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This project provides a Python module and script for scraping detailed information about books from Goodreads. It includes functions to retrieve book URLs, extract book details, and process Goodreads list URLs.

## Features

- Retrieve book URLs from a Goodreads page.
- Extract detailed information about books from Goodreads using BeautifulSoup.
- Process Goodreads list URLs and save the data to a CSV file.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/goodreads-scraper.git
   cd goodreads-scraper
   ```

2. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Module usage

```python
# Example module usage
from scraper import get_books, scrape_book

# Your code here...
```

### Script usage

```bash
# Example script usage
python main.py --url https://www.goodreads.com/list/show/195641.Books_to_read_on_Kashmir
```

For more options, run `python main.py --help`.

## Documentation

Detailed documentation for the module functions and script is available in the code. Check the docstrings for each function in the `scraper.py` and `main.py` files.

## Contributing

Feel free to contribute to the project by opening issues or submitting pull requests. Contributions are always welcome!

## License

This script is licensed under the [MIT License](LICENSE).
