import pandas as pd
from second_eye_api.schema.skill import Skill

def replace_column_values_with_minus_one_if_not_in_valid_list(dataframe, column_name, valid_list):
    dataframe.loc[~dataframe[column_name].isin(
        valid_list
    ), column_name] = -1

def calculate_entities_time_left_by_tasks_time_left_filtering_by_skill_and_summing_up_by_column(
        entities,
        tasks,
        sum_up_by_column,
        skill
):
    time_left_column_names = {
        Skill.ANALYSIS: "analysis_time_left",
        Skill.DEVELOPMENT: "development_time_left",
        Skill.TESTING: "testing_time_left"
    }

    tasks_filtered_by_skill = tasks if not skill else tasks[tasks["skill_id"] == skill]

    time_left_column_name = "time_left" if not skill else time_left_column_names[skill]

    tasks_time_left_aggregated_by_column = tasks_filtered_by_skill.groupby(
        [sum_up_by_column]
    ).agg({
        "time_left": "sum"
    }).reset_index().rename(
        columns={
            sum_up_by_column: "id",
            "time_left": time_left_column_name
        },
    )

    entities = entities.merge(
        tasks_time_left_aggregated_by_column,
        how="left",
        on="id",
        suffixes=(False, ""),
    )

    entities[time_left_column_name].fillna(0, inplace=True)

    return entities

def calculate_entities_time_left_by_tasks_time_left_summing_up_by_column(entities, tasks, sum_up_by_column):
    return calculate_entities_time_left_by_tasks_time_left_filtering_by_skill_and_summing_up_by_column(
        entities=entities,
        tasks=tasks,
        sum_up_by_column=sum_up_by_column,
        skill=None
    )

def calculate_entities_analysis_time_left_by_tasks_time_left_summing_up_by_column(entities, tasks, sum_up_by_column):
    return calculate_entities_time_left_by_tasks_time_left_filtering_by_skill_and_summing_up_by_column(
        entities=entities,
        tasks=tasks,
        sum_up_by_column=sum_up_by_column,
        skill=Skill.ANALYSIS
    )

def calculate_entities_development_time_left_by_tasks_time_left_summing_up_by_column(entities, tasks, sum_up_by_column):
    return calculate_entities_time_left_by_tasks_time_left_filtering_by_skill_and_summing_up_by_column(
        entities=entities,
        tasks=tasks,
        sum_up_by_column=sum_up_by_column,
        skill=Skill.DEVELOPMENT
    )

def calculate_entities_testing_time_left_by_tasks_time_left_summing_up_by_column(entities, tasks, sum_up_by_column):
    return calculate_entities_time_left_by_tasks_time_left_filtering_by_skill_and_summing_up_by_column(
        entities=entities,
        tasks=tasks,
        sum_up_by_column=sum_up_by_column,
        skill=Skill.TESTING
    )

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

    number_of_days_in_period = 28
    look_behind = 7
    work_days = 5
    week_days = 7
    today = pd.to_datetime('today').normalize()
    start = today - pd.to_timedelta("{}day".format(number_of_days_in_period + look_behind))
    end = today - pd.to_timedelta("{}day".format(look_behind))

    tasks_time_sheets_filtered_by_skill = task_time_sheets if not skill else task_time_sheets[
        task_time_sheets["skill_id"] == skill
    ]

    task_time_sheets_behind = tasks_time_sheets_filtered_by_skill[
        (task_time_sheets["date"] >= start)
        & (task_time_sheets["date"] < end)
    ].copy()

    tasks_time_sheets_aggregated_by_company_id = task_time_sheets_behind.groupby(
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
        tasks_time_sheets_aggregated_by_company_id,
        how="left",
        on="id",
        suffixes=(False, ""),
    )

    entities[time_spent_last_period_column_name].fillna(0, inplace=True)

    actual_capacity_column_name = "actual_change_request_capacity" if not skill else actual_capacity_column_names[
        skill
    ]

    entities[actual_capacity_column_name] = entities[time_spent_last_period_column_name] / number_of_days_in_period * week_days / work_days

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
