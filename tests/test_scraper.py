from unittest.mock import patch
import json
from bs4 import BeautifulSoup
from goodreads_miner.scraper import (
    get_books,
    get_isbn10,
    get_book_infos,
    get_year_first_published,
    get_id,
    parse_name,
    scrape_book,
)


# ------------------------
# Test get_isbn10
# ------------------------
def test_get_isbn10_valid():
    assert get_isbn10("9781234567897") == "1234567897"

def test_get_isbn10_invalid_length():
    assert get_isbn10("123456789") is None

def test_get_isbn10_non_978_prefix():
    assert get_isbn10("1234567890123") is None


# ------------------------
# Test parse_name
# ------------------------
def test_parse_name_two_parts():
    assert parse_name("John Doe") == "Doe, John"

def test_parse_name_multiple_parts():
    assert parse_name("Mary Jane Smith") == "Smith, Mary Jane "

def test_parse_name_none():
    assert parse_name(None) is None


# ------------------------
# Test get_id
# ------------------------
def test_get_id():
    url = "/book/show/12345678.Some-Book-Title"
    assert get_id(url) == "12345678"  # match actual extracted book ID

# ------------------------
# Test get_books (mock network)
# ------------------------
@patch("goodreads_miner.scraper.urlopen")
def test_get_books(mock_urlopen):
    html_content = """
    <html>
        <body>
            <a class="bookTitle" href="/book/show/1">Book 1</a>
            <a class="bookTitle" href="/book/show/2">Book 2</a>
        </body>
    </html>
    """
    mock_urlopen.return_value = html_content.encode("utf-8")
    with patch("bs4.BeautifulSoup") as mock_soup:
        soup_instance = BeautifulSoup(html_content, "html.parser")
        mock_soup.return_value = soup_instance
        urls = get_books("https://example.com")
        assert urls == ["/book/show/1", "/book/show/2"]


# ------------------------
# Test get_book_infos
# ------------------------
def test_get_book_infos_basic():
    json_data = {
        "isbn": "1234567890123",
        "name": "Test Book",
        "numberOfPages": 200,
        "bookFormat": "Hardcover",
        "author": [{"name": "John Doe"}],
        "aggregateRating": {"ratingValue": 4.5},
    }
    soup = BeautifulSoup(
        f'<script type="application/ld+json">{json.dumps(json_data)}</script>',
        "html.parser",
    )
    info = get_book_infos(soup)
    assert info[0] == "Test Book"
    assert info[1] == "John Doe"
    assert info[3] == "1234567890123"
    assert info[4] == 4.5
    assert info[5] == "Hardcover"
    assert info[6] == 200


# ------------------------
# Test get_year_first_published
# ------------------------
def test_get_year_first_published():
    soup = BeautifulSoup(
        '<p data-testid="publicationInfo">Published 2015 by Some Publisher</p>',
        "html.parser",
    )
    assert get_year_first_published(soup) == 2015

def test_get_year_first_published_none():
    soup = BeautifulSoup("<p>No publication info</p>", "html.parser")
    assert get_year_first_published(soup) is None


# ------------------------
# Test scrape_book (mock network)
# ------------------------
@patch("goodreads_miner.scraper.urlopen")
def test_scrape_book(mock_urlopen):
    html_content = """
    <html>
        <script type="application/ld+json">
        {
            "isbn": "9781234567897",
            "name": "Test Book",
            "numberOfPages": 300,
            "bookFormat": "Hardcover",
            "author": [{"name": "John Doe"}],
            "aggregateRating": {"ratingValue": 4.2}
        }
        </script>
        <p data-testid="publicationInfo">Published 2010 by Publisher</p>
    </html>
    """
    mock_urlopen.return_value = html_content.encode("utf-8")
    result = scrape_book("/book/show/1", "2025-11-01")
    assert result["Title"] == "Test Book"
    assert result["Author"] == "John Doe"
    assert result["ISBN13"] == '="9781234567897"'
    assert result["ISBN"] == '="1234567897"'
    assert result["Number of Pages"] == 300
    assert result["Original Publication Year"] == 2010
    assert result["Average Rating"] == 4.2
