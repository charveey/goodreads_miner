# Goodreads List Scraper

This script allows you to scrape information about books from a Goodreads list and save it to a CSV file.

## Usage

### To scrape a Goodreads list from a URL

```bash
python script.py --url <goodreads_list_url>
```

This will process the specified Goodreads list URL and save the information to a CSV file with a name based on the list.

### To use a test URL

```bash
python script.py --test
```

This will use a predefined test Goodreads list URL for testing purposes and save the information to a CSV file.

### Other Options

- `--file`: To be implemented. Currently, it does not have any functionality.
  
## Dependencies

- [Beautiful Soup 4](https://code.launchpad.net/beautifulsoup): a Python library for pulling data out of HTML and XML files. It works with your favorite parser to provide idiomatic ways of navigating, searching, and modifying the parse tree. It commonly saves programmers hours or days of work.
  
## How It Works

1. The script takes command-line arguments to determine the operation.
2. If a Goodreads list URL is provided, it scrapes book information from the list and saves it to a CSV file.
3. If a test flag is provided, a predefined Goodreads list URL is used for testing purposes.
4. The list name is extracted from the URL to create a meaningful CSV file name.

## Usage Example

```bash
# Scrape a Goodreads list from a URL
python script.py --url https://www.goodreads.com/list/show/195641.Books_to_read_on_Kashmir
```

## License

This script is licensed under the [MIT License](LICENSE).