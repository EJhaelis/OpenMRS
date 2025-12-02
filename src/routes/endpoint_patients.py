from src.routes.endpoint import Endpoint
from utils.config import BASE_URL

class EndpointPatients:

    @classmethod
    def patient(cls):
        return f"{BASE_URL}{Endpoint.BASE_PATIENT.value}"

    @staticmethod
    def build_url_patient_code(base, patient_code):
        return f"{BASE_URL}{base.format(uuid=patient_code)}"

    @classmethod
    def code(cls, patient_code):
        return cls.build_url_patient_code(Endpoint.BASE_PATIENT_BY_UUID.value, patient_code)

    @classmethod
    def patients_with_code_and_params(cls, patient_code, validate: bool = False, **params):
        if validate and not patient_code:
            raise ValueError("`patient_code` no puede ser vacío")
        base_url = cls.build_url_patient_code(Endpoint.BASE_PATIENT_BY_UUID.value, patient_code)
        if params:
            query_string = "&".join([f"{key}={value}" for key, value in params.items()])
            return f"{base_url}?{query_string}"
        return base_url

    @classmethod
    def generate_identifier(cls):
        return f"{BASE_URL}{Endpoint.BASE_GENERATE_IDGEN_ID.value}"

    @classmethod
    def patients_with_params(cls,**params):
        base_url = f"{BASE_URL}{Endpoint.BASE_PATIENT.value}"
        if params:
            query_string = "&".join([f"{key}={value}" for key, value in params.items()])
            return f"{base_url}?{query_string}"
        return base_url
