from second_eye_api.migrate_from_external_db.transform.utils import *

def replace_broken_function_component_task_id_to_task_id_with_minus_one(function_components, tasks):
    valid_task_ids = tasks['id']
    replace_column_values_with_minus_one_if_not_in_valid_list(
        dataframe=function_components,
        column_name="task_id",
        valid_list=valid_task_ids
    )

def propagate_state_category_id_into_function_components(function_components, states):
    state_id_to_category_id_mapping = states[["id", "category_id"]].rename(columns={"id": "state_id", "category_id": "state_category_id"})

    return function_components.merge(
        state_id_to_category_id_mapping,
        how="left",
        on="state_id",
        suffixes=(None, ""),
    )

def propagate_function_component_kind_function_points_into_function_component(function_components, function_component_kinds):
    function_components_kinds_id_to_function_points_mapping = function_component_kinds[["id", "function_points"]].rename(
        columns={"id": "kind_id", "function_points": "kind_function_points"}
    )

    return function_components.merge(
        function_components_kinds_id_to_function_points_mapping,
        how="left",
        on="kind_id",
        suffixes=(None, ""),
    )

def calculate_function_components_function_points_using_count_and_kind_function_points_inplace(function_components):
    function_components['function_points'] = function_components['count'] * function_components['kind_function_points']
