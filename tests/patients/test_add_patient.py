import pytest
import string
import random

from faker import Faker
from src.routes.endpoint_patients import EndpointPatients
from src.assertions.status_code_assertions import AssertionStatusCode
from utils.logger_helpers import log_request_response
from src.routes.request import OpenMrsRequest
from src.resources.payloads.payload_create_patients import PayloadCreatePatients

fake = Faker()

@pytest.mark.negative
@pytest.mark.high
def test_creacion_paciente_sin_autorizacion():
    payload = PayloadCreatePatients.build_payload_create_patient_with_identifier_defined()
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, {}, payload)
    log_request_response(endpoint, response, {})
    AssertionStatusCode.assert_status_code_is_error(response)

@pytest.mark.negative
@pytest.mark.high
def test_creacion_paciente_con_token_invalido():
    auth_headers = {'Authorization': 'Basic token_invalido'}
    payload = PayloadCreatePatients.build_payload_create_patient_with_identifier_defined()
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, auth_headers, payload)
    log_request_response(endpoint, response, auth_headers)
    AssertionStatusCode.assert_status_code_is_error(response)

@pytest.mark.functional
@pytest.mark.high
def test_creacion_paciente_exitosa_con_todos_campos_obligatorios(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload = PayloadCreatePatients.build_payload_create_patient_with_all_fields_mandatory(headers)
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_201(response)
    created_patients.append(response.json())

@pytest.mark.functional
@pytest.mark.medium
def test_creacion_paciente_exitosa_con_segundo_nombre(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload = PayloadCreatePatients.build_payload_create_patient(headers)
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_201(response)
    created_patients.append(response.json())

@pytest.mark.negative
@pytest.mark.high
def test_creacion_paciente_sin_nombre(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload = PayloadCreatePatients.build_payload_create_patient_without_give_name(headers)
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_400(response)
    assert response.json()["error"]['fieldErrors']['names[0].givenName'][0][
               "message"] == "You must define the Given Name"

@pytest.mark.functional
@pytest.mark.low
def test_creacion_paciente_sin_segundo_nombre(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload = PayloadCreatePatients.build_payload_create_patient_without_middle_name(headers)
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_201(response)
    created_patients.append(response.json())

@pytest.mark.negative
@pytest.mark.high
def test_creacion_paciente_sin_apellido(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload = PayloadCreatePatients.build_payload_create_patient_without_family_name(headers)
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_201(response)
    created_patients.append(response.json())

@pytest.mark.boundary
@pytest.mark.low
def test_creacion_paciente_con_nombre_con_50_caracteres(setup_add_patient):
    headers, created_patients = setup_add_patient
    caracteres_validos = string.ascii_letters
    data_random = ''.join(random.choices(caracteres_validos, k=50))
    payload = PayloadCreatePatients.build_payload_create_patient_custom(headers, data_random)
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_201(response)
    created_patients.append(response.json())


@pytest.mark.boundary
@pytest.mark.low
def test_creacion_paciente_con_nombre_con_51_caracteres(setup_add_patient):
    headers, created_patients = setup_add_patient
    caracteres_validos = string.ascii_letters
    data_random = ''.join(random.choices(caracteres_validos, k=51))
    payload = PayloadCreatePatients.build_payload_create_patient_custom(headers, data_random)
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_400(response)

@pytest.mark.boundary
@pytest.mark.low
def test_creacion_paciente_con_segundo_nombre_con_50_caracteres(setup_add_patient):
    headers, created_patients = setup_add_patient
    caracteres_validos = string.ascii_letters
    data_random = ''.join(random.choices(caracteres_validos, k=50))
    payload = PayloadCreatePatients.build_payload_create_patient_custom(headers, "Juan", data_random)
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_201(response)
    created_patients.append(response.json())

@pytest.mark.boundary
@pytest.mark.low
def test_creacion_paciente_con_segundo_nombre_con_51_caracteres(setup_add_patient):
    headers, created_patients = setup_add_patient
    caracteres_validos = string.ascii_letters
    data_random = ''.join(random.choices(caracteres_validos, k=51))
    payload = PayloadCreatePatients.build_payload_create_patient_custom(headers, "Juan", data_random)
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_400(response)

@pytest.mark.boundary
@pytest.mark.low
def test_creacion_paciente_con_apellido_con_50_caracteres(setup_add_patient):
    headers, created_patients = setup_add_patient
    caracteres_validos = string.ascii_letters
    data_random = ''.join(random.choices(caracteres_validos, k=50))
    payload = PayloadCreatePatients.build_payload_create_patient_custom(headers, "Juan", "perez", data_random)
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_201(response)
    created_patients.append(response.json())

@pytest.mark.boundary
@pytest.mark.low
def test_creacion_paciente_con_apellido_con_51_caracteres(setup_add_patient):
    headers, created_patients = setup_add_patient
    caracteres_validos = string.ascii_letters
    data_random = ''.join(random.choices(caracteres_validos, k=51))
    payload = PayloadCreatePatients.build_payload_create_patient_custom(headers, "Juan", "perez", data_random)
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_400(response)

@pytest.mark.negative
@pytest.mark.low
def test_verificar_error_con_first_name_con_caracteres_especiales(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload = PayloadCreatePatients.build_payload_create_patient_custom(
        headers,
        fake.bothify(text='?' * fake.random_int(min=2, max=50), letters='!#$%&/()=?¿¡°|@€*+-_'))
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    created_patients.append(response.json())
    AssertionStatusCode.assert_status_code_400(response)

@pytest.mark.negative
@pytest.mark.low
def test_verificar_error_con_first_name_con_caracteres_numericos(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload = PayloadCreatePatients.build_payload_create_patient_custom(
        headers,
        fake.numerify(text='#' * fake.random_int(min=2, max=50)))
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    created_patients.append(response.json())
    AssertionStatusCode.assert_status_code_400(response)

@pytest.mark.negative
@pytest.mark.low
def test_verificar_error_con_middle_name_con_caracteres_especiales(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload = PayloadCreatePatients.build_payload_create_patient_custom(
        headers,
        None,
        fake.bothify(text='?' * fake.random_int(min=2, max=50), letters='!#$%&/()=?¿¡°|@€*+-_'))
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    created_patients.append(response.json())
    AssertionStatusCode.assert_status_code_400(response)

@pytest.mark.negative
@pytest.mark.low
def test_verificar_error_con_middle_name_con_caracteres_numericos(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload = PayloadCreatePatients.build_payload_create_patient_custom(
        headers,
        None,
        fake.numerify(text='#' * fake.random_int(min=2, max=50)))
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    created_patients.append(response.json())
    AssertionStatusCode.assert_status_code_400(response)

@pytest.mark.negative
@pytest.mark.low
def test_verificar_error_con_last_name_con_caracteres_especiales(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload = PayloadCreatePatients.build_payload_create_patient_custom(
        headers,
        None,
        None,
        fake.bothify(text='?' * fake.random_int(min=2, max=50), letters='!#$%&/()=?¿¡°|@€*+-_'))
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    created_patients.append(response.json())
    AssertionStatusCode.assert_status_code_400(response)

@pytest.mark.negative
@pytest.mark.low
def test_verificar_error_con_last_name_con_caracteres_numericos(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload = PayloadCreatePatients.build_payload_create_patient_custom(
        headers,
        None,
        None,
        fake.numerify(text='#' * fake.random_int(min=2, max=50)))
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    created_patients.append(response.json())
    AssertionStatusCode.assert_status_code_400(response)

@pytest.mark.functional
@pytest.mark.medium
def test_verificar_crear_paciente_con_genero_masculino(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload = PayloadCreatePatients.build_payload_create_patient(headers, "M")
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_201(response)
    assert response.json()['person']['gender'] == "M"
    created_patients.append(response.json())

@pytest.mark.functional
@pytest.mark.medium
def test_verificar_crear_paciente_con_genero_femenino(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload = PayloadCreatePatients.build_payload_create_patient(headers, "F")
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_201(response)
    assert response.json()['person']['gender'] == "F"
    created_patients.append(response.json())

@pytest.mark.functional
@pytest.mark.medium
def test_verificar_crear_paciente_con_genero_otro(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload = PayloadCreatePatients.build_payload_create_patient(headers, "O")
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_201(response)
    assert response.json()['person']['gender'] == "O"
    created_patients.append(response.json())

@pytest.mark.functional
@pytest.mark.medium
def test_verificar_crear_paciente_con_genero_desconocido(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload = PayloadCreatePatients.build_payload_create_patient(headers, "U")
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_201(response)
    assert response.json()['person']['gender'] == "U"
    created_patients.append(response.json())

@pytest.mark.negative
@pytest.mark.medium
def test_verificar_error_de_creacion_de_paciente_sin_genero(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload = PayloadCreatePatients.build_payload_create_patient_without_gender(headers)
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_400(response)
    assert response.json()["error"]['fieldErrors']['gender'][0]["message"] == "Please select a gender"

@pytest.mark.functional
@pytest.mark.high
def test_creacion_paciente_con_fecha_de_nacimiento_conocida_exitosa(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload = PayloadCreatePatients.build_payload_create_patient(headers, None, False)
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_201(response)
    assert response.json()['person']['birthdate'] is not None
    created_patients.append(response.json())

@pytest.mark.negative
@pytest.mark.medium
def test_creacion_paciente_con_formato_fecha_invalido_DD_MM_YY(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload = PayloadCreatePatients.build_payload_create_patient_without_format_birthdate(headers, "15-08-1990")
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_400(response)
    assert "yyyy-MM-dd'T'HH:mm:ss.SSSZ => Invalid format" in response.json()["error"]["message"]

@pytest.mark.functional
@pytest.mark.high
def test_creacion_paciente_con_fecha_de_nacimiento_null_exitosa(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload = PayloadCreatePatients.build_payload_create_patient(headers, "M", True)
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_201(response)
    assert response.json()['person']['birthdate'] is None
    created_patients.append(response.json())

@pytest.mark.negative
@pytest.mark.low
def test_Verificar_error_de_creacion_con_fecha_de_nacimiento_muy_antigua(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload = PayloadCreatePatients.build_payload_create_patient_custom(headers, "M", None, None, None, "1885-01-01")
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_400(response)
    assert response.json()['error']['fieldErrors']['birthdate'][0]["message"] == "Nonsensical date, please check."
    created_patients.append(response.json())

@pytest.mark.negative
@pytest.mark.low
def test_Verificar_error_de_creacion_con_fecha_de_nacimiento_futura(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload = PayloadCreatePatients.build_payload_create_patient_custom(headers, "M", None, None, None, "2030-01-01")
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_400(response)
    assert response.json()['error']['fieldErrors']['birthdate'][0]["message"] == "Cannot be a date in the future"
    created_patients.append(response.json())

@pytest.mark.negative
@pytest.mark.low
def test_Verificar_error_de_creacion_con_fecha_de_nacimiento_inválida(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload = PayloadCreatePatients.build_payload_create_patient_custom(headers, "M", None, None, None, "2000-01-56")
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_400(response)

@pytest.mark.functional
@pytest.mark.high
def test_creacion_paciente_con_direccion_exitosa(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload = PayloadCreatePatients.build_payload_create_patient_with_optional_fields(headers)
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_201(response)
    assert response.json()["person"]['preferredAddress']['display'] is not None
    created_patients.append(response.json())

@pytest.mark.negative
@pytest.mark.low
def test_creacion_paciente_con_direccion_mas_de_250_caracteres(setup_add_patient):
    headers, created_patients = setup_add_patient
    caracteres_validos = string.ascii_letters
    data_random = ''.join(random.choices(caracteres_validos, k=300))
    payload = PayloadCreatePatients.build_payload_create_patient_with_optional_fields(headers, data_random)
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_400(response)
    assert "This value exceeds the maximum length" in \
           response.json()["error"]['fieldErrors']['addresses[0].address1'][0]["message"]
    created_patients.append(response.json())

@pytest.mark.functional
@pytest.mark.medium
def test_creacion_paciente_con_pais_exitosa(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload = PayloadCreatePatients.build_payload_create_patient_with_optional_fields(headers, None, fake.country())
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_201(response)
    created_patients.append(response.json())

@pytest.mark.negative
@pytest.mark.low
def test_creacion_paciente_con_pais_con_mas_de_250_caracteres(setup_add_patient):
    headers, created_patients = setup_add_patient
    caracteres_validos = string.ascii_letters
    data_random = ''.join(random.choices(caracteres_validos, k=300))
    payload = PayloadCreatePatients.build_payload_create_patient_with_optional_fields(headers, None, data_random)
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_400(response)
    assert "This value exceeds the maximum length" in \
           response.json()["error"]['fieldErrors']['addresses[0].country'][0]["message"]
    created_patients.append(response.json())

@pytest.mark.functional
@pytest.mark.medium
def test_creacion_paciente_con_ciudad_exitosa(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload = PayloadCreatePatients.build_payload_create_patient_with_optional_fields(headers, None, None, fake.city())
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_201(response)
    created_patients.append(response.json())

@pytest.mark.negative
@pytest.mark.low
def test_creacion_paciente_con_ciudad_con_mas_de_250_caracteres(setup_add_patient):
    headers, created_patients = setup_add_patient
    caracteres_validos = string.ascii_letters
    data_random = ''.join(random.choices(caracteres_validos, k=300))
    payload = PayloadCreatePatients.build_payload_create_patient_with_optional_fields(headers, None, None, data_random)
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_400(response)
    assert "This value exceeds the maximum length" in \
           response.json()["error"]['fieldErrors']['addresses[0].cityVillage'][0]["message"]
    created_patients.append(response.json())

@pytest.mark.functional
@pytest.mark.medium
def test_creacion_paciente_con_provincia_exitosa(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload = PayloadCreatePatients.build_payload_create_patient_with_optional_fields(headers, None, None, None, fake.state())
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_201(response)
    created_patients.append(response.json())

@pytest.mark.negative
@pytest.mark.low
def test_creacion_paciente_con_provincia_con_mas_de_250_caracteres(setup_add_patient):
    headers, created_patients = setup_add_patient
    caracteres_validos = string.ascii_letters
    data_random = ''.join(random.choices(caracteres_validos, k=300))
    payload = PayloadCreatePatients.build_payload_create_patient_with_optional_fields(headers, None, None, None,
                                                                                      data_random)
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_400(response)
    assert "This value exceeds the maximum length" in \
           response.json()["error"]['fieldErrors']['addresses[0].stateProvince'][0]["message"]
    created_patients.append(response.json())

@pytest.mark.functional
@pytest.mark.medium
def test_creacion_paciente_con_provincia_exitosa(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload = PayloadCreatePatients.build_payload_create_patient_with_optional_fields(headers, None, None, None, None, fake.postcode())
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_201(response)
    created_patients.append(response.json())

@pytest.mark.negative
@pytest.mark.low
def test_creacion_paciente_con_codigo_postal_muy_largo(setup_add_patient):
    headers, created_patients = setup_add_patient
    caracteres_validos = string.ascii_letters
    data_random = ''.join(random.choices(caracteres_validos, k=100))
    payload = PayloadCreatePatients.build_payload_create_patient_with_optional_fields(headers, None, None, None,
                                                                                      None, data_random)
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_400(response)
    assert "This value exceeds the maximum length" in \
           response.json()["error"]['fieldErrors']['addresses[0].postalCode'][0]["message"]
    created_patients.append(response.json())

@pytest.mark.functional
@pytest.mark.medium
def test_creacion_paciente_con_telefono_exitoso(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload = PayloadCreatePatients.build_payload_create_patient_with_telephone_fields(headers)
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_201(response)
    assert response.json()["person"]['attributes'][0]['display'] is not None
    created_patients.append(response.json())

@pytest.mark.negative
@pytest.mark.medium
def test_creacion_paciente_con_telefono_con_letras(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload = PayloadCreatePatients.build_payload_create_patient_with_telephone_fields(headers, fake.word())
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_400(response)
    created_patients.append(response.json())

@pytest.mark.negative
@pytest.mark.medium
def test_creacion_paciente_con_telefono_con_caracteres_especiales(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload = PayloadCreatePatients.build_payload_create_patient_with_telephone_fields(headers, fake.bothify(text='?' * fake.random_int(min=2, max=10), letters='!#$%&/()=?¿¡°|@€*+-_'))
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_400(response)
    created_patients.append(response.json())

@pytest.mark.negative
@pytest.mark.low
def test_creacion_paciente_con_telefono_con_muy_largo(setup_add_patient):
    headers, created_patients = setup_add_patient
    caracteres_validos = string.ascii_letters
    data_random = ''.join(random.choices(caracteres_validos, k=300))
    payload = PayloadCreatePatients.build_payload_create_patient_with_telephone_fields(headers, data_random)
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_500(response)
    assert "Data too long for column 'value" in \
           response.json()["error"]["message"]
    created_patients.append(response.json())

@pytest.mark.negative
@pytest.mark.medium
def test_creacion_paciente_sin_campo_identificadores(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload = PayloadCreatePatients.build_payload_create_patient_with_out_identifier()
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_400(response)
    assert "[Some required properties are missing: identifiers]" in response.json()["error"]["message"]

@pytest.mark.negative
@pytest.mark.low
def test_creacion_paciente_con_campo_identificadores_con_attributo_identificador_incorrecto(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload = PayloadCreatePatients.build_payload_create_patient_with_identifiers_custom(headers,"1312321")
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_400(response)
    assert "Invalid check digit for identifier" in response.json()["error"]["globalErrors"][0]["code"]

@pytest.mark.negative
@pytest.mark.low
def test_creacion_paciente_con_campo_identificadores_con_attributo_identifierType_incorrecto(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload = PayloadCreatePatients.build_payload_create_patient_with_identifiers_custom(headers,None,"1312321")
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_400(response)

@pytest.mark.negative
@pytest.mark.low
def test_creacion_paciente_con_campo_identificadores_con_attributo_location_incorrecto(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload = PayloadCreatePatients.build_payload_create_patient_with_identifiers_custom(headers, None, None, "1312321")
    endpoint = EndpointPatients.patient()
    response = OpenMrsRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers)
    AssertionStatusCode.assert_status_code_400(response)
