from second_eye_api.migrate_from_external_db.transform import utils
import datetime

def test_is_in_in_chronon_bounds_takes_holidays_into_account():
    assert not utils.is_in_chronon_bounds(
        for_date=datetime.date(year=2021, month=12, day=9),
        sys_date=datetime.date(year=2022, month=1, day=23)
    )
    assert utils.is_in_chronon_bounds(
        for_date=datetime.date(year=2021, month=12, day=10),
        sys_date=datetime.date(year=2022, month=1, day=23)
    )
    assert utils.is_in_chronon_bounds(
        for_date=datetime.date(year=2021, month=12, day=30),
        sys_date=datetime.date(year=2022, month=1, day=23)
    )
    assert utils.is_in_chronon_bounds(
        for_date=datetime.date(year=2021, month=12, day=31),
        sys_date=datetime.date(year=2022, month=1, day=23)
    )
    assert utils.is_in_chronon_bounds(
        for_date=datetime.date(year=2022, month=1, day=1),
        sys_date=datetime.date(year=2022, month=1, day=23)
    )

def test_is_in_in_chronon_working_days_takes_holidays_into_account():
    assert not utils.is_in_chronon_working_days(
        for_date=datetime.date(year=2021, month=12, day=9),
        sys_date=datetime.date(year=2022, month=1, day=23)
    )
    assert utils.is_in_chronon_working_days(
        for_date=datetime.date(year=2021, month=12, day=10),
        sys_date=datetime.date(year=2022, month=1, day=23)
    )
    assert utils.is_in_chronon_working_days(
        for_date=datetime.date(year=2021, month=12, day=30),
        sys_date=datetime.date(year=2022, month=1, day=23)
    )
    assert not utils.is_in_chronon_working_days(
        for_date=datetime.date(year=2021, month=12, day=31),
        sys_date=datetime.date(year=2022, month=1, day=23)
    )
    assert not utils.is_in_chronon_working_days(
        for_date=datetime.date(year=2022, month=1, day=1),
        sys_date=datetime.date(year=2022, month=1, day=23)
    )

def test_working_days_in_month_occured_changes_on_consequent_assuming_date_change():
    july_2022 = datetime.date(year=2022, month=7, day=1)
    july_25_2022 = datetime.date(year=2022, month=7, day=25)
    working_days_in_month_occured_for_july_2022_as_of_july_25_2022 = utils.working_days_in_month_occured(for_date=july_2022, sys_date=july_25_2022)
    assert working_days_in_month_occured_for_july_2022_as_of_july_25_2022 == 17

    july_26_2022 = datetime.date(year=2022, month=7, day=26)
    working_days_in_month_occured_for_july_2022_as_of_july_26_2022 = utils.working_days_in_month_occured(for_date=july_2022, sys_date=july_26_2022)
    assert working_days_in_month_occured_for_july_2022_as_of_july_26_2022 == 18

