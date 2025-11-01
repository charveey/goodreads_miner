import os
import tempfile
import csv
from unittest.mock import mock_open, patch, MagicMock
from goodreads_miner import save_import

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

def read_csv(filepath: str) -> list[dict]:
    """Utility function to read back a CSV file into a list of dicts."""
    with open(filepath, encoding="utf8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def test_save_import_creates_file():
    """It should create a CSV file with the correct name."""
    data = [{"Title": "Test Book", "Author": "Author Name"}]

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "output.csv")
        save_import(data, filename="output.csv", output_dir=tmpdir)

        assert os.path.exists(output_path), "CSV file should be created"


def test_save_import_writes_headers_and_rows():
    """It should write correct headers and include all book data."""
    data = [
        {"Title": "Book 1", "Author": "Author 1"},
        {"Title": "Book 2", "Author": "Author 2"},
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "books.csv")
        save_import(data, filename="books.csv", output_dir=tmpdir)

        rows = read_csv(filepath)
        assert len(rows) == 2
        assert rows[0]["Title"] == "Book 1"
        assert "Bookshelves" in rows[0]


def test_bookshelf_argument_is_applied():
    """It should populate the Bookshelves column with the provided value."""
    data = [{"Title": "Shelf Test", "Author": "Tester"}]

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "shelf.csv")
        save_import(data, filename="shelf.csv", bookshelf="to-read", output_dir=tmpdir)

        rows = read_csv(filepath)
        assert rows[0]["Bookshelves"] == "to-read"


def test_output_dir_is_created_if_missing():
    """It should create the output directory if it does not exist."""
    data = [{"Title": "AutoDir", "Author": "Bot"}]

    with tempfile.TemporaryDirectory() as tmpdir:
        target_dir = os.path.join(tmpdir, "new_folder")
        filepath = os.path.join(target_dir, "out.csv")

        save_import(data, filename="out.csv", output_dir=target_dir)
        assert os.path.exists(filepath), "Output directory should be auto-created"


def test_extra_fields_are_ignored():
    """It should ignore unexpected fields not defined in data_fields."""
    data = [{"Title": "Extra", "Author": "Someone", "RandomField": "ignored"}]

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "ignore.csv")
        save_import(data, filename="ignore.csv", output_dir=tmpdir)

        rows = read_csv(filepath)
        assert "RandomField" not in rows[0]
