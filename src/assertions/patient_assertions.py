from src.assertions.schema_assertions import AssertionSchemas

class AssertionPatients:
    MODULE = "patients"

    @staticmethod
    def assert_patient_create_output_schema(response):
        return AssertionSchemas().validate_json_schema(response, "patient_create_output_schema.json", AssertionPatients.MODULE)

    @staticmethod
    def assert_patient_get_output_schema(response):
        return AssertionSchemas().validate_json_schema(response, "patient_get_output_schema.json", AssertionPatients.MODULE)

    @staticmethod
    def assert_patient_update_output_schema(response):
        return AssertionSchemas().validate_json_schema(response, "patient_update_output_schema.json", AssertionPatients.MODULE)

    @staticmethod
    def assert_patient_search_output_schema(response):
        return AssertionSchemas.validate_json_schema(response,"patient_search_output_schema.json", AssertionPatients.MODULE)