from faker import Faker
import random
import requests

fake = Faker()
from datetime import date
from utils.config import BASE_URL
from src.routes.endpoint import Endpoint
from src.routes.request import OpenMrsRequest
import logging


def generate_patients_source_data(birthdate_is_null=False):
    gender = random.choice(['M', 'F', 'O'])
    if gender == 'M':
        given_name = fake.first_name_male()
        middle_name = fake.first_name_male()
    else:
        given_name = fake.first_name_female()
        middle_name = fake.first_name_female()

    family_name = fake.last_name()
    start_date = date.today().replace(year=date.today().year - 80)
    end_date = date.today().replace(year=date.today().year - 18)
    birthdate = (
        None
        if birthdate_is_null
        else fake.date_between(start_date=start_date, end_date=end_date).isoformat()
    )
    street_type = random.choice(["Av.", "Calle"])
    street_name = fake.street_name()
    street_intersect_1 = fake.street_name()
    street_intersect_2 = fake.street_name()
    address_line_1 = (
        f"{street_type} {street_name} entre {street_intersect_1} y {street_intersect_2}"
    )
    return {
        "gender": gender,
        "birthdate": birthdate,
        "given_name": given_name,
        "middle_name": middle_name,
        "family_name": family_name,
        "address1": address_line_1,
        "telephone": fake.phone_number() ,
        "country": "Bolivia",
        "cityVillage": "cbba",
        "stateProvince": "cbba",
        "postalCode": "+591"
    }


def get_valid_openmrs_id(auth_headers):
    id_gen_endpoint = f"{BASE_URL}{Endpoint.BASE_GENERATE_IDGEN_ID.value}"
    try:
        response = OpenMrsRequest.get(id_gen_endpoint, auth_headers)
        response.raise_for_status()
        generated_id_data = response.json()

        # 1. Lógica para el formato específico: {"results": [{"identifierValue": "..."}]}
        if isinstance(generated_id_data, dict) and 'results' in generated_id_data:
            results = generated_id_data['results']
            if isinstance(results, list) and len(results) > 0 and 'identifierValue' in results[0]:
                generated_id = results[0]['identifierValue']

        # 2. Lógica para otros formatos comunes (como fallback)
        elif isinstance(generated_id_data, list) and generated_id_data:
            generated_id = generated_id_data[0]
        elif isinstance(generated_id_data, dict) and 'identifier' in generated_id_data:
            generated_id = generated_id_data['identifier']
        elif response.text.strip():
            # Texto plano como fallback
            generated_id = response.text.strip()

        if not generated_id:
            # Si después de todos los intentos no se pudo extraer el ID
            raise ValueError("Respuesta del generador de ID vacía o inesperada. No se encontró 'identifierValue'.")

        return generated_id.strip()

    except requests.exceptions.RequestException as e:
        logging.error(f"FATAL: No se pudo obtener el OpenMRS ID. ¿Está el servidor IDGEN disponible? Error: {e}")
        raise
