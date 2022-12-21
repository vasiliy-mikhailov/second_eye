import cubista
import time

class DataSource:
    def __init__(self, tables):
        self.tables = {type(table): table for table in tables}

        self.set_data_source_for_tables()
        self.check_references_raise_exception_otherwise()
        self.evaluate_tables()

    def set_data_source_for_tables(self):
        tables = self.tables
        for _, table in tables.items():
            table.data_source = self

    def check_references_raise_exception_otherwise(self):
        tables = self.tables
        for _, table in tables.items():
            table.check_references_raise_exception_otherwise()

    def get_fields_to_evaluate(self, limited_fields_to_evaluate=None):
        tables = self.tables
        result = {}

        for _, table in tables.items():
            fields_to_evaluate = table.get_fields_to_evaluate(limited_fields_to_evaluate=limited_fields_to_evaluate)

            for fields_to_evaluate in fields_to_evaluate:
                result[fields_to_evaluate] = table

        return result

    def evaluate_tables(self):
        fields_to_evaluate = self.get_fields_to_evaluate()
        tables_to_evaluate = set(list(fields_to_evaluate.values()))

        table_statistics = {}

        while len(fields_to_evaluate) > 0:
            for table_object in tables_to_evaluate:
                start = time.time()
                table_object.evaluate()
                end = time.time()
                duration = end - start

                if table_object not in table_statistics:
                    table_statistics[table_object] = 0

                table_statistics[table_object] = table_statistics[table_object] + duration

            not_evaluated_fields = self.get_fields_to_evaluate()

            if len(fields_to_evaluate) == len(not_evaluated_fields):
                raise cubista.CannotEvaluateFields("{}".format(", ".join([str(field) for field in not_evaluated_fields])))

            fields_to_evaluate = not_evaluated_fields
            tables_to_evaluate = set(list(fields_to_evaluate.values()))

        # for table_object, duration in dict(sorted(table_statistics.items(), key=lambda item: item[1], reverse=True)).items():
        #     print("{} {}".format(duration, table_object))