# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from datetime import datetime
from dateutil.relativedelta import relativedelta


class AcademicTerm():
    WINTER = 1
    SPRING = 2
    SUMMER = 3
    AUTUMN = 4

    QTR_NAMES = {WINTER: 'WIN', SPRING: 'SPR', SUMMER: 'SUM', AUTUMN: 'AUT'}

    def __init__(self, year=None, quarter=None, date=None):
        self._date = date
        if (year is not None and quarter is not None):
            self.year = year
            self.quarter = quarter
        else:
            self.current()

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, AcademicTerm):
            return False
        return self.year == __o.year and self.quarter == __o.quarter

    def current(self):
        if self._date is None:
            self._date = datetime.now()
        year, quarter = self._term_from_datetime(self._date)
        self.year = year
        self.quarter = quarter
        return self

    def next(self):
        if self.quarter == self.AUTUMN:
            self.year = self.year + 1
            self.quarter = self.WINTER
        else:
            self.quarter = self.quarter + 1
        return self

    def previous(self):
        if self.quarter == self.WINTER:
            self.year = self.year - 1
            self.quarter = self.AUTUMN
        else:
            self.quarter = self.quarter - 1
        return self

    @property
    def name(self):
        return '{}{}'.format(self.QTR_NAMES.get(self.quarter), self.year)

    def _autumn_start_date(self, year):
        sept = datetime(year, 9, 24)
        return sept + relativedelta(weekday=2)  # last Wednesday of Sept

    def _winter_start_date(self, year):
        jan = datetime(year, 1, 2)
        # if Jan 1 is Sunday or Monday, start on Jan 3
        if jan.weekday() in [0, 1]:
            return jan.replace(day=3)
        return jan + relativedelta(weekday=0)  # first Monday after Jan 1

    def _spring_start_date(self, year):
        start = self._winter_start_date(year) + relativedelta(weeks=11, days=1)
        return start + relativedelta(weekday=0)  # second Monday after winter

    def _summer_start_date(self, year):
        start = self._spring_start_date(year) + relativedelta(weeks=11, days=1)
        return start + relativedelta(weekday=0)  # second Monday after spring

    def _term_from_datetime(self, dt: datetime):
        terms = [self._winter_start_date(dt.year),
                 self._spring_start_date(dt.year),
                 self._summer_start_date(dt.year),
                 self._autumn_start_date(dt.year)]

        quarter = 0
        while quarter < len(terms) and dt >= terms[quarter]:
            quarter += 1

        return dt.year, quarter if (quarter > 0) else self.AUTUMN
