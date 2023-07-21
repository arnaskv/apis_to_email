from apis_to_email import check_email
from apis_to_email import check_api
import pytest


def main():
    test_check_api()
    test_check_api()


def test_check_email():
    with pytest.raises(SystemExit):
        check_email("edmund@gmailcom")
        check_email("ed123gmail.com")
        check_email("myemail")


def test_check_api():
    with pytest.raises(SystemExit):
        check_api("guard")
        check_api("lastfm")
