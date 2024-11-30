import datetime

def convert_to_date(date_str):
    """
    Converts a date string in the format 'DD-MM-YYYY' to a datetime.date object.

    Args:
        date_str: The date string to convert.

    Returns:
        A datetime.date object representing the date.

    Raises:
        ValueError: If the date string is not in the correct format.
    """

    try:
        day, month, year = map(int, date_str.split('-'))
        return datetime.date(year, month, day)
    except ValueError:
        raise ValueError("Invalid date format. Please use DD-MM-YYYY format.")