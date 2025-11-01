import sys
from datetime import date
from goodread_miner import scrape_book, get_books, save_import


def main() -> None:
    """
    Main entry point for the script.

    Command line arguments:
    - --url <goodreads_list_url>: Process a Goodreads list URL.
    - --file <file_with_goodreads_lists_urls>: Process a file containing Goodreads list URLs.
    - --test: Process a predefined test Goodreads list URL.

    If no valid arguments are provided, the script processes a default file ("list.txt").
    """
    if len(sys.argv) == 3 and sys.argv[1] == "--url":
        save_import(process_url(sys.argv[2]), f"{get_list_name(sys.argv[2])}.csv")
    elif len(sys.argv) == 3 and sys.argv[1] == "--file":
        save_import(process_file(sys.argv[2]), f"{sys.argv[2].split('.')[0]}.csv")     
    elif len(sys.argv) == 2 and sys.argv[1] == "--test":
        test = "https://www.goodreads.com/list/show/195641.Books_to_read_on_Kashmir"
        save_import(process_url(test), f"{get_list_name(test)}.csv")
    else:
        sys.exit(
            "Invalid usage.\nUse --url goodread_list_url or --file file_with_goodread_lists_urls."
        )

def process_url(url: str) -> list[dict]:
    """
    Processes a Goodreads list URL and returns a list of dictionaries containing book information.

    Parameters:
    - url (str): The Goodreads list URL.

    Returns:
    - list[dict]: A list of dictionaries containing book information.
    """
    progress: int = 0
    today = date.today()
    books_data: list = []
    books_urls: list = get_books(url)
    for link in books_urls:
        progress += 1
        print(f"Processing books: {progress}/{len(books_urls)}")
        books_data.append(scrape_book(link, str(today)))
        print(f"Processed {books_data[-1]['Title']} succesfully")
    return books_data


def process_file(txtfile) -> list[dict]:
    """
    Processes a file containing Goodreads list URLs and returns a list of dictionaries containing book information.

    Parameters:
    - txtfile: The path to the file containing Goodreads list URLs.

    Returns:
    - list[dict]: A list of dictionaries containing book information.
    """
    # TO-DO:
    # check if the link matches the list or the book format first
    # add a progress checker too
    today = date.today()
    links: list[str] = []
    books: list[str] = []
    books_data: list[dict] = []
    with open(file=txtfile, encoding="utf8") as file:
        links = [line.strip() for line in file if line.strip()]
    for link in links:
        books.extend(get_books(link))
    for book in books:
        books_data.append(scrape_book(book, str(today)))
    return books_data


def get_list_name(url: str) -> str:
    """
    Extracts the list name from a Goodreads list URL.

    Parameters:
    - url (str): The Goodreads list URL.

    Returns:
    - str: The formatted list name.
    """
    if url.startswith("https://"):
        url = url.replace("https://www.", "")
    elif url.startswith("www"):
        url = url.replace("www.", "")
    url = url.replace("goodreads.com/list/show/", "")
    list_id, list_name = url.split(".")
    return f"{list_id} - {list_name}"


if __name__ == "__main__":
    main()