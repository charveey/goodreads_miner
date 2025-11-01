from unittest.mock import mock_open, patch, MagicMock
from goodread_miner import save_import

# Sample data
sample_data = [
    {
        "Book Id": "1",
        "Title": "Book One",
        "Author": "Author A",
        "Author l-f": "A, Author",
        "Additional Authors": "",
        "ISBN": '="1234567890"',
        "ISBN13": '="9781234567897"',
        "My Rating": "",
        "Average Rating": 4.5,
        "Publisher": "Publisher A",
        "Binding": "Hardcover",
        "Number of Pages": 300,
        "Year Published": 2020,
        "Original Publication Year": 2019,
        "Date Read": "2025-11-01",
        "Date Added": "2025-11-01",
        "Bookshelves": "imported",
        "Bookshelves with positions": "",
        "Exclusive Shelf": "imported",
        "My Review": "",
        "Spoiler": "",
        "Private Notes": "",
        "Read Count": 1,
        "Owned Copies": 1,
    }
]

# ------------------------
# Test default filename
# ------------------------
@patch("builtins.open", new_callable=mock_open)
@patch("csv.DictWriter")
def test_save_import_default_filename(mock_csv_writer, mock_file):
    mock_writer_instance = MagicMock()
    mock_csv_writer.return_value = mock_writer_instance

    save_import(sample_data)

    # Check that open was called with default filename
    args, kwargs = mock_file.call_args
    assert "data.csv" in args[0]

    # Check that DictWriter wrote header and row
    mock_writer_instance.writeheader.assert_called_once()
    mock_writer_instance.writerow.assert_called_once_with(sample_data[0])

# ------------------------
# Test custom filename
# ------------------------
@patch("builtins.open", new_callable=mock_open)
@patch("csv.DictWriter")
def test_save_import_custom_filename(mock_csv_writer, mock_file):
    mock_writer_instance = MagicMock()
    mock_csv_writer.return_value = mock_writer_instance

    save_import(sample_data, filename="custom_books.csv")

    args, kwargs = mock_file.call_args
    assert "custom_books.csv" in args[0]

    mock_writer_instance.writeheader.assert_called_once()
    mock_writer_instance.writerow.assert_called_once_with(sample_data[0])

# ------------------------
# Test empty data
# ------------------------
@patch("builtins.open", new_callable=mock_open)
@patch("csv.DictWriter")
def test_save_import_empty_data(mock_csv_writer, mock_file):
    mock_writer_instance = MagicMock()
    mock_csv_writer.return_value = mock_writer_instance

    save_import([])

    mock_writer_instance.writeheader.assert_called_once()
    # writerow should not be called
    mock_writer_instance.writerow.assert_not_called()
