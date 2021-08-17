from second_eye_api.migrate_from_external_db.transform.utils import *

def replace_broken_project_team_positions_person_id_to_persons_id_with_minus_one(project_team_positions, persons):
    valid_person_ids = persons['id']
    replace_column_values_with_minus_one_if_not_in_valid_list(
        dataframe=project_team_positions,
        column_name="person_id",
        valid_list=valid_person_ids
    )