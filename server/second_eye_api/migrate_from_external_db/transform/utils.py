import pandas as pd
from .skill import Skill
import datetime
import calendar
from . import quarter

chronon_working_days_for_sys_date = {}
chronon_start_dates_for_sys_date = {}
chronon_end_dates_for_sys_date = {}
working_days_in_month_hash = {}

public_holidays = [
    datetime.date(year=2017, month=1, day=2),
    datetime.date(year=2017, month=1, day=3),
    datetime.date(year=2017, month=1, day=4),
    datetime.date(year=2017, month=1, day=5),
    datetime.date(year=2017, month=1, day=6),
    datetime.date(year=2017, month=2, day=23),
    datetime.date(year=2017, month=2, day=24),
    datetime.date(year=2017, month=3, day=8),
    datetime.date(year=2017, month=5, day=1),
    datetime.date(year=2017, month=5, day=8),
    datetime.date(year=2017, month=5, day=9),
    datetime.date(year=2017, month=6, day=12),
    datetime.date(year=2017, month=11, day=6),
    datetime.date(year=2018, month=1, day=1),
    datetime.date(year=2018, month=1, day=2),
    datetime.date(year=2018, month=1, day=3),
    datetime.date(year=2018, month=1, day=4),
    datetime.date(year=2018, month=1, day=5),
    datetime.date(year=2018, month=1, day=8),
    datetime.date(year=2018, month=2, day=23),
    datetime.date(year=2018, month=3, day=8),
    datetime.date(year=2018, month=3, day=9),
    datetime.date(year=2018, month=4, day=30),
    datetime.date(year=2018, month=5, day=1),
    datetime.date(year=2018, month=5, day=2),
    datetime.date(year=2018, month=5, day=9),
    datetime.date(year=2018, month=6, day=11),
    datetime.date(year=2018, month=6, day=12),
    datetime.date(year=2018, month=11, day=5),
    datetime.date(year=2018, month=12, day=31),
    datetime.date(year=2019, month=1, day=1),
    datetime.date(year=2019, month=1, day=2),
    datetime.date(year=2019, month=1, day=3),
    datetime.date(year=2019, month=1, day=4),
    datetime.date(year=2019, month=1, day=7),
    datetime.date(year=2019, month=1, day=8),
    datetime.date(year=2019, month=3, day=8),
    datetime.date(year=2019, month=5, day=1),
    datetime.date(year=2019, month=5, day=2),
    datetime.date(year=2019, month=5, day=3),
    datetime.date(year=2019, month=5, day=9),
    datetime.date(year=2019, month=5, day=10),
    datetime.date(year=2019, month=6, day=12),
    datetime.date(year=2019, month=11, day=4),
    datetime.date(year=2020, month=1, day=1),
    datetime.date(year=2020, month=1, day=2),
    datetime.date(year=2020, month=1, day=3),
    datetime.date(year=2020, month=1, day=6),
    datetime.date(year=2020, month=1, day=7),
    datetime.date(year=2020, month=1, day=8),
    datetime.date(year=2020, month=2, day=24),
    datetime.date(year=2020, month=3, day=9),
    datetime.date(year=2020, month=5, day=1),
    datetime.date(year=2020, month=5, day=4),
    datetime.date(year=2020, month=5, day=5),
    datetime.date(year=2020, month=5, day=11),
    datetime.date(year=2020, month=6, day=12),
    datetime.date(year=2020, month=11, day=4),
    datetime.date(year=2021, month=1, day=1),
    datetime.date(year=2021, month=1, day=4),
    datetime.date(year=2021, month=1, day=5),
    datetime.date(year=2021, month=1, day=6),
    datetime.date(year=2021, month=1, day=7),
    datetime.date(year=2021, month=1, day=8),
    datetime.date(year=2021, month=2, day=22),
    datetime.date(year=2021, month=2, day=23),
    datetime.date(year=2021, month=3, day=8),
    datetime.date(year=2021, month=5, day=3),
    datetime.date(year=2021, month=5, day=10),
    datetime.date(year=2021, month=6, day=14),
    datetime.date(year=2021, month=11, day=4),
    datetime.date(year=2021, month=11, day=5),
    datetime.date(year=2021, month=12, day=31),
    datetime.date(year=2022, month=1, day=3),
    datetime.date(year=2022, month=1, day=4),
    datetime.date(year=2022, month=1, day=5),
    datetime.date(year=2022, month=1, day=6),
    datetime.date(year=2022, month=1, day=7),
    datetime.date(year=2022, month=2, day=23),
    datetime.date(year=2022, month=3, day=7),
    datetime.date(year=2022, month=3, day=8),
    datetime.date(year=2022, month=5, day=2),
    datetime.date(year=2022, month=5, day=3),
    datetime.date(year=2022, month=5, day=9),
    datetime.date(year=2022, month=5, day=10),
    datetime.date(year=2022, month=6, day=13),
    datetime.date(year=2022, month=11, day=4),
    datetime.date(year=2023, month=1, day=2),
    datetime.date(year=2023, month=1, day=3),
    datetime.date(year=2023, month=1, day=4),
    datetime.date(year=2023, month=1, day=5),
    datetime.date(year=2023, month=1, day=6),
    datetime.date(year=2023, month=2, day=23),
    datetime.date(year=2023, month=2, day=24),
    datetime.date(year=2023, month=3, day=8),
    datetime.date(year=2023, month=5, day=9),
    datetime.date(year=2023, month=1, day=12),
    datetime.date(year=2023, month=10, day=6),
]

