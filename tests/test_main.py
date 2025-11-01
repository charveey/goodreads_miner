from pathlib import Path
from unittest.mock import patch, mock_open
import pytest
import sys
from goodreads_miner import main as main_module

DATA_FILE = "data/data.txt"


# ------------------------
# Test: --file argument
# ------------------------
@patch("builtins.open", new_callable=mock_open, read_data=(
    "https://www.goodreads.com/list/show/195641.Books_to_read_on_Kashmir\n"
    "https://www.goodreads.com/list/show/195860.Books_for_Players_of_Sid_Meier_s_Civilization_Games\n"
    "https://www.goodreads.com/list/show/195838.Best_Sci_Fi_and_Fantasy_reads\n"
))
@patch("goodreads_miner.main.save_import")
@patch("goodreads_miner.main.get_books", return_value=["/book/show/1", "/book/show/2"])
@patch("goodreads_miner.main.scrape_book", return_value={"Title": "Book1"})
def test_main_file(mock_scrape, mock_get_books, mock_save, mock_file):
    test_argv = ["main.py", "--file", DATA_FILE, "--bookshelf", "to-read", "--output_dir", "exports"]
    with patch.object(sys, "argv", test_argv):
        main_module.main()

        # File opened correctly
        mock_file.assert_called_once_with(DATA_FILE, encoding="utf8")

        # get_books called once per list URL
        assert mock_get_books.call_count == 3

        # scrape_book called once per book URL (3 lists × 2 books)
        assert mock_scrape.call_count == 6

        # save_import called once
        mock_save.assert_called_once()

        # Check keyword argument "bookshelf" is passed correctly
        _, kwargs = mock_save.call_args
        assert kwargs["bookshelf"] == "to-read"

        # Check filename/path
        filename_arg = mock_save.call_args[0][1]  # second positional argument → filename
        assert Path(filename_arg).name.startswith("data") or Path(filename_arg).suffix == ".csv"


# ------------------------
# Test: --url argument
# ------------------------
@patch("goodreads_miner.main.save_import")
@patch("goodreads_miner.main.get_books", return_value=["/book/show/1"])
@patch("goodreads_miner.main.scrape_book", return_value={"Title": "TestBook"})
def test_main_url(mock_scrape, mock_get_books, mock_save):
    url = "https://www.goodreads.com/list/show/195641.Books_to_read_on_Kashmir"
    test_argv = ["main.py", "--url", url, "--bookshelf", "favorites"]
    with patch.object(sys, "argv", test_argv):
        main_module.main()

        # get_books called with the provided URL
        mock_get_books.assert_called_once_with(url)

        # scrape_book called for each book
        mock_scrape.assert_called_once()

        # save_import called once
        mock_save.assert_called_once()

        # Check keyword argument "bookshelf" is passed correctly
        _, kwargs = mock_save.call_args
        assert kwargs["bookshelf"] == "favorites"

        # Check filename/path
        filename_arg = mock_save.call_args[0][1]
        assert "195641" in Path(filename_arg).name
        assert Path(filename_arg).suffix == ".csv"


# ------------------------
# Test: invalid arguments
# ------------------------
def test_main_invalid_args():
    test_argv = ["main.py", "--invalid"]
    with patch.object(sys, "argv", test_argv):
        with pytest.raises(SystemExit):
            main_module.main()


# ------------------------
# Test: file with empty lines
# ------------------------
@patch("builtins.open", new_callable=mock_open, read_data=(
    "\nhttps://www.goodreads.com/list/show/195641.Books_to_read_on_Kashmir\n\n"
))
@patch("goodreads_miner.main.save_import")
@patch("goodreads_miner.main.get_books", return_value=["/book/show/1"])
@patch("goodreads_miner.main.scrape_book", return_value={"Title": "Book1"})
def test_main_file_empty_lines(mock_scrape, mock_get_books, mock_save, mock_file):
    test_argv = ["main.py", "--file", DATA_FILE]
    with patch.object(sys, "argv", test_argv):
        main_module.main()

        mock_file.assert_called_once()
        args, kwargs = mock_file.call_args
        assert args[0] == DATA_FILE
        assert kwargs.get("encoding") == "utf8"

        # Only one URL processed
        assert mock_get_books.call_count == 1
        assert mock_scrape.call_count == 1
        mock_save.assert_called_once()
