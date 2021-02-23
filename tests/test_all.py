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


@pytest.mark.parametrize(("date", "int_day", "int_month", "int_year"), [
    ("01.01.0001", 1, 1, 1),
    ("29.02.0020", 29, 2, 20),
    ("01.01.0000", 1, 1, 0),
    ("13.12.3000", 13, 12, 3000)])
def test__str__(date, int_day, int_month, int_year):
    dt = Date(int_day, int_month, int_year)
    assert date == dt.__str__()


@pytest.mark.parametrize(("date", "int_day", "int_month", "int_year"), [
    ("Date(1, 1, 1)", 1, 1, 1),
    ("Date(29, 2, 20)", 29, 2, 20),
    ("Date(1, 1, 0)", 1, 1, 0),
    ("Date(13, 12, 3000)", 13, 12, 3000)])
def test__repr__(date, int_day, int_month, int_year):
    dt = Date(int_day, int_month, int_year)
    assert date == dt.__repr__()


@pytest.mark.parametrize(("year", "result"), [
    (2020, True),
    (2021, False),
    (2000, True),
    (1900, False)])
def test__leap__fun(year, result):
    assert result == Date.is_leap_year(year)


@pytest.mark.parametrize(("month", "year", "result"), [
    (1, 2020, 31),
    (2, 2020, 29),
    (2, 2021, 28),
    (12, 2020, 31),
    (2, 1900, 28),
    (3, 22, 31),
    (4, 33, 30),
    (5, 44, 31),
    (6, 55, 30),
    (7, 166, 31),
    (8, 177, 31),
    (9, 1188, 30),
    (10, 2220, 31),
    (11, 3120, 30)])
def test__max_day_fun(month, year, result):
    assert result == Date.get_max_day(month, year)


@pytest.mark.parametrize(("date1", "date2", "result"), [
    ("01.12.2020", "01.12.2021", 365),
    ("01.12.2021", "01.12.2020", -365),
    ("01.12.2019", "01.12.2020", 366),
    ("01.12.2020", "01.12.2019", -366),
    ("01.12.2010", "01.12.2020", 3653),
    ("01.12.2020", "01.12.2010", -3653),
    ("31.07.2019", "31.08.2019", 31),
    ("31.08.2019", "31.07.2019", -31),
    ("10.07.2019", "11.07.2019", 1),
    ("31.07.2019", "31.07.2019", 0)
])
def test__sub__fun(date1, date2, result):
    dt1 = Date(date1)
    dt2 = Date(date2)
    assert result == dt2.__sub__(dt1)


@pytest.mark.parametrize(
    ("date", "delta_day", "delta_month", "delta_year", "delta_res", "res"),
    [("01.01.0001", 0, 0, 1, "01.01.0002", "01.01.0001"),
     ("01.01.2020", 0, 12, 0, "01.01.2021", "01.01.2020"),
     ("01.01.2020", 365, 0, 0, "31.12.2020", "01.01.2020"),
     ("01.01.2020", 365, 10, 10, "01.11.2031", "01.01.2020")
     ])
def test__add__(date, delta_day, delta_month, delta_year, delta_res, res):
    dt = Date(date)
    td = TimeDelta(delta_day, delta_month, delta_year)
    assert Date(delta_res).__str__() == dt.__add__(td).__str__()
    assert dt.__str__() == res


@pytest.mark.parametrize(("date", "delta_day", "delta_month", "delta_year"),
                         [("01.01.2020", 365, 0, 1000),
                          ("01.01.1", 365, 10, 2999)])
def test__add_wrong(date, delta_day, delta_month, delta_year):
    with pytest.raises(ValueError):
        dt = Date(date)
        td = TimeDelta(delta_day, delta_month, delta_year)
        dt.__add__(td)


@pytest.mark.parametrize(("date", "trash"),
                         [("01.01.2020", 365),
                          ("01.01.1", "hey, get me a beer")])
def test__add_wrong_class(date, trash):
    with pytest.raises(ValueError):
        dt = Date(date)
        dt.__add__(trash)


@pytest.mark.parametrize(
    ("date", "delta_day", "delta_month", "delta_year", "res"),
    [("01.01.0001", 0, 0, 1, "01.01.0002"),
     ("01.01.2020", 0, 12, 0, "01.01.2021"),
     ("01.01.2020", 365, 0, 0, "31.12.2020"),
     ("01.01.2020", 365, 10, 10, "01.11.2031")
     ])
def test__add__(date, delta_day, delta_month, delta_year, res):
    dt = Date(date)
    td = TimeDelta(delta_day, delta_month, delta_year)
    dt.__iadd__(td)
    assert res == dt.__str__()


@pytest.mark.parametrize(("date", "trash"),
                         [("01.01.2020", 365),
                          ("01.01.1", "hey, give me another beer")])
def test__iadd_wrong_class(date, trash):
    with pytest.raises(ValueError):
        dt = Date(date)
        dt.__iadd__(trash)