public_non_standard_working_days = [
    datetime.date(year=2018, month=4, day=28),
    datetime.date(year=2018, month=6, day=9),
    datetime.date(year=2018, month=12, day=30),
    datetime.date(year=2020, month=2, day=20),
    datetime.date(year=2021, month=2, day=20),
    datetime.date(year=2022, month=3, day=5),
]

def is_holiday(date):
    global public_holidays

    return (date.weekday() in [5, 6] or date in public_holidays) and date not in public_non_standard_working_days

def subtract_working_days(from_date, number_of_working_days):
    probe_date = from_date
    work_days_counter = 0
    one_day = datetime.timedelta(days=1)

    while work_days_counter < number_of_working_days or is_holiday(probe_date):
        if not is_holiday(date=probe_date):
            work_days_counter = work_days_counter + 1

        probe_date = probe_date - one_day

    return probe_date

def make_chronon_dates(sys_date):
    result = set()

    start_date = sys_date

    start_date = subtract_working_days(from_date=start_date, number_of_working_days=5)

    probe_date = start_date
    for i in range(0, 20):
        result.add(probe_date)
        probe_date = subtract_working_days(from_date=probe_date, number_of_working_days=1)

    return result

def is_in_chronon_working_days(for_date, sys_date):
    global chronon_working_days_for_sys_date

    if sys_date not in chronon_working_days_for_sys_date:
        window = make_chronon_dates(sys_date=sys_date)
        chronon_working_days_for_sys_date[sys_date] = window

    return for_date in chronon_working_days_for_sys_date[sys_date]

def is_in_chronon_bounds(for_date, sys_date):
    start_date = chronon_start_date(sys_date=sys_date)
    end_date = chronon_end_date(sys_date=sys_date)

    return for_date >= start_date and for_date <= end_date

def chronon_start_date(sys_date):
    global chronon_start_dates_for_sys_date

    if sys_date not in chronon_start_dates_for_sys_date:
        window = make_chronon_dates(sys_date=sys_date)
        start_date = min(window)
        chronon_start_dates_for_sys_date[sys_date] = start_date

    result = chronon_start_dates_for_sys_date[sys_date]

    return result

def chronon_end_date(sys_date):
    global chronon_end_dates_for_sys_date

    if sys_date not in chronon_end_dates_for_sys_date:
        window = make_chronon_dates(sys_date=sys_date)
        end_date = max(window)
        chronon_end_dates_for_sys_date[sys_date] = end_date

    result = chronon_end_dates_for_sys_date[sys_date]

    return result

def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + datetime.timedelta(n)

def working_days_in_month_occured(for_date, sys_date):
    global working_days_in_month_hash

    if sys_date not in working_days_in_month_hash:
        working_days_in_month_hash[sys_date] = {}

    if for_date not in working_days_in_month_hash[sys_date]:
        month_start_date = datetime.date(for_date.year, for_date.month, 1)
        month_start_date_limited_by_sys_date = min(month_start_date, sys_date)

        month_end_date = datetime.date(for_date.year, for_date.month, calendar.monthrange(for_date.year, for_date.month)[1])
        month_end_date_limited_by_sys_date = min(month_end_date, sys_date)

        working_days = 0

        for day in date_range(month_start_date_limited_by_sys_date, month_end_date_limited_by_sys_date):
            if not is_holiday(date=day):
                working_days = working_days + 1

        working_days_in_month_hash[sys_date][for_date] = working_days

    return working_days_in_month_hash[sys_date][for_date]

def get_current_year():
    today = datetime.date.today()

    return today.year

def get_current_quarter_id():
    today = datetime.date.today()
    return get_year_and_quarter_number(date=today)