def test_working_days_in_month_from_2018_to_2022():
    jan_2100 = datetime.date(year=2100, month=1, day=1)
    expected_data = {
        datetime.date(year=2017, month=1, day=1): 17,
        datetime.date(year=2017, month=2, day=1): 18,
        datetime.date(year=2017, month=3, day=1): 22,
        datetime.date(year=2017, month=4, day=1): 20,
        datetime.date(year=2017, month=5, day=1): 20,
        datetime.date(year=2017, month=6, day=1): 21,
        datetime.date(year=2017, month=7, day=1): 21,
        datetime.date(year=2017, month=8, day=1): 23,
        datetime.date(year=2017, month=9, day=1): 21,
        datetime.date(year=2017, month=10, day=1): 22,
        datetime.date(year=2017, month=11, day=1): 21,
        datetime.date(year=2017, month=12, day=1): 21,
        datetime.date(year=2018, month=1, day=1): 17,
        datetime.date(year=2018, month=2, day=1): 19,
        datetime.date(year=2018, month=3, day=1): 20,
        datetime.date(year=2018, month=4, day=1): 21,
        datetime.date(year=2018, month=5, day=1): 20,
        datetime.date(year=2018, month=6, day=1): 20,
        datetime.date(year=2018, month=7, day=1): 22,
        datetime.date(year=2018, month=8, day=1): 23,
        datetime.date(year=2018, month=9, day=1): 20,
        datetime.date(year=2018, month=10, day=1): 23,
        datetime.date(year=2018, month=11, day=1): 21,
        datetime.date(year=2018, month=12, day=1): 21,
        datetime.date(year=2019, month=1, day=1): 17,
        datetime.date(year=2019, month=2, day=1): 20,
        datetime.date(year=2019, month=3, day=1): 20,
        datetime.date(year=2019, month=4, day=1): 22,
        datetime.date(year=2019, month=5, day=1): 18,
        datetime.date(year=2019, month=6, day=1): 19,
        datetime.date(year=2019, month=7, day=1): 23,
        datetime.date(year=2019, month=8, day=1): 22,
        datetime.date(year=2019, month=9, day=1): 21,
        datetime.date(year=2019, month=10, day=1): 23,
        datetime.date(year=2019, month=11, day=1): 20,
        datetime.date(year=2019, month=12, day=1): 22,
        datetime.date(year=2020, month=1, day=1): 17,
        datetime.date(year=2020, month=2, day=1): 19,
        datetime.date(year=2020, month=3, day=1): 21,
        datetime.date(year=2020, month=4, day=1): 22,
        datetime.date(year=2020, month=5, day=1): 17,
        datetime.date(year=2020, month=6, day=1): 21,
        datetime.date(year=2020, month=7, day=1): 23,
        datetime.date(year=2020, month=8, day=1): 21,
        datetime.date(year=2020, month=9, day=1): 22,
        datetime.date(year=2020, month=10, day=1): 22,
        datetime.date(year=2020, month=11, day=1): 20,
        datetime.date(year=2020, month=12, day=1): 23,
        datetime.date(year=2021, month=1, day=1): 15,
        datetime.date(year=2021, month=2, day=1): 19,
        datetime.date(year=2021, month=3, day=1): 22,
        datetime.date(year=2021, month=4, day=1): 22,
        datetime.date(year=2021, month=5, day=1): 19,
        datetime.date(year=2021, month=6, day=1): 21,
        datetime.date(year=2021, month=7, day=1): 22,
        datetime.date(year=2021, month=8, day=1): 22,
        datetime.date(year=2021, month=9, day=1): 22,
        datetime.date(year=2021, month=10, day=1): 21,
        datetime.date(year=2021, month=11, day=1): 20,
        datetime.date(year=2021, month=12, day=1): 22,
        datetime.date(year=2022, month=1, day=1): 16,
        datetime.date(year=2022, month=2, day=1): 19,
        datetime.date(year=2022, month=3, day=1): 22,
        datetime.date(year=2022, month=4, day=1): 21,
        datetime.date(year=2022, month=5, day=1): 18,
        datetime.date(year=2022, month=6, day=1): 21,
        datetime.date(year=2022, month=7, day=1): 21,
        datetime.date(year=2022, month=8, day=1): 23,
        datetime.date(year=2022, month=9, day=1): 22,
        datetime.date(year=2022, month=10, day=1): 21,
        datetime.date(year=2022, month=11, day=1): 21,
        datetime.date(year=2022, month=12, day=1): 22,
    }

    for date, days in expected_data.items():
        assert days == utils.working_days_in_month_occured(for_date=date, sys_date=jan_2100)

def test_make_25_to_5_working_days_sliding_window_for_date_excludes_holidays():
    correct_working_days = {
        datetime.date(2021, 12, 9),
        datetime.date(2021, 12, 10),
        datetime.date(2021, 12, 13),
        datetime.date(2021, 12, 14),
        datetime.date(2021, 12, 15),
        datetime.date(2021, 12, 16),
        datetime.date(2021, 12, 17),
        datetime.date(2021, 12, 20),
        datetime.date(2021, 12, 21),
        datetime.date(2021, 12, 22),
        datetime.date(2021, 12, 23),
        datetime.date(2021, 12, 24),
        datetime.date(2021, 12, 27),
        datetime.date(2021, 12, 28),
        datetime.date(2021, 12, 29),
        datetime.date(2021, 12, 30),
        datetime.date(2022, 1, 10),
        datetime.date(2022, 1, 11),
        datetime.date(2022, 1, 12),
        datetime.date(2022, 1, 13)
    }

    sys_date = datetime.date(year=2022, month=1, day=20)

    calculated_working_days = utils.make_chronon_dates(
        sys_date=sys_date
    )

    assert len(calculated_working_days) == 20
    assert correct_working_days == calculated_working_days

