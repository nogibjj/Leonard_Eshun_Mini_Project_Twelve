from app import convert_currency


def test_failed_connection():
    """Testing a nicely handled failed connection"""
    assert convert_currency(True)[1] == 500
    assert convert_currency(True)[0] == "Handled"


if __name__ == "__main__":
    test_failed_connection()