def get_quarter_number(date):
    return ((date.month - 1) // 3 + 1)

def get_year_and_quarter_number(date):
    return date.year * 10 + get_quarter_number(date=date)

def get_quarter_key(date):
    year = date.year
    quarter_number = get_quarter_number(date=date)
    quarter_roman_number = quarter.Quarter.QUARTER_ROMAN_NUMBERS[quarter_number]
    return "{}-{}".format(year, quarter_roman_number)

def get_quarter_start_date(date):
    quarter_number = get_quarter_number(date=date)
    return datetime.date(year=date.year, month=((quarter_number - 1) * 3) + 1, day=1)

def get_quarter_end_date(date):
    quarter_number = get_quarter_number(date=date)
    one_day = datetime.timedelta(days=1)
    first_day_of_next_quarter = datetime.date(year=date.year + 3 * quarter_number // 12, month=3 * quarter_number % 12 + 1, day=1)
    return first_day_of_next_quarter - one_day

def is_in_current_quarter(for_date):
    quarter_number = get_year_and_quarter_number(date=for_date)
    today = datetime.date.today()
    current_quarter_number = get_year_and_quarter_number(date=today)

    return quarter_number == current_quarter_number

def calculate_entities_actual_capacity_by_task_time_sheets_filtering_by_skill_and_summing_up_by_column(
    entities,
    task_time_sheets,
    sum_up_by_column,
    skill
):
    time_spent_last_period_column_names = {
        Skill.ANALYSIS: "analysis_time_spent_last_period",
        Skill.DEVELOPMENT: "development_time_spent_last_period",
        Skill.TESTING: "testing_time_spent_last_period"
    }

    actual_capacity_column_names = {
        Skill.ANALYSIS: "actual_analysis_capacity",
        Skill.DEVELOPMENT: "actual_development_capacity",
        Skill.TESTING: "actual_testing_capacity"
    }

    time_spent_last_period_column_name = "time_spent_last_period" if not skill else time_spent_last_period_column_names[
        skill
    ]

    tasks_time_sheets_filtered_by_skill = task_time_sheets if not skill else task_time_sheets[
        task_time_sheets["skill_id"] == skill
    ]

    task_time_sheets_behind = tasks_time_sheets_filtered_by_skill[
        tasks_time_sheets_filtered_by_skill.apply(lambda x: is_in_chronon_bounds(for_date=x["date"]), axis=1)
    ].copy()

    tasks_time_sheets_aggregated_by_sum_up_column = task_time_sheets_behind.groupby(
        [sum_up_by_column]
    ).agg({
        "time_spent": "sum"
    }).reset_index().rename(
        columns={
            sum_up_by_column: "id",
            "time_spent": time_spent_last_period_column_name
        },
    )

    entities = entities.merge(
        tasks_time_sheets_aggregated_by_sum_up_column,
        how="left",
        on="id",
        suffixes=(False, ""),
    )

    entities[time_spent_last_period_column_name].fillna(0, inplace=True)

    actual_capacity_column_name = "actual_change_request_capacity" if not skill else actual_capacity_column_names[
        skill
    ]

    number_of_work_days_in_period = 20

    entities[actual_capacity_column_name] = entities[time_spent_last_period_column_name] / number_of_work_days_in_period

    return entities

def calculate_entities_actual_change_request_capacity_by_task_time_sheets_summing_up_by_column(
        entities,
        task_time_sheets,
        sum_up_by_column
):
    return calculate_entities_actual_capacity_by_task_time_sheets_filtering_by_skill_and_summing_up_by_column(
        entities=entities,
        task_time_sheets=task_time_sheets,
        sum_up_by_column=sum_up_by_column,
        skill=None
    )

def calculate_entities_actual_analysis_capacity_by_task_time_sheets_summing_up_by_column(
        entities,
        task_time_sheets,
        sum_up_by_column
):
    return calculate_entities_actual_capacity_by_task_time_sheets_filtering_by_skill_and_summing_up_by_column(
        entities=entities,
        task_time_sheets=task_time_sheets,
        sum_up_by_column=sum_up_by_column,
        skill=Skill.ANALYSIS
    )


def calculate_entities_actual_development_capacity_by_task_time_sheets_summing_up_by_column(
        entities,
        task_time_sheets,
        sum_up_by_column
):
    return calculate_entities_actual_capacity_by_task_time_sheets_filtering_by_skill_and_summing_up_by_column(
        entities=entities,
        task_time_sheets=task_time_sheets,
        sum_up_by_column=sum_up_by_column,
        skill=Skill.DEVELOPMENT
    )


def calculate_entities_actual_testing_capacity_by_task_time_sheets_summing_up_by_column(
        entities,
        task_time_sheets,
        sum_up_by_column
):
    return calculate_entities_actual_capacity_by_task_time_sheets_filtering_by_skill_and_summing_up_by_column(
        entities=entities,
        task_time_sheets=task_time_sheets,
        sum_up_by_column=sum_up_by_column,
        skill=Skill.TESTING
    )

def normalize(x, min_x, max_x):
    if not pd.isnull(min_x) and not pd.isnull(max_x) and min_x != max_x:
        return (x - min_x) / (max_x - min_x)
    else:
        return 0
