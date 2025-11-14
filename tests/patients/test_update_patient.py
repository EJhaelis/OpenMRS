import pytest
import string
import random

from faker import Faker
from src.routes.endpoint_patients import EndpointPatients
from src.assertions.status_code_assertions import AssertionStatusCode
from tests.patients.conftest import create_patient, build_full_name
from utils.logger_helpers import log_request_response
from src.routes.request import OpenMrsRequest
from src.resources.payloads.payload_update_patients import PayloadUpdatePatients
from src.resources.payloads.payload_create_patients import PayloadCreatePatients

fake = Faker()

@pytest.mark.negative
@pytest.mark.high
def test_actualizar_paciente_sin_autorizacion(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload_create = PayloadCreatePatients.build_payload_create_patient(headers)
    response_create_json = create_patient(headers, payload_create)
    patient_code = response_create_json["uuid"]
    payload_update = PayloadUpdatePatients.build_payload_update_patient_custom(patient_code, payload_create)
    endpoint_update = EndpointPatients.code(patient_code)
    response_update = OpenMrsRequest.post(endpoint_update,{} , payload_update)
    AssertionStatusCode.assert_status_code_401(response_update)
    log_request_response(endpoint_update, response_update, {})
    created_patients.append(response_update.json())

@pytest.mark.negative
@pytest.mark.high
def test_actualizar_paciente_con_token_invalido(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload_create = PayloadCreatePatients.build_payload_create_patient(headers)
    response_create_json = create_patient(headers, payload_create)
    patient_code = response_create_json["uuid"]
    payload_update = PayloadUpdatePatients.build_payload_update_patient_custom(patient_code, payload_create)
    endpoint_update = EndpointPatients.code(patient_code)
    auth_headers={'Authorization': 'Basic token_invalido'}
    response_update = OpenMrsRequest.post(endpoint_update,auth_headers , payload_update)
    AssertionStatusCode.assert_status_code_401(response_update)
    log_request_response(endpoint_update, response_update, auth_headers)
    created_patients.append(response_update.json())
    assert "User is not logged" in response_update.json()["error"]['message']

@pytest.mark.functional
@pytest.mark.high
def test_verificar_actualizacion_de_paciente_exitosa(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload_create = PayloadCreatePatients.build_payload_create_patient(headers)
    response_create_json = create_patient(headers, payload_create)
    patient_code = response_create_json["uuid"]
    payload_update = PayloadUpdatePatients.build_payload_update_patient_custom(patient_code, payload_create,fake.first_name(), fake.last_name())
    endpoint_update = EndpointPatients.code(patient_code)
    response_update = OpenMrsRequest.post(endpoint_update, headers, payload_update)
    response_update_json = response_update.json()
    AssertionStatusCode.assert_status_code_200(response_update)
    family_name_request = build_full_name(payload_update)
    family_name_updated = response_update_json["person"]["display"]
    assert family_name_updated == family_name_request
    log_request_response(endpoint_update, response_update, headers)
    created_patients.append(response_update.json())

@pytest.mark.negative
@pytest.mark.high
def test_actualizar_paciente_inexistente(setup_add_patient):
    headers, created_patients = setup_add_patient
    patient_code = str(fake.uuid4())
    payload_update = PayloadUpdatePatients.build_payload_update_invalid_patient(patient_code)
    endpoint_update = EndpointPatients.code(patient_code)
    response_update = OpenMrsRequest.post(endpoint_update, headers, payload_update)
    AssertionStatusCode.assert_status_code_is_error(response_update)
    log_request_response(endpoint_update, response_update, headers)

@pytest.mark.negative
@pytest.mark.high
def test_actualizar_paciente_con_campo_uuid_vacio(setup_add_patient):
    headers, created_patients = setup_add_patient
    patient_code = ""
    payload_create = PayloadCreatePatients.build_payload_create_patient(headers)
    payload_update = PayloadUpdatePatients.build_payload_update_patient_custom(patient_code, payload_create)
    with pytest.raises(ValueError):
        EndpointPatients.patients_with_code_and_params(patient_code, validate=True, purge="true")


@pytest.mark.negative
@pytest.mark.medium
def test_actualizar_paciente_con_campo_uuid_formato_incorrecto(setup_add_patient):
    headers, created_patients = setup_add_patient
    patient_code = "formato-incorrecto-no-uuid"
    payload_update = PayloadUpdatePatients.build_payload_update_invalid_patient(patient_code)
    endpoint_update = EndpointPatients.code(patient_code)
    response_update = OpenMrsRequest.post(endpoint_update, headers, payload_update)
    AssertionStatusCode.assert_status_code_is_error(response_update)
    log_request_response(endpoint_update, response_update, headers)

@pytest.mark.functional
@pytest.mark.medium
def test_actualizar_campo_first_name(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload_create = PayloadCreatePatients.build_payload_create_patient(headers)
    response_create_json = create_patient(headers, payload_create)
    patient_code = response_create_json["uuid"]
    payload_update = PayloadUpdatePatients.build_payload_update_patient_custom(patient_code, payload_create, fake.first_name_male())
    endpoint_update = EndpointPatients.code(patient_code)
    response_update = OpenMrsRequest.post(endpoint_update, headers, payload_update)
    response_update_json = response_update.json()
    AssertionStatusCode.assert_status_code_200(response_update)
    family_name_request = build_full_name(payload_update)
    family_name_updated = response_update_json["person"]["display"]
    assert family_name_updated == family_name_request
    log_request_response(endpoint_update, response_update, headers)
    created_patients.append(response_update.json())

@pytest.mark.negative
@pytest.mark.low
def test_verificar_error_al_actualizar_campo_first_name_vacio(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload_create = PayloadCreatePatients.build_payload_create_patient(headers)
    response_create_json = create_patient(headers, payload_create)
    patient_code = response_create_json["uuid"]
    payload_update = PayloadUpdatePatients.build_payload_update_patient_custom(patient_code, payload_create, "")
    endpoint_update = EndpointPatients.code(patient_code)
    response_update = OpenMrsRequest.post(endpoint_update, headers, payload_update)
    AssertionStatusCode.assert_status_code_is_error(response_update)
    log_request_response(endpoint_update, response_update, headers)

@pytest.mark.negative
@pytest.mark.low
@pytest.mark.xfail(reason="Known issue BUG: Validación faltante para caracteres especiales en campo 'First name'", run=True)
def test_verificar_error_al_editar_campo_first_name_con_caracteres_especiales(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload_create = PayloadCreatePatients.build_payload_create_patient(headers)
    response_create_json = create_patient(headers, payload_create)
    patient_code = response_create_json["uuid"]
    payload_update = PayloadUpdatePatients.build_payload_update_patient_custom(patient_code, payload_create, "@@@###$$$")
    endpoint_update = EndpointPatients.code(patient_code)
    response_update = OpenMrsRequest.post(endpoint_update, headers, payload_update)
    AssertionStatusCode.assert_status_code_is_error(response_update)
    log_request_response(endpoint_update, response_update, headers)

@pytest.mark.negative
@pytest.mark.low
@pytest.mark.xfail(reason="Known issue BUG: Validación faltante para caracteres numéricos en campo 'First name'", run=True)
def test_verificar_error_al_editar_campo_first_name_con_caracteres_numericos(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload_create = PayloadCreatePatients.build_payload_create_patient(headers)
    response_create_json = create_patient(headers, payload_create)
    patient_code = response_create_json["uuid"]
    random_numbers = str(fake.random_number(digits=8, fix_len=True))
    payload_update = PayloadUpdatePatients.build_payload_update_patient_custom(patient_code, payload_create, random_numbers)
    endpoint_update = EndpointPatients.code(patient_code)
    response_update = OpenMrsRequest.post(endpoint_update, headers, payload_update)
    AssertionStatusCode.assert_status_code_is_error(response_update)
    log_request_response(endpoint_update, response_update, headers)

@pytest.mark.negative
@pytest.mark.low
@pytest.mark.xfail(reason="Known issue BUG: Validación faltante para mas de 255 caracteres en campo 'First name'", run=True)
def test_verificar_error_al_ingresar_mas_de_255_caracteres_en_campo_first_name(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload_create = PayloadCreatePatients.build_payload_create_patient(headers)
    response_create_json = create_patient(headers, payload_create)
    caracteres_validos = string.ascii_letters
    data_random = ''.join(random.choices(caracteres_validos, k=300))
    patient_code = response_create_json["uuid"]
    payload_update = PayloadUpdatePatients.build_payload_update_patient_custom(patient_code, payload_create, data_random, None)
    endpoint_update = EndpointPatients.code(patient_code)
    response_update = OpenMrsRequest.post(endpoint_update, headers, payload_update)
    AssertionStatusCode.assert_status_code_is_error(response_update)
    log_request_response(endpoint_update, response_update, headers)

@pytest.mark.functional
@pytest.mark.medium
def test_actualizar_campo_last_name(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload_create = PayloadCreatePatients.build_payload_create_patient(headers)
    response_create_json = create_patient(headers, payload_create)
    patient_code = response_create_json["uuid"]
    payload_update = PayloadUpdatePatients.build_payload_update_patient_custom(patient_code, payload_create, None, fake.last_name())
    endpoint_update = EndpointPatients.code(patient_code)
    response_update = OpenMrsRequest.post(endpoint_update, headers, payload_update)
    response_update_json = response_update.json()
    AssertionStatusCode.assert_status_code_200(response_update)
    family_name_request = build_full_name(payload_update)
    family_name_updated = response_update_json["person"]["display"]
    assert family_name_updated == family_name_request
    log_request_response(endpoint_update, response_update, headers)
    created_patients.append(response_update.json())

# @pytest.mark.negative
# @pytest.mark.low
# def test_verificar_error_al_actualizar_campo_last_name_vacio(setup_add_patient):
#     headers, created_patients = setup_add_patient
#     payload_create = PayloadCreatePatients.build_payload_create_patient(headers)
#     response_create_json = create_patient(headers, payload_create)
#     patient_code = response_create_json["uuid"]
#     payload_update = PayloadUpdatePatients.build_payload_update_patient_custom(patient_code, payload_create, None, None, " ")
#     endpoint_update = EndpointPatients.code(patient_code)
#     response_update = OpenMrsRequest.post(endpoint_update, headers, payload_update)
#     AssertionStatusCode.assert_status_code_is_error(response_update)
#     log_request_response(endpoint_update, response_update, headers)

@pytest.mark.negative
@pytest.mark.low
@pytest.mark.xfail(reason="Known issue BUG: Validación faltante para caracteres numéricos en campo 'Last name'", run=True)
def test_verificar_error_al_editar_campo_last_name_con_caracteres_numericos(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload_create = PayloadCreatePatients.build_payload_create_patient(headers)
    response_create_json = create_patient(headers, payload_create)
    patient_code = response_create_json["uuid"]
    payload_update = PayloadUpdatePatients.build_payload_update_patient_custom(patient_code, payload_create, None, None, 12345)
    endpoint_update = EndpointPatients.code(patient_code)
    response_update = OpenMrsRequest.post(endpoint_update, headers, payload_update)
    AssertionStatusCode.assert_status_code_is_error(response_update)
    log_request_response(endpoint_update, response_update, headers)

@pytest.mark.negative
@pytest.mark.low
@pytest.mark.xfail(reason="Known issue BUG: Validación faltante para caracteres especiales en campo 'Last name'", run=True)
def test_verificar_error_al_editar_campo_last_name_con_caracteres_especiales(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload_create = PayloadCreatePatients.build_payload_create_patient(headers)
    response_create_json = create_patient(headers, payload_create)
    patient_code = response_create_json["uuid"]
    payload_update = PayloadUpdatePatients.build_payload_update_patient_custom(patient_code, payload_create, None, None, "@@@###$$$")
    endpoint_update = EndpointPatients.code(patient_code)
    response_update = OpenMrsRequest.post(endpoint_update, headers, payload_update)
    AssertionStatusCode.assert_status_code_is_error(response_update)
    log_request_response(endpoint_update, response_update, headers)

@pytest.mark.negative
@pytest.mark.low
def test_verificar_error_al_ingresar_mas_de_50_caracteres_en_campo_last_name(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload_create = PayloadCreatePatients.build_payload_create_patient(headers)
    response_create_json = create_patient(headers, payload_create)
    caracteres_validos = string.ascii_letters
    data_random = ''.join(random.choices(caracteres_validos, k=51))
    patient_code = response_create_json["uuid"]
    payload_update = PayloadUpdatePatients.build_payload_update_patient_custom(patient_code, payload_create, None, None, data_random)
    endpoint_update = EndpointPatients.code(patient_code)
    response_update = OpenMrsRequest.post(endpoint_update, headers, payload_update)
    AssertionStatusCode.assert_status_code_is_error(response_update)
    log_request_response(endpoint_update, response_update, headers)

@pytest.mark.functional
@pytest.mark.medium
def test_actualizar_campo_middle_name(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload_create = PayloadCreatePatients.build_payload_create_patient(headers)
    response_create_json = create_patient(headers, payload_create)
    patient_code = response_create_json["uuid"]
    payload_update = PayloadUpdatePatients.build_payload_update_patient_custom(patient_code, payload_create, None, None, fake.first_name())
    endpoint_update = EndpointPatients.code(patient_code)
    response_update = OpenMrsRequest.post(endpoint_update, headers, payload_update)
    response_update_json = response_update.json()
    AssertionStatusCode.assert_status_code_200(response_update)
    family_name_request = build_full_name(payload_update)
    family_name_updated = response_update_json["person"]["display"]
    assert family_name_updated == family_name_request
    log_request_response(endpoint_update, response_update, headers)
    created_patients.append(response_update.json())

@pytest.mark.negative
@pytest.mark.medium
def test_verificar_error_al_actualizar_campo_middle_name_vacio(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload_create = PayloadCreatePatients.build_payload_create_patient(headers)
    response_create_json = create_patient(headers, payload_create)
    patient_code = response_create_json["uuid"]
    payload_update = PayloadUpdatePatients.build_payload_update_patient_custom(patient_code, payload_create, None, "")
    endpoint_update = EndpointPatients.code(patient_code)
    response_update = OpenMrsRequest.post(endpoint_update, headers, payload_update)
    AssertionStatusCode.assert_status_code_200(response_update)
    log_request_response(endpoint_update, response_update, headers)

@pytest.mark.negative
@pytest.mark.low
@pytest.mark.xfail(reason="Known issue BUG: Validación faltante para caracteres numéricos en campo 'Middle name'", run=True)
def test_verificar_error_al_editar_campo_middle_name_con_caracteres_numericos(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload_create = PayloadCreatePatients.build_payload_create_patient(headers)
    response_create_json = create_patient(headers, payload_create)
    patient_code = response_create_json["uuid"]
    payload_update = PayloadUpdatePatients.build_payload_update_patient_custom(patient_code, payload_create, None, fake.numerify(text='#' * fake.random_int(min=2, max=50)) )
    endpoint_update = EndpointPatients.code(patient_code)
    response_update = OpenMrsRequest.post(endpoint_update, headers, payload_update)
    AssertionStatusCode.assert_status_code_is_error(response_update)
    log_request_response(endpoint_update, response_update, headers)

@pytest.mark.negative
@pytest.mark.low
@pytest.mark.xfail(reason="Known issue BUG: Validación faltante para caracteres especiales en campo 'Middle name'", run=True)
def test_verificar_error_al_editar_campo_middle_name_con_caracteres_especiales(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload_create = PayloadCreatePatients.build_payload_create_patient(headers)
    response_create_json = create_patient(headers, payload_create)
    patient_code = response_create_json["uuid"]
    payload_update = PayloadUpdatePatients.build_payload_update_patient_custom(patient_code, payload_create, None, fake.bothify(text='?' * fake.random_int(min=2, max=50), letters='!#$%&/()=?¿¡°|@€*+-_') )
    endpoint_update = EndpointPatients.code(patient_code)
    response_update = OpenMrsRequest.post(endpoint_update, headers, payload_update)
    AssertionStatusCode.assert_status_code_is_error(response_update)
    log_request_response(endpoint_update, response_update, headers)

@pytest.mark.negative
@pytest.mark.low
def test_verificar_error_al_ingresar_mas_de_50_caracteres_en_campo_middle_name(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload_create = PayloadCreatePatients.build_payload_create_patient(headers)
    response_create_json = create_patient(headers, payload_create)
    caracteres_validos = string.ascii_letters
    data_random = ''.join(random.choices(caracteres_validos, k=51))
    patient_code = response_create_json["uuid"]
    payload_update = PayloadUpdatePatients.build_payload_update_patient_custom(patient_code, payload_create, None,
                                                                               data_random)
    endpoint_update = EndpointPatients.code(patient_code)
    response_update = OpenMrsRequest.post(endpoint_update, headers, payload_update)
    AssertionStatusCode.assert_status_code_is_error(response_update)
    log_request_response(endpoint_update, response_update, headers)

@pytest.mark.functional
@pytest.mark.medium
def test_actualizar_todos_los_campos_de_basic_info(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload_create = PayloadCreatePatients.build_payload_create_patient(headers)
    response_create_json = create_patient(headers, payload_create)
    patient_code = response_create_json["uuid"]
    payload_update = PayloadUpdatePatients.build_payload_update_patient_custom(
        patient_code,
        payload_create,
        fake.first_name(),
        fake.name(),
        fake.last_name())
    endpoint_update = EndpointPatients.code(patient_code)
    response_update = OpenMrsRequest.post(endpoint_update, headers, payload_update)
    response_update_json = response_update.json()
    AssertionStatusCode.assert_status_code_200(response_update)
    family_name_request = build_full_name(payload_update)
    family_name_updated = response_update_json["person"]["display"]
    assert family_name_updated == family_name_request
    log_request_response(endpoint_update, response_update, headers)
    created_patients.append(response_update.json())

@pytest.mark.functional
@pytest.mark.medium
def test_actualizar_campo_birthdate(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload_create = PayloadCreatePatients.build_payload_create_patient(headers)
    response_create_json = create_patient(headers, payload_create)
    patient_code = response_create_json["uuid"]
    payload_update = PayloadUpdatePatients.build_payload_update_birthdate(
        patient_code,
        payload_create,
        fake.date_of_birth(minimum_age=1, maximum_age=90).strftime("%Y-%m-%d"))
    endpoint_update = EndpointPatients.code(patient_code)
    response_update = OpenMrsRequest.post(endpoint_update, headers, payload_update)
    response_update_json = response_update.json()
    AssertionStatusCode.assert_status_code_200(response_update)
    birthdate_request = payload_update["person"]["birthdate"]
    birthdate_updated = response_update_json["person"]["birthdate"]
    assert birthdate_updated == birthdate_request
    log_request_response(endpoint_update, response_update, headers)
    created_patients.append(response_update.json())

@pytest.mark.negative
@pytest.mark.medium
def test_actualizar_campo_birthdate_vacio(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload_create = PayloadCreatePatients.build_payload_create_patient(headers)
    response_create_json = create_patient(headers, payload_create)
    patient_code = response_create_json["uuid"]
    payload_update = PayloadUpdatePatients.build_payload_update_birthdate(
        patient_code,
        payload_create,
        "")
    endpoint_update = EndpointPatients.code(patient_code)
    response_update = OpenMrsRequest.post(endpoint_update, headers, payload_update)
    AssertionStatusCode.assert_status_code_400(response_update)
    log_request_response(endpoint_update, response_update, headers)
    created_patients.append(response_update.json())

@pytest.mark.negative
@pytest.mark.medium
def test_actualizar_campo_birthdate_con_letras(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload_create = PayloadCreatePatients.build_payload_create_patient(headers)
    response_create_json = create_patient(headers, payload_create)
    patient_code = response_create_json["uuid"]
    payload_update = PayloadUpdatePatients.build_payload_update_birthdate(
        patient_code,
        payload_create,
        "ADADWQE")
    endpoint_update = EndpointPatients.code(patient_code)
    response_update = OpenMrsRequest.post(endpoint_update, headers, payload_update)
    AssertionStatusCode.assert_status_code_400(response_update)
    log_request_response(endpoint_update, response_update, headers)
    created_patients.append(response_update.json())

@pytest.mark.functional
@pytest.mark.medium
def test_actualizar_campo_address(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload_create = PayloadCreatePatients.build_payload_create_patient_with_optional_fields(headers)
    response_create_json = create_patient(headers, payload_create)
    patient_code = response_create_json["uuid"]
    payload_update = PayloadUpdatePatients.build_payload_update_patient_field_addresses_custom(
        patient_code,
        payload_create,
        fake.street_address())
    endpoint_update = EndpointPatients.code(patient_code)
    response_update = OpenMrsRequest.post(endpoint_update, headers, payload_update)
    AssertionStatusCode.assert_status_code_200(response_update)
    log_request_response(endpoint_update, response_update, headers)
    created_patients.append(response_update.json())

@pytest.mark.negative
@pytest.mark.low
def test_actualizar_campo_address_con_mas_de_255_caracteres(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload_create = PayloadCreatePatients.build_payload_create_patient_with_optional_fields(headers)
    response_create_json = create_patient(headers, payload_create)
    patient_code = response_create_json["uuid"]
    caracteres_validos = string.ascii_letters
    data_random = ''.join(random.choices(caracteres_validos, k=300))
    payload_update = PayloadUpdatePatients.build_payload_update_patient_field_addresses_custom(
        patient_code,
        payload_create,
        data_random)
    endpoint_update = EndpointPatients.code(patient_code)
    response_update = OpenMrsRequest.post(endpoint_update, headers, payload_update)
    AssertionStatusCode.assert_status_code_400(response_update)
    log_request_response(endpoint_update, response_update, headers)
    created_patients.append(response_update.json())

@pytest.mark.negative
@pytest.mark.low
def test_actualizar_campo_address_con_numeros(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload_create = PayloadCreatePatients.build_payload_create_patient_with_optional_fields(headers)
    response_create_json = create_patient(headers, payload_create)
    patient_code = response_create_json["uuid"]
    payload_update = PayloadUpdatePatients.build_payload_update_patient_field_addresses_custom(
        patient_code,
        payload_create,
        122456)
    endpoint_update = EndpointPatients.code(patient_code)
    response_update = OpenMrsRequest.post(endpoint_update, headers, payload_update)
    AssertionStatusCode.assert_status_code_400(response_update)
    log_request_response(endpoint_update, response_update, headers)
    created_patients.append(response_update.json())

@pytest.mark.negative
@pytest.mark.low
@pytest.mark.xfail(reason="Known issue BUG: Validación faltante para caracteres especiales en el campo 'Address1'", run=True)
def test_actualizar_campo_address_con_puros_caracteres_especiales(setup_add_patient):
    headers, created_patients = setup_add_patient
    payload_create = PayloadCreatePatients.build_payload_create_patient_with_optional_fields(headers)
    response_create_json = create_patient(headers, payload_create)
    patient_code = response_create_json["uuid"]
    payload_update = PayloadUpdatePatients.build_payload_update_patient_field_addresses_custom(
        patient_code,
        payload_create,
        fake.bothify(text='?' * fake.random_int(min=2, max=100), letters='!#$%&/()=?¿¡°|@€*+-_'))
    endpoint_update = EndpointPatients.code(patient_code)
    response_update = OpenMrsRequest.post(endpoint_update, headers, payload_update)
    AssertionStatusCode.assert_status_code_400(response_update)
    log_request_response(endpoint_update, response_update, headers)
    created_patients.append(response_update.json())