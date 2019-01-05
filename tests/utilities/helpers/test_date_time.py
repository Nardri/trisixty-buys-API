"""Test the date time method"""

from datetime import datetime
from api.utilities.helpers.date_time import date_time

fmt = '%Y-%m-%d %H:%M:%S'
fmt1 = '%Y-%m-%d %H:%M:%S %Z%z'


class TestDateTime:
    """Tests the custom datetime class"""

    def test_the_date_time_method_succeeds(self):
        """Tests the date_time.date_time method"""

        date = date_time.date_time(2018, 12, 6, 8, 54, 32, format_=fmt1)

        assert str(date) == '2018-12-06 09:54:32 WAT+0100'

    def test_the_time_method_with_sub_succeeds(self):
        """Tests the date_time.time method"""

        date = date_time.time(
            manipulate=True, manipulation_type='SUB', format_=fmt, hours=1)
        dt = round(datetime.strptime(date, fmt).timestamp())

        assert dt is not None

    def test_the_time_method_with_add_succeeds(self):
        """Tests the date_time.time method"""

        date = date_time.time(
            manipulate=True, manipulation_type='ADD', format_=fmt, hours=1)

        dt = round(datetime.strptime(date, fmt).timestamp())

        assert dt is not None