def test_is_in_chronon_bounds_makes_correct_results():
    correct_working_days = {
        datetime.date(2021, 12, 9),
        datetime.date(2021, 12, 10),
        datetime.date(2021, 12, 13),
        datetime.date(2021, 12, 14),
        datetime.date(2021, 12, 15),
        datetime.date(2021, 12, 16),
        datetime.date(2021, 12, 17),
        datetime.date(2021, 12, 20),
        datetime.date(2021, 12, 21),
        datetime.date(2021, 12, 22),
        datetime.date(2021, 12, 23),
        datetime.date(2021, 12, 24),
        datetime.date(2021, 12, 27),
        datetime.date(2021, 12, 28),
        datetime.date(2021, 12, 29),
        datetime.date(2021, 12, 30),
        datetime.date(2022, 1, 10),
        datetime.date(2022, 1, 11),
        datetime.date(2022, 1, 12),
        datetime.date(2022, 1, 13)
    }

    correct_non_working_days = {
        datetime.date(year=2021, month=12, day=31),
        datetime.date(year=2022, month=1, day=1)
    }

    sys_date = datetime.date(year=2022, month=1, day=20)

    for correct_working_day in correct_working_days:
        assert utils.is_in_chronon_bounds(for_date=correct_working_day, sys_date=sys_date)

    for correct_non_working_day in correct_non_working_days:
        assert utils.is_in_chronon_bounds(for_date=correct_non_working_day, sys_date=sys_date)

def test_is_in_chronon_working_days_makes_correct_results():
    correct_working_days = {
        datetime.date(2021, 12, 9),
        datetime.date(2021, 12, 10),
        datetime.date(2021, 12, 13),
        datetime.date(2021, 12, 14),
        datetime.date(2021, 12, 15),
        datetime.date(2021, 12, 16),
        datetime.date(2021, 12, 17),
        datetime.date(2021, 12, 20),
        datetime.date(2021, 12, 21),
        datetime.date(2021, 12, 22),
        datetime.date(2021, 12, 23),
        datetime.date(2021, 12, 24),
        datetime.date(2021, 12, 27),
        datetime.date(2021, 12, 28),
        datetime.date(2021, 12, 29),
        datetime.date(2021, 12, 30),
        datetime.date(2022, 1, 10),
        datetime.date(2022, 1, 11),
        datetime.date(2022, 1, 12),
        datetime.date(2022, 1, 13)
    }

    incorrect_working_days = {
        datetime.date(year=2022, month=1, day=20),
        datetime.date(year=2022, month=1, day=1)
    }

    sys_date = datetime.date(year=2022, month=1, day=20)

    for correct_working_day in correct_working_days:
        assert utils.is_in_chronon_bounds(for_date=correct_working_day, sys_date=sys_date)

    for incorrect_working_day in incorrect_working_days:
        assert not utils.is_in_chronon_working_days(for_date=incorrect_working_day, sys_date=sys_date)

def test_chronon_start_date_makes_correct_results():
    sys_date = datetime.date(year=2022, month=1, day=20)

    correct_start_date = datetime.date(2021, 12, 9)

    calculated_start_date = utils.chronon_start_date(
        sys_date=sys_date
    )

    assert correct_start_date == calculated_start_date

def test_chronon_end_date_makes_correct_results():
    sys_date = datetime.date(year=2022, month=1, day=20)

    correct_end_date = datetime.date(2022, 1, 13)

    calculated_end_date = utils.chronon_end_date(
        sys_date=sys_date
    )

    assert correct_end_date == calculated_end_date