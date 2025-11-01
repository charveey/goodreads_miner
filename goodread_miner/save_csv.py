'''
This module handles the saving of all scrapped book data into a CSV file. 
'''
import csv
import os


def save_import(data: list[dict], filename: str = "data.csv") -> None:
    '''
    Saves the scraped book information into a CSV file.

    Args:
        data (list[dict]): A list of dictionaries containing book information.
        filename (str, optional): The name of the CSV file to save the data. Defaults to "data.csv".

    Example:
        >>> book_data = [
        ...     {"Title": "The Great Gatsby", "Author": "F. Scott Fitzgerald", ...},
        ...     # Add more book entries here...
        ... ]
        >>> save_import(book_data, "my_books.csv")

    Note:
        - The function creates or overwrites the specified CSV file.
        - The data should be a list of dictionaries, where each dictionary represents a book's details.
        - The fieldnames in the CSV file correspond to the keys in the dictionaries.
    '''
    data_fields: list[str] = [
        # List of field names (column headers) for the CSV
        # Customize this list based on your specific book data structure
        "Book Id",
        "Title",
        "Author",
        "Author l-f",
        "Additional Authors",
        "ISBN",
        "ISBN13",
        "My Rating",
        "Average Rating",
        "Publisher",
        "Binding",
        "Number of Pages",
        "Year Published",
        "Original Publication Year",
        "Date Read",
        "Date Added",
        "Bookshelves",
        "Bookshelves with positions",
        "Exclusive Shelf",
        "My Review",
        "Spoiler",
        "Private Notes",
        "Read Count",
        "Owned Copies",
    ]

    file_path: str = os.path.join(os.getcwd(), os.path.dirname(__file__), filename)
    with open(file_path, "w", newline="", encoding="utf8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data_fields)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
