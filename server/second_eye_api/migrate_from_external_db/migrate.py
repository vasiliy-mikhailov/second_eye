from .extract import Extractor
from .transform import Transformer
from .load import Loader
from second_eye_api.interactors.team_load_output_maker import make_team_load_outputs

def migrate(get_input_connection, output_database, settings):
    print("extract")
    extractor = Extractor(get_connection=get_input_connection, settings=settings)
    input_data = extractor.extract()

    print("transform")
    transformer = Transformer(input_data=input_data, settings=settings)
    output_data = transformer.transform()

    print("load")
    loader = Loader(output_data=output_data, output_database=output_database)
    loader.load()

    print("make outputs")
    make_team_load_outputs(output_data=output_data, output_database=output_database)

    print("done")