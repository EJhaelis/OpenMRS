from enum import Enum


class Endpoint(Enum):
    BASE_PATIENT = "/ws/rest/v1/patient"
    BASE_PATIENT_BY_UUID = "/ws/rest/v1/patient/{uuid}"
    BASE_GENERATE_IDGEN_ID = "/ws/rest/v1/idgen/nextIdentifier?source=1"
