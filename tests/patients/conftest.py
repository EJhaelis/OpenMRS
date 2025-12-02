import pytest

from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_patients import EndpointPatients
from src.routes.request import OpenMrsRequest
from utils.logger_helpers import log_request_response


@pytest.fixture(scope="function")
def setup_add_patient(auth_headers):
    created_patients = []
    yield auth_headers, created_patients

    for patient in created_patients:
        if 'uuid' in patient:
            delete_endpoint = EndpointPatients.patients_with_code_and_params(patient_code=patient['uuid'], purge="true")
            OpenMrsRequest.delete(delete_endpoint, auth_headers)
        else:
            print(f"La opción de producto no tiene 'code': {patient}")

def build_full_name(jsonModel) -> str:
    given_name = jsonModel["person"]["names"][0]["givenName"]
    middle_name = jsonModel["person"]["names"][0]["middleName"]
    family_name = jsonModel["person"]["names"][0]["familyName"]
    return given_name + " " + middle_name + " " + family_name


def create_patient(headers, payload_create):
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload_create)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_201(response)
    return response.json()