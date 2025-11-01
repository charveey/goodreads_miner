from unittest.mock import patch, mock_open
import pytest
import sys
from goodread_miner import main as main_module

DATA_FILE = "data/data.txt"

@patch("builtins.open", new_callable=mock_open, read_data=(
    "https://www.goodreads.com/list/show/195641.Books_to_read_on_Kashmir\n"
    "https://www.goodreads.com/list/show/195860.Books_for_Players_of_Sid_Meier_s_Civilization_Games\n"
    "https://www.goodreads.com/list/show/195838.Best_Sci_Fi_and_Fantasy_reads\n"
))
@patch("goodread_miner.main.save_import")
@patch("goodread_miner.main.get_books", return_value=["/book/show/1", "/book/show/2"])
@patch("goodread_miner.main.scrape_book", return_value={"Title": "Book1"})
def test_main_file(mock_scrape, mock_get_books, mock_save, mock_file):
    test_argv = ["main.py", "--file", DATA_FILE]
    with patch.object(sys, "argv", test_argv):
        main_module.main()

        # Check open was called correctly
        mock_file.assert_called_once()
        args, kwargs = mock_file.call_args
        assert kwargs["file"] == DATA_FILE
        assert kwargs["encoding"] == "utf8"

        # get_books called 3 times (one per URL)
        assert mock_get_books.call_count == 3
        # scrape_book called 6 times (3 URLs × 2 books)
        assert mock_scrape.call_count == 6
        # save_import called once
        mock_save.assert_called_once()


# ------------------------
# Test --test argument
# ------------------------
@patch("goodread_miner.main.save_import")
@patch("goodread_miner.main.get_books", return_value=["/book/show/1"])
@patch("goodread_miner.main.scrape_book", return_value={"Title": "TestBook"})
def test_main_test(mock_scrape, mock_get_books, mock_save):
    test_argv = ["main.py", "--test"]
    with patch.object(sys, "argv", test_argv):
        main_module.main()
        mock_get_books.assert_called_once()
        mock_scrape.assert_called_once()
        mock_save.assert_called_once()

# ------------------------
# Test invalid arguments
# ------------------------
def test_main_invalid_args():
    test_argv = ["main.py", "--invalid"]
    with patch.object(sys, "argv", test_argv):
        with pytest.raises(SystemExit):
            main_module.main()

# ------------------------
# Test file with empty lines
# ------------------------
@patch("builtins.open", new_callable=mock_open, read_data=(
    "\nhttps://www.goodreads.com/list/show/195641.Books_to_read_on_Kashmir\n\n"
))
@patch("goodread_miner.main.save_import")
@patch("goodread_miner.main.get_books", return_value=["/book/show/1"])
@patch("goodread_miner.main.scrape_book", return_value={"Title": "Book1"})
def test_main_file_empty_lines(mock_scrape, mock_get_books, mock_save, mock_file):
    test_argv = ["main.py", "--file", DATA_FILE]
    with patch.object(sys, "argv", test_argv):
        main_module.main()

        # Check open was called correctly
        mock_file.assert_called_once()
        args, kwargs = mock_file.call_args
        assert kwargs["file"] == DATA_FILE
        assert kwargs["encoding"] == "utf8"

        # get_books called once
        assert mock_get_books.call_count == 1
        # scrape_book called once
        assert mock_scrape.call_count == 1
        # save_import called once
        mock_save.assert_called_once()

