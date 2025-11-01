import sys
from datetime import date
from pathlib import Path
from goodreads_miner import scrape_book, get_books, save_import


def main() -> None:
    """
    Main entry point for the script.

    Command line arguments:
    - --url <goodreads_list_url>: Process a Goodreads list URL.
    - --file <file_with_goodreads_lists_urls>: Process a file containing Goodreads list URLs.
    - --bookshelf <shelf_name>: Specify the Goodreads bookshelf for import metadata (optional, default: "to-read")
    - --output_dir <path>: Directory where the CSV file will be saved (optional, default: current directory)

    Example:
        python main.py --url https://www.goodreads.com/list/show/12345.My_Favorite_Books --bookshelf read --output_dir exports
    """
    args = parse_args(sys.argv[1:])  # expects a dict or Namespace

    # Determine data and filename
    if args.get("url"):
        data = process_url(args["url"])
        filename = f"{get_list_name(args['url'])}.csv"
    elif args.get("file"):
        data = process_file(args["file"])
        filename = f"{Path(args['file']).stem}.csv"
    else:
        sys.exit("Invalid usage.\nUse --url <url> or --file <file>.")

    # Prepare output directory
    output_dir = Path(args.get("output_dir", "."))
    output_dir.mkdir(parents=True, exist_ok=True)
    save_path = output_dir / filename

    # Save CSV, passing bookshelf only if specified
    save_import(data, str(save_path), bookshelf=args.get("bookshelf", "to-read"))



def parse_args(argv):
    args = {"bookshelf": "imported by Goodread miner", "output_dir": "."}
    i = 0
    while i < len(argv):
        if i + 1 >= len(argv):
            sys.exit(f"Missing value for argument: {argv[i]}")
        if argv[i] == "--url":
            args["url"] = argv[i + 1]
        elif argv[i] == "--file":
            args["file"] = argv[i + 1]
        elif argv[i] == "--bookshelf":
            args["bookshelf"] = argv[i + 1]
        elif argv[i] == "--output_dir":
            args["output_dir"] = argv[i + 1]
        else:
            sys.exit(f"Unknown argument: {argv[i]}")
        i += 2
    return args



def process_url(url: str) -> list[dict]:
    """Processes a Goodreads list URL and returns a list of book info."""
    today = date.today()
    books_data = []
    books_urls = get_books(url)
    for idx, link in enumerate(books_urls, start=1):
        print(f"Processing book {idx}/{len(books_urls)}")
        book = scrape_book(link, str(today))
        books_data.append(book)
        print(f"Processed {book['Title']} successfully")
    return books_data


def process_file(txtfile: str) -> list[dict]:
    """Processes a file containing multiple Goodreads list URLs."""
    today = date.today()
    books_data = []
    with open(txtfile, encoding="utf8") as file:
        links = [line.strip() for line in file if line.strip()]
    for list_url in links:
        books_urls = get_books(list_url)
        for link in books_urls:
            book = scrape_book(link, str(today))
            books_data.append(book)
    return books_data


def get_list_name(url: str) -> str:
    """Extracts the list name from a Goodreads list URL."""
    if url.startswith("https://"):
        url = url.replace("https://www.", "")
    elif url.startswith("www."):
        url = url.replace("www.", "")
    url = url.replace("goodreads.com/list/show/", "")
    list_id, list_name = url.split(".")
    return f"{list_id} - {list_name}"


if __name__ == "__main__":
    main()
