import datetime
import unittest

import aind_behavior_services.utils as utils


class UtilsTest(unittest.TestCase):
    def test_datetime_fmt(self):
        tz_aware_utc = datetime.datetime(2023, 12, 25, 13, 30, 15, tzinfo=datetime.timezone.utc)
        tz_aware_pst = datetime.datetime(
            2023, 12, 25, 13, 30, 15, tzinfo=datetime.timezone(datetime.timedelta(hours=-8))
        )
        tz_naive = datetime.datetime(2023, 12, 25, 13, 30, 15)

        self.assertEqual(utils.format_datetime(tz_aware_utc), "2023-12-25T133015Z")
        self.assertEqual(utils.format_datetime(tz_aware_pst), "2023-12-25T133015-0800")
        self.assertEqual(utils.format_datetime(tz_naive, is_tz_strict=False), "2023-12-25T133015")
        self.assertRaises(ValueError, utils.format_datetime, tz_naive, is_tz_strict=True)


if __name__ == "__main__":
    unittest.main()
