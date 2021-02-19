# Unit tests
import pytest

from main import Date
from main import TimeDelta


@pytest.mark.parametrize(("day", "month", "year"), [
    (31, 12, 1),
    (29, 2, 2020),
    (1, 1, 0),
    (13, 12, 3000)])
def test_create_date(day, month, year):
    date = Date(day, month, year)
    assert (date.day, date.month, date.year) == (day, month, year)


@pytest.mark.parametrize("date, exp_day, exp_month, exp_year", [
    ("31.12.0001", 31, 12, 1),
    ("29.02.1996", 29, 2, 1996),
    ("01.01.3000", 1, 1, 3000)])
def test_create_str_date(date, exp_day, exp_month, exp_year):
    date = Date(date)
    assert (date.day, date.month, date.year) == (exp_day, exp_month, exp_year)


@pytest.mark.parametrize(("day", "month", "year"), [
    (32, 12, 1),
    (30, 2, 1),
    ("a", 12, 1),
    (-1, 12, 1),
    (31, 9, 1),
    (0, 12, 1),
    (1, 0, 0),
    (None, 12, 1),
    (31.3, 8, 1),
    (3, 13, 1),
    (13, "b", 1),
    (13, -1, 1),
    (31, None, 1),
    (3, 0, 1),
    (29, 2, 2019),
    (2, 12, -1),
    (32, 12, "year"),
    (32, 12, None),
    (13, 12, 3001)])
def test_create_wrong_date(day, month, year):
    with pytest.raises(ValueError):
        date = Date(day, month, year)


@pytest.mark.parametrize("date", [
    "32.12.1",
    "aa.aaaa.aa",
    "1.0.1",
    "1,1,2020",
    "28,02,2021",
    "29.02.2021",
    12,
    "12.-1.1222"
])
def test_create_str_wrong_date(date):
    with pytest.raises(ValueError):
        date = Date(date)


@pytest.mark.parametrize("date", [

])
def test__str__fun(date):
    a = Date.__