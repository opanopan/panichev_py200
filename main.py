from datetime import datetime
from typing import Optional, overload


class TimeDelta:
    """Класс для хранения времени без привязки к дате"""

    def __init__(self, days: Optional[int] = None, months: Optional[int] = None, years: Optional[int] = None):
        self.days, self.months, self.years = days, months, years


class Date:
    """Класс для работы с датами"""

    YEAR = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    L_YEAR = (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

    @overload
    def __init__(self, day: int, month: int, year: int):
        """Создание даты из трех чисел"""

    @overload
    def __init__(self, date: str):
        """Создание даты из строки формата dd.mm.yyyy"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], str):
            dt = args[0].split(".")
            self.day, self.month, self.year = int(dt[0]), int(dt[1]), int(dt[2])

        elif len(args) == 3:
            for a in args:
                if not isinstance(a, int):
                    raise ValueError("Значения должны быть integer.")

            self.day = int(args[0])
            self.month = int(args[1])
            self.year = int(args[2])

        else:
            raise ValueError("Expected one string or three integers.")

        if not self.is_valid_date():
            raise ValueError("Incorrect date: %s" % self.__str__())

    def __str__(self) -> str:
        """Возвращает дату в формате dd.mm.yyyy"""
        result = f"{self.day:02d}.{self.month:02d}.{self.year:04d}"
        return result

    def __repr__(self) -> str:
        """Возвращает дату в формате Date(day, month, year)"""
        return f"Date({self.day}, {self.month}, {self.year})"

    @staticmethod
    def is_leap_year(year: int) -> bool:
        """Проверяет, является ли год високосным"""
        return not (year % 4 != 0 or (year % 100 == 0 and year % 400 != 0))

    @classmethod
    def get_max_day(cls, month: int, year: int) -> int:
        """Возвращает максимальное количество дней в месяце для указанного года"""
        if cls.is_leap_year(year):
            return cls.L_YEAR[month - 1]
        else:
            return cls.YEAR[month - 1]

    def is_valid_date(self):
        """Проверяет, является ли дата корректной"""
        return 0 <= self.year <= 3000 and \
               0 < self.month <= 12 and \
               0 < self.day <= self.get_max_day(self.month, self.year)

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, value: int):
        """value от 1 до 31. Проверять значение и корректность даты"""
        if value > 0 and value <= 31:
            self._day = value
        else:
            raise ValueError("День должен быть в промежутке между 1 и 31.")

    @property
    def month(self):
        return self._month

    @month.setter
    def month(self, value: int):
        """value от 1 до 12. Проверять значение и корректность даты"""
        if value > 0 and value <= 12:
            self._month = value
        else:
            raise ValueError("Месяц должен быть в промежутке от 1 до 12.")

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value: int):
        """value от 1 до ... . Проверять значение и корректность даты"""
        if value >= 0 and value <= 3000:
            self._year = value
        else:
            raise ValueError("Мы умеем работать с годом от 1 до 3000")

    def __sub__(self, other: "Date") -> int:
        """Разница между датой self и other (-)"""
        return self.days_count(self.day, self.month, self.year) - self.days_count(other.day, other.month, other.year)

    def days_count(self, day: int, month: int, year: int):
        """Возвращает количество дней от рождества Христова"""
        sm = 0
        for i in range(year):
            if Date.is_leap_year(i):
                sm += 366
            else:
                sm += 365

        for i in range(1, month):
            sm += Date.get_max_day(i, year)

        sm += day

        return sm

    def date_from_days(self, days: int) -> []:
        """Принимает количество дней от рождества Христова, возвращает дату"""
        sm = prevsm = month = 0
        for i in range(3000):
            if sm >= days:
                year = i - 1
                break

            prevsm = sm
            if Date.is_leap_year(i):
                sm += 366
            else:
                sm += 365

        else:
            raise ValueError("Мы не умеем обрабатывать даты, большие 3000 лет.")

        days -= prevsm

        sm = 0
        for i in range(1, 13):
            if sm >= days:
                month = i - 1
                break

            prevsm = sm
            sm += Date.get_max_day(i, year)
            month = i

        day = days - prevsm
        return day, month, year

    def __add__(self, other: TimeDelta) -> "Date":
        """Складывает self и некий timedeltа. Возвращает НОВЫЙ инстанс Date, self не меняет (+)"""
        if not isinstance(other, TimeDelta):
            raise ValueError("Class TimeDelta incorrect")
        years_from_month = (other.months + self.month) // 12
        int_month = (other.months + self.month) % 12
        int_year = other.years + self.year + years_from_month
        days_sum = self.days_count(self.day, int_month, int_year) + other.days

        new_day, new_mon, new_year = self.date_from_days(days_sum)

        return Date(new_day, new_mon, new_year)

    def __iadd__(self, other: TimeDelta) -> "Date":
        """Добавляет к self некий timedelta меняя сам self (+=)"""
        if not isinstance(other, TimeDelta):
            raise ValueError("Class TimeDelta incorrect")
        years_from_month = (other.months + self.month) // 12
        self.month = (other.months + self.month) % 12
        self.year = other.years + self.year + years_from_month

        days_sum = self.days_count(self.day, self.month, self.year) + other.days

        return self.date_from_days(days_sum)
