import traceback
import pandas as pd

def get_model_field_names(model):
    return [
        field.attname if hasattr(field, 'attname') else field.name
        for field in model._meta.concrete_fields
    ]

def load_dataframe_to_db(dataframe, model, output_database):
    print(model)

    model.objects.using(output_database).all().delete()

    model_field_names = get_model_field_names(model)
    dataframe_columns = dataframe.columns

    reduced_columns = [column for column in dataframe_columns if column in model_field_names]

    reduced_dataframe = dataframe[reduced_columns]

    try:
        model.objects.bulk_create(
            [model(**vals) for vals in reduced_dataframe.to_dict('records')]
        )
    except:
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', 1000)

        print("Error loading {} ".format(model))
        print(reduced_dataframe)
        traceback.print_exc()

        for vals in reduced_dataframe.to_dict('records'):
            try:
                model.objects.get_or_create(**vals)
            except Exception as e:
                print(vals)
                raise e