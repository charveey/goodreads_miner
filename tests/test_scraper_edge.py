from unittest.mock import patch, mock_open
import pytest
from bs4 import BeautifulSoup
from goodread_miner.scraper import (
    get_books,
    get_isbn10,
    get_book_infos,
    get_year_first_published,
    parse_name,
    scrape_book,
    get_id
)

# Edge-case tests for parsing functions
@pytest.mark.parametrize("isbn,expected", [
    (None, None),
    ("", None),
    ("123", None),
    ("9780000000000", "0000000000"),
    ("9790000000000", None),
])
def test_get_isbn10_edge(isbn, expected):
    assert get_isbn10(isbn) == expected

@pytest.mark.parametrize("fullname,expected", [
    (None, None),
    ("SingleName", None),
    ("First Last", "Last, First"),
    ("Mary Jane Smith", "Smith, Mary Jane "),
])
def test_parse_name_edge(fullname, expected):
    assert parse_name(fullname) == expected

# Test get_book_infos with missing JSON script tag or invalid JSON
def test_get_book_infos_no_script():
    soup = BeautifulSoup("<html><head></head><body><p>No data</p></body></html>", "html.parser")
    result = get_book_infos(soup)
    assert result == (None, None, None, None, None, None, None)

@pytest.mark.parametrize("bookid,expected", [
    ("/book/show/12345678.Some-Book-Title", "12345678"),
    ("12345678-Title", "12345678"),
    ("/book/show/1", "1"),
    ("-LeadingDash", ""),
    ("NoDigitsHere", ""),
])
def test_get_id_edge(bookid, expected):
    assert get_id(bookid) == expected

def test_get_book_infos_malformed_json():
    soup = BeautifulSoup(
        '<script type="application/ld+json">{"not":"valid",}</script>',
        "html.parser"
    )
    result = get_book_infos(soup)
    assert result == (None, None, None, None, None, None, None)

# Test get_year_first_published edge cases
def test_get_year_first_published_missing():
    soup = BeautifulSoup("<p>No publicationInfo attr</p>", "html.parser")
    assert get_year_first_published(soup) is None

def test_get_year_first_published_invalid_format():
    soup = BeautifulSoup(
        '<p data-testid="publicationInfo">Published in Month Year</p>',
        "html.parser"
    )
    with pytest.raises(AttributeError):
        # Because re.search(...).group() will fail if no match
        _ = get_year_first_published(soup)

# Fake file content
FAKE_DATA = """
https://www.goodreads.com/list/show/195641.Books_to_read_on_Kashmir
https://www.goodreads.com/list/show/195860.Books_for_Players_of_Sid_Meier_s_Civilization_Games
https://www.goodreads.com/list/show/195838.Best_Sci_Fi_and_Fantasy_reads
"""

@pytest.fixture
def list_urls():
    with patch("builtins.open", mock_open(read_data=FAKE_DATA)):
        # read_urls_from_file() now reads from the mocked file
        return [line.strip() for line in FAKE_DATA.splitlines() if line.strip()]

@patch("goodread_miner.scraper.urlopen")
@patch("bs4.BeautifulSoup")
def test_get_books_from_lists(mock_bs4, mock_urlopen, list_urls):
    # Simulate each list URL returning a page with 2 book links
    html_template = """
    <html><body>
        <a class="bookTitle" href="/book/show/1">Book1</a>
        <a class="bookTitle" href="/book/show/2">Book2</a>
    </body></html>
    """
    for url in list_urls:
        mock_urlopen.return_value = html_template.encode("utf8")
        mock_bs4.return_value = BeautifulSoup(html_template, "html.parser")

        books = get_books(url)
        assert books == ["/book/show/1", "/book/show/2"]

@patch("goodread_miner.scraper.urlopen")
def test_scrape_book_full_flow(mock_urlopen):
    # Simulate a full book page with valid data
    html_content = """
    <html>
      <script type="application/ld+json">
      {
        "isbn": "9781234567897",
        "name": "Edge Book",
        "numberOfPages": 400,
        "bookFormat": "Kindle",
        "author": [{"name": "Edge Author"}, {"name": "Co-Author"}],
        "aggregateRating": {"ratingValue": 3.8}
      }
      </script>
      <p data-testid="publicationInfo">Published 1999 by SomePublisher</p>
    </html>
    """
    mock_urlopen.return_value = html_content.encode("utf8")

    result = scrape_book("/book/show/9999", "2025-11-01", bookshelf="testShelf")
    assert result["Title"] == "Edge Book"
    assert result["Author"] == "Edge Author"
    assert result["Author l-f"] == "Author, Edge"
    assert result["Additional Authors"] == "Co-Author"
    assert result["ISBN13"] == '="9781234567897"'
    assert result["ISBN"] == '="1234567897"'
    assert result["Number of Pages"] == 400
    assert result["Original Publication Year"] == 1999
    assert result["Exclusive Shelf"] == "testShelf"
    assert result["Bookshelves"] == "testShelf"
    assert result["Average Rating"] == 3.8

@patch("goodread_miner.scraper.urlopen", side_effect=Exception("Network error"))
def test_scrape_book_network_failure(mock_urlopen):
    with pytest.raises(Exception):
        # If urlopen fails (and no fallback implemented), expect exception
        _ = scrape_book("/book/show/1000", "2025-11-01")
