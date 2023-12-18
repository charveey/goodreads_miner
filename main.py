import sys
from datetime import date
from goodreads_miner.scraper import get_books, scrape_book
from goodreads_miner.save_csv import save_import


def main() -> None:
    if len(sys.argv) == 3 and sys.argv[1] == "--url":
        save_import(process_url(sys.argv[2]), f"{get_list_name(sys.argv[2])}.csv")
    elif len(sys.argv) == 3 and sys.argv[1] == "--file":
        pass
    elif len(sys.argv) == 2 and sys.argv[1] == "--test":
        test = "https://www.goodreads.com/list/show/195641.Books_to_read_on_Kashmir"
        save_import(process_url(test), f"{get_list_name(test)}.csv")
    else:
        sys.exit(
            "Invalid usage.\nUse --url goodread_list_url or --file text_file_with_goodread_lists_url."
        )


def process_url(url: str) -> list[dict]:
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
    # TO-DO
    ...


def get_list_name(url: str) -> str:
    if url.startswith("https://"):
        url = url.replace("https://www.", "")
    elif url.startswith("www"):
        url = url.replace("www.", "")
    url = url.replace("goodreads.com/list/show/", "")
    list_id, list_name = url.split(".")
    return f"{list_id} - {list_name}"


if __name__ == "__main__":
    main()
