def replace_column_values_with_minus_one_if_not_in_valid_list(dataframe, column_name, valid_list):
    dataframe.loc[~dataframe[column_name].isin(
        valid_list
    ), column_name] = -1