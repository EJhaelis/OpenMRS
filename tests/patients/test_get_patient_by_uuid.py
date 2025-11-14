import pytest

from faker import Faker
from src.routes.endpoint_patients import EndpointPatients
from src.assertions.status_code_assertions import AssertionStatusCode
from utils.logger_helpers import log_request_response
from src.routes.request import OpenMrsRequest
from src.resources.payloads.payload_create_patients import PayloadCreatePatients
fake = Faker()

@pytest.mark.functional
@pytest.mark.high
def test_busqueda_paciente_exitosa_por_uuid(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload_create_patient = PayloadCreatePatients.build_payload_create_patient(headers)
    endpoint_create_patient = EndpointPatients.patient()
    create_response = OpenMrsRequest.post(endpoint_create_patient, headers, payload_create_patient)
    log_request_response(endpoint_create_patient, create_response,headers)
    AssertionStatusCode.assert_status_code_201(create_response)

    options_code = create_response.json()["uuid"]

    endpoint = EndpointPatients.code(options_code)
    response = OpenMrsRequest.get(EndpointPatients.code(options_code), headers)
    AssertionStatusCode.assert_status_code_200(response)
    log_request_response(endpoint, response, headers)
    created_patients.append(create_response.json())

@pytest.mark.negative
@pytest.mark.medium
def test_busqueda_paciente_inexistente_por_uuid():
    options_code = "12345678-1234-1234-1234-1234567890ab"
    endpoint = EndpointPatients.code(options_code)
    response = OpenMrsRequest.get(EndpointPatients.code(options_code), {})
    AssertionStatusCode.assert_status_code_401(response)
    log_request_response(endpoint, response, {})

@pytest.mark.negative
@pytest.mark.high
def test_busqueda_paciente_por_uuid_sin_authorizacion(auth_headers):
    options_code = "12345678-1234-1234-1234-1234567890ab"
    endpoint = EndpointPatients.code(options_code)
    response = OpenMrsRequest.get(EndpointPatients.code(options_code), auth_headers)
    AssertionStatusCode.assert_status_code_404(response)
    log_request_response(endpoint, response, auth_headers)

@pytest.mark.negative
@pytest.mark.high
def test_busqueda_paciente_por_uuid_sin_authorizacion():
    options_code = "12345678-1234-1234-1234-1234567890ab"
    auth_headers={'Authorization': 'Basic token_invalido'}
    endpoint = EndpointPatients.code(options_code)
    response = OpenMrsRequest.get(EndpointPatients.code(options_code), auth_headers)
    AssertionStatusCode.assert_status_code_401(response)
    log_request_response(endpoint, response, auth_headers)
    assert "User is not logged" in response.json()["error"]['message']

@pytest.mark.functional
@pytest.mark.high
def test_busqueda_paciente_exitosa_por_identifier(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload_create_patient = PayloadCreatePatients.build_payload_create_patient(headers)
    endpoint_create_patient = EndpointPatients.patient()
    create_response = OpenMrsRequest.post(endpoint_create_patient, headers, payload_create_patient)
    log_request_response(endpoint_create_patient, create_response,headers)
    AssertionStatusCode.assert_status_code_201(create_response)

    identifier_code = payload_create_patient["identifiers"][0]["identifier"]

    endpoint = EndpointPatients.patients_with_params(q=identifier_code)
    response = OpenMrsRequest.get(endpoint, headers)
    AssertionStatusCode.assert_status_code_200(response)
    log_request_response(endpoint, response, headers)
    created_patients.append(create_response.json())

@pytest.mark.negative
@pytest.mark.medium
def test_busqueda_paciente_por_identifier_inexistente(setup_add_patient):
    headers, created_patients = setup_add_patient
    identifier_code = fake.pystr(min_chars=8, max_chars=12)
    endpoint = EndpointPatients.patients_with_params(q=identifier_code)
    response = OpenMrsRequest.get(endpoint, headers)
    AssertionStatusCode.assert_status_code_200(response)
    assert response.json()["results"] == []
    log_request_response(endpoint, response, headers)

@pytest.mark.functional
@pytest.mark.high
def test_busqueda_paciente_exitosa_por_nombre(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload_create_patient = PayloadCreatePatients.build_payload_create_patient(headers)
    endpoint_create_patient = EndpointPatients.patient()
    create_response = OpenMrsRequest.post(endpoint_create_patient, headers, payload_create_patient)
    log_request_response(endpoint_create_patient, create_response,headers)
    AssertionStatusCode.assert_status_code_201(create_response)

    given_name = payload_create_patient["person"]["names"][0]["givenName"]

    endpoint = EndpointPatients.patients_with_params(q=given_name)
    response = OpenMrsRequest.get(endpoint, headers)
    AssertionStatusCode.assert_status_code_200(response)
    log_request_response(endpoint, response, headers)
    created_patients.append(create_response.json())


@pytest.mark.negative
@pytest.mark.medium
def test_busqueda_paciente_por_nombre_inexistente(setup_add_patient):
    headers, created_patients = setup_add_patient
    query = "NombreInexistente"
    endpoint = EndpointPatients.patients_with_params(q=query)
    response = OpenMrsRequest.get(endpoint, headers)
    AssertionStatusCode.assert_status_code_200(response)
    assert response.json()["results"] == []
    log_request_response(endpoint, response, headers)

@pytest.mark.functional
@pytest.mark.high
def test_busqueda_paciente_exitosa_por_apellido(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload_create_patient = PayloadCreatePatients.build_payload_create_patient(headers)
    endpoint_create_patient = EndpointPatients.patient()
    create_response = OpenMrsRequest.post(endpoint_create_patient, headers, payload_create_patient)
    log_request_response(endpoint_create_patient, create_response,headers)
    AssertionStatusCode.assert_status_code_201(create_response)

    family_name = payload_create_patient["person"]["names"][0]["familyName"]

    endpoint = EndpointPatients.patients_with_params(q=family_name)
    response = OpenMrsRequest.get(endpoint, headers)
    AssertionStatusCode.assert_status_code_200(response)
    log_request_response(endpoint, response, headers)
    created_patients.append(create_response.json())

@pytest.mark.negative
@pytest.mark.medium
def test_busqueda_paciente_exitosa_por_apellido_inexistente(setup_add_patient):
    headers, created_patients = setup_add_patient
    family_name = "ApellidoInexistente"
    endpoint = EndpointPatients.patients_with_params(q=family_name)
    response = OpenMrsRequest.get(endpoint, headers)
    AssertionStatusCode.assert_status_code_200(response)
    assert response.json()["results"] == []
    log_request_response(endpoint, response, headers)

@pytest.mark.functional
@pytest.mark.high
def test_busqueda_varios_pacientes_exitosa(setup_add_patient):
    headers, created_patients = setup_add_patient
    endpoint_create_patient = EndpointPatients.patient()
    common_name = fake.first_name()

    payload_create_patient_one = PayloadCreatePatients.build_payload_create_patient_custom(headers, common_name)
    payload_create_patient_two = PayloadCreatePatients.build_payload_create_patient_custom(headers, common_name)

    create_response_one = OpenMrsRequest.post(endpoint_create_patient, headers, payload_create_patient_one)
    create_response_two = OpenMrsRequest.post(endpoint_create_patient, headers, payload_create_patient_two)

    log_request_response(endpoint_create_patient, create_response_one,headers)
    log_request_response(endpoint_create_patient, create_response_two,headers)
    AssertionStatusCode.assert_status_code_201(create_response_one)
    AssertionStatusCode.assert_status_code_201(create_response_two)

    endpoint = EndpointPatients.patients_with_params(q=common_name)
    response = OpenMrsRequest.get(endpoint, headers)
    AssertionStatusCode.assert_status_code_200(response)
    log_request_response(endpoint, response, headers)
    assert len(response.json()["results"]) >= 1

    created_patients.append(create_response_one.json())
    created_patients.append(create_response_two.json())