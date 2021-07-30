def get_model_field_names(model):
    return [
        field.attname if hasattr(field, 'attname') else field.name
        for field in model._meta.concrete_fields
    ]

def load_dataframe_to_db(dataframe, model, output_database):
    model.objects.all().using(output_database).delete()

    model_field_names = get_model_field_names(model)

    reduced_dataframe = dataframe.reset_index()[model_field_names]

    print(reduced_dataframe)

    try:
        model.objects.bulk_create(
            [model(**vals) for vals in reduced_dataframe.to_dict('records')]
        )
    except:
        for vals in reduced_dataframe.to_dict('records'):
            try:
                model.objects.get_or_create(**vals)
            except Exception as e:
                print(vals)
                raise e


