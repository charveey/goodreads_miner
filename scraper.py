"""
Goodreads Scraper Module

This module provides functions to scrape book information from Goodreads website.

Dependencies:
- bs4 (BeautifulSoup)

Functions:
- get_books(url: str) -> list[str]:
  Returns a list of book URLs from the given Goodreads page URL.

- get_isbn10(isbn) -> str | None:
  Returns the ISBN-10 of the given ISBN-13 if valid, otherwise returns None.

- get_book_infos(soup) -> tuple:
  Extracts book information from the provided BeautifulSoup object and returns a tuple
  containing book details such as title, author, ISBN, average rating, etc.

- get_year_first_published(soup) -> int | None:
  Retrieves the year of first publication from the provided BeautifulSoup object.

- get_id(bookid) -> str:
  Extracts the book ID from the given book URL.

- parse_name(fullname: str) -> str | None:
  Parses and formats the author's full name into "Last Name, First Name" format.

- scrape_book(book_url: str, date: str, bookshelf: str = "imported") -> dict[str, int | str | None]:
  Scrapes detailed information about a book from the given Goodreads book URL and returns a 
  dictionary containing various details such as title, author, ISBN, etc.

Usage Example:
```python
book_url = "https://www.goodreads.com/book/show/12345678"
today = "2023-12-24"
bookshelf = "imported by Kev"
book_info = scrape_book(book_url, today, bookshelf)
print(book_info)

Note:
    - Ensure that BeautifulSoup (bs4) is installed before using this module.
    - The website structure may affect the scraping results.
    - Handle exceptions appropriately when using these functions.

For more information on web scraping and BeautifulSoup, refer to the official documentation:
- BeautifulSoup: BeautifulSoup Documentation
- Web scraping guidelines: Python Web Scraping Tutorial
"""

import html
import json
import re
import time
from random import randint
from urllib.error import HTTPError
from urllib.request import urlopen

import bs4


def get_books(url: str) -> list[str]:
    """
    Retrieves a list of book URLs from the provided Goodreads list URL.

    Parameters:
    - url (str): The URL of the Goodreads page.

    Returns:
    - list[str]: A list of book URLs.
    """
    source = urlopen(url)
    soup = bs4.BeautifulSoup(source, "html.parser")
    return [a.get("href") for a in soup.find_all("a", class_="bookTitle")]


def get_isbn10(isbn) -> str | None:
    """
    Returns the ISBN-10 of the given ISBN-13 if valid, otherwise returns None.

    Parameters:
    - isbn: The ISBN-13 to be converted to ISBN-10.

    Returns:
    - str | None: The ISBN-10 if conversion is successful, otherwise None.
    """
    if isbn is None or len(isbn) != 13:
        return None
    elif isbn.startswith("978"):
        isbn = isbn.replace("978", "")
        return isbn
    else:
        return None


def get_book_infos(soup) -> tuple:
    """
    Extracts book information from the provided BeautifulSoup object.

    Parameters:
    - soup: BeautifulSoup object representing the HTML content of a book page on Goodreads.

    Returns:
    - tuple: A tuple containing book details such as title, author, ISBN, average rating, etc.
    """
    try:
        additional_authors: str = ""
        for script_tag in soup.find_all("script", {"type": "application/ld+json"}):
            data = json.loads(script_tag.string)
            if "isbn" in data:
                isbn: str = data["isbn"]
                title: str = html.unescape(data["name"])
                num_pages: int = data["numberOfPages"]
                book_format: str = data["bookFormat"]
                author: str = html.unescape(data["author"][0]["name"])
                if len(data["author"]) > 1:
                    for a in data["author"][1:]:
                        additional_authors += html.unescape(a["name"]) + ", "
                avg_rating: float = data["aggregateRating"]["ratingValue"]
                return (
                    title,
                    author,
                    additional_authors.strip().rstrip(","),
                    isbn,
                    avg_rating,
                    book_format,
                    num_pages,
                )
        return (None, None, None, None, None, None, None)
    except Exception:
        return (None, None, None, None, None, None, None)


def get_year_first_published(soup) -> int | None:
    """
    Retrieves the year of first publication from the provided BeautifulSoup object.

    Parameters:
    - soup: BeautifulSoup object representing the HTML content of a book page on Goodreads.

    Returns:
    - int | None: The year of first publication if available, otherwise None.
    """
    publication_paragraph = soup.find("p", attrs={"data-testid": "publicationInfo"})
    if publication_paragraph:
        publication_sentence = publication_paragraph.string
        return int(re.search("[0-9]{3,4}", publication_sentence).group())
    else:
        return None


def get_id(bookid) -> str:
    """
    Extracts the book ID from the given book URL.

    Parameters:
    - bookid: The book URL containing the book ID.

    Returns:
    - str: The extracted book ID.
    """
    pattern = re.compile("([^.-]+)")
    return pattern.search(bookid).group()


def parse_name(fullname: str) -> str | None:
    """
    Parses and formats the author's full name into "Last Name, First Name" format.

    Parameters:
    - fullname (str): The full name of the author.

    Returns:
    - str | None: The formatted name if valid, otherwise None.
    """
    if fullname is not None:
        names: list[str] = fullname.split(" ")
        if len(names) == 2:
            return f"{names[1]}, {names[0]}"
        elif len(names) > 2:
            last_name: str = names[-1:][0]
            first_names: str = ""
            for f_name in names[:-1]:
                first_names += f"{f_name} "
            return f"{last_name}, {first_names}"
    else:
        return None


def scrape_book(
    book_url: str, today: str, bookshelf: str = "imported by Kev"
) -> dict[str, int | str | None]:
    """
    Scrapes detailed information about a book from the given Goodreads book URL.

    Parameters:
    - book_url (str): The URL of the book on Goodreads.
    - today (str): The current date in the format "YYYY-MM-DD".
    - bookshelf (str): The name of the bookshelf. Default is "imported by Kev".

    Returns:
    - dict[str, int | str | None]: A dictionary containing various details such as title, author, ISBN, etc.
    """
    url: str = "https://www.goodreads.com" + book_url
    try:
        source = urlopen(url)
    except HTTPError:
        time.sleep(randint(1, 5))
        source = urlopen(url)
    soup = bs4.BeautifulSoup(source, "html.parser")
    (
        title,
        author,
        more_authors,
        isbn13,
        avg_rating,
        book_format,
        num_pages,
    ) = get_book_infos(soup)
    book_id = book_url.replace("/book/show/", "")
    return {
        "Book Id": get_id(book_id),
        "Title": title,
        "Author": author,
        "Author l-f": parse_name(author),
        "Additional Authors": more_authors,
        "Original Publication Year": get_year_first_published(soup),
        "ISBN13": f'="{isbn13}"',
        "ISBN": f'="{get_isbn10(isbn13)}"',
        "Number of Pages": num_pages,
        "Date Added": today,
        "Exclusive Shelf": bookshelf,
        "Bookshelves": bookshelf,
        "Binding": book_format,
        "Average Rating": avg_rating,
    }
