import pytest

from faker import Faker

from conftest import auth_headers
from src.routes.endpoint_patients import EndpointPatients
from src.assertions.status_code_assertions import AssertionStatusCode
from utils.logger_helpers import log_request_response
from src.routes.request import OpenMrsRequest
from src.resources.payloads.payload_create_patients import PayloadCreatePatients
fake = Faker()

@pytest.mark.negative
@pytest.mark.high
def test_eliminacion_paciente_sin_autorizacion(auth_headers):
    payload = PayloadCreatePatients.build_payload_create_patient(auth_headers)
    endpoint_create = EndpointPatients.patient()
    create_response = OpenMrsRequest.post(endpoint_create, auth_headers, payload)
    log_request_response(endpoint_create, create_response, auth_headers)
    AssertionStatusCode.assert_status_code_201(create_response)
    patient_uuid = create_response.json().get("uuid")
    delete_endpoint = EndpointPatients.patients_with_code_and_params(patient_code=patient_uuid, purge="true")
    delete_response = OpenMrsRequest.delete(delete_endpoint, {})
    log_request_response(delete_endpoint, delete_response, {})
    AssertionStatusCode.assert_status_code_401(delete_response)

@pytest.mark.negative
@pytest.mark.high
def test_eliminacion_paciente_con_token_invalido():
    patient_uuid = fake.pystr(min_chars=8, max_chars=12)
    auth_headers={'Authorization': 'Basic token_invalido'}
    delete_endpoint = EndpointPatients.patients_with_code_and_params(patient_code=patient_uuid, purge="true")
    delete_response = OpenMrsRequest.delete(delete_endpoint, auth_headers)
    log_request_response(delete_endpoint, delete_response, auth_headers)
    AssertionStatusCode.assert_status_code_401(delete_response)
    assert "User is not logged" in delete_response.json()["error"]['message']

@pytest.mark.functional
@pytest.mark.high
def test_eliminacion_paciente_exitosa(auth_headers):
    payload = PayloadCreatePatients.build_payload_create_patient(auth_headers)
    endpoint = EndpointPatients.patient()
    create_response = OpenMrsRequest.post(endpoint, auth_headers, payload)
    log_request_response(endpoint, create_response, auth_headers)
    AssertionStatusCode.assert_status_code_201(create_response)

    patient_uuid = create_response.json().get("uuid")
    delete_endpoint = EndpointPatients.patients_with_code_and_params(patient_code=patient_uuid, purge="true")
    delete_response = OpenMrsRequest.delete(delete_endpoint, auth_headers)
    log_request_response(delete_endpoint, delete_response, auth_headers)
    AssertionStatusCode.assert_status_code_204(delete_response)

@pytest.mark.negative
@pytest.mark.high
def test_eliminacion_paciente_con_campo_uuid_vacio(auth_headers):
    patient_uuid = ""
    with pytest.raises(ValueError):
        EndpointPatients.patients_with_code_and_params(patient_uuid, validate=True, purge="true")

@pytest.mark.negative
@pytest.mark.high
def test_eliminacion_paciente_inexistente(auth_headers):
    patient_uuid = fake.pystr(min_chars=8, max_chars=12)
    delete_endpoint = EndpointPatients.patients_with_code_and_params(patient_code=patient_uuid, purge="true")
    delete_response = OpenMrsRequest.delete(delete_endpoint, auth_headers)
    log_request_response(delete_endpoint, delete_response, auth_headers)
    AssertionStatusCode.assert_status_code_204(delete_response)

@pytest.mark.negative
@pytest.mark.high
def test_verificar_error_al_eliminar_paciente_ya_eliminado(auth_headers):
    payload = PayloadCreatePatients.build_payload_create_patient(auth_headers)
    endpoint = EndpointPatients.patient()
    create_response = OpenMrsRequest.post(endpoint, auth_headers, payload)
    log_request_response(endpoint, create_response, auth_headers)
    AssertionStatusCode.assert_status_code_201(create_response)
    patient_uuid = create_response.json().get("uuid")
    delete_endpoint = EndpointPatients.patients_with_code_and_params(patient_code=patient_uuid, purge="true")
    delete_response = OpenMrsRequest.delete(delete_endpoint, auth_headers)
    log_request_response(delete_endpoint, delete_response, auth_headers)
    AssertionStatusCode.assert_status_code_204(delete_response)
    second_delete_response = OpenMrsRequest.delete(delete_endpoint, auth_headers)
    log_request_response(delete_endpoint, second_delete_response, auth_headers)
    AssertionStatusCode.assert_status_code_204(second_delete_response)

