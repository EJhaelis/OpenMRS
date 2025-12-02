from src.data.patients import generate_patients_source_data, get_valid_openmrs_id


class PayloadCreatePatients:
    @staticmethod
    def build_payload_create_patient_custom(auth_headers, given_name=None, middle_name=None, family_name=None,
                                            gender=None, birthdate=None):
        data = generate_patients_source_data()
        payload = {
            "person": {
                "gender": gender or data['gender'],
                "birthdate": birthdate or data['birthdate'],
                "names": [
                    {
                        "givenName": given_name or data['given_name'],
                        "familyName": family_name or data['family_name'],
                        "middleName": middle_name or data['middle_name'],
                        "preferred": True
                    }
                ]
            },
            "identifiers": [
                {
                    "identifier": get_valid_openmrs_id(auth_headers),
                    "identifierType": "05a29f94-c0ed-11e2-94be-8c13b969e334",
                    "location": "1ce1b7d4-c865-4178-82b0-5932e51503d6",
                    "preferred": True
                }
            ]
        }
        return payload

    @staticmethod
    def build_payload_create_patient_with_all_fields_mandatory(auth_headers):
        data = generate_patients_source_data()
        payload = {
            "person": {
                "gender": data['gender'],
                "names": [
                    {
                        "givenName": data['given_name'],
                        "familyName": data['family_name'],
                        "preferred": True
                    }
                ]
            },
            "identifiers": [
                {
                    "identifier": get_valid_openmrs_id(auth_headers),
                    "identifierType": "05a29f94-c0ed-11e2-94be-8c13b969e334",
                    "location": "1ce1b7d4-c865-4178-82b0-5932e51503d6",
                    "preferred": True
                }
            ]
        }
        return payload

    @staticmethod
    def build_payload_create_patient_without_give_name(auth_headers):
        data = generate_patients_source_data()
        payload = {
            "person": {
                "gender": data['gender'],
                "names": [
                    {
                        "familyName": data['family_name'],
                        "preferred": True
                    }
                ]
            },
            "identifiers": [
                {
                    "identifier": get_valid_openmrs_id(auth_headers),
                    "identifierType": "05a29f94-c0ed-11e2-94be-8c13b969e334",
                    "location": "1ce1b7d4-c865-4178-82b0-5932e51503d6",
                    "preferred": True
                }
            ]
        }
        return payload

    @staticmethod
    def build_payload_create_patient_without_middle_name(auth_headers):
        data = generate_patients_source_data()
        payload = {
            "person": {
                "gender": data['gender'],
                "names": [
                    {
                        "givenName": data['given_name'],
                        "familyName": data['family_name'],
                        "preferred": True
                    }
                ]
            },
            "identifiers": [
                {
                    "identifier": get_valid_openmrs_id(auth_headers),
                    "identifierType": "05a29f94-c0ed-11e2-94be-8c13b969e334",
                    "location": "1ce1b7d4-c865-4178-82b0-5932e51503d6",
                    "preferred": True
                }
            ]
        }
        return payload

    @staticmethod
    def build_payload_create_patient_without_family_name(auth_headers):
        data = generate_patients_source_data()
        payload = {
            "person": {
                "gender": data['gender'],
                "names": [
                    {
                        "givenName": data['given_name'],
                        "preferred": True
                    }
                ]
            },
            "identifiers": [
                {
                    "identifier": get_valid_openmrs_id(auth_headers),
                    "identifierType": "05a29f94-c0ed-11e2-94be-8c13b969e334",
                    "location": "1ce1b7d4-c865-4178-82b0-5932e51503d6",
                    "preferred": True
                }
            ]
        }
        return payload

    @staticmethod
    def build_payload_create_patient_without_gender(auth_headers):
        data = generate_patients_source_data()
        payload = {
            "person": {
                "names": [
                    {
                        "givenName": data['given_name'],
                        "preferred": True
                    }
                ]
            },
            "identifiers": [
                {
                    "identifier": get_valid_openmrs_id(auth_headers),
                    "identifierType": "05a29f94-c0ed-11e2-94be-8c13b969e334",
                    "location": "1ce1b7d4-c865-4178-82b0-5932e51503d6",
                    "preferred": True
                }
            ]
        }
        return payload

    @staticmethod
    def build_payload_create_patient_without_format_birthdate(auth_headers, birthdate):
        data = generate_patients_source_data()
        payload = {
            "person": {
                "birthdate": birthdate,
                "names": [
                    {
                        "givenName": data['given_name'],
                        "preferred": True
                    }
                ]
            },
            "identifiers": [
                {
                    "identifier": get_valid_openmrs_id(auth_headers),
                    "identifierType": "05a29f94-c0ed-11e2-94be-8c13b969e334",
                    "location": "1ce1b7d4-c865-4178-82b0-5932e51503d6",
                    "preferred": True
                }
            ]
        }
        return payload

    @staticmethod
    def build_payload_create_patient(auth_headers, gender=None, birthdate_is_null=False):
        data = generate_patients_source_data(birthdate_is_null)
        payload = {
            "person": {
                "gender": gender or data['gender'],
                "birthdate": data['birthdate'],
                "names": [
                    {
                        "givenName": data['given_name'],
                        "familyName": data['family_name'],
                        "middleName": data['middle_name'],
                        "preferred": True
                    }
                ]
            },
            "identifiers": [
                {
                    "identifier": get_valid_openmrs_id(auth_headers),
                    "identifierType": "05a29f94-c0ed-11e2-94be-8c13b969e334",
                    "location": "1ce1b7d4-c865-4178-82b0-5932e51503d6",
                    "preferred": True
                }
            ]
        }
        return payload

    @staticmethod
    def build_payload_create_patient_with_out_identifier():
        data = generate_patients_source_data()
        payload = {
            "person": {
                "gender": 'M',
                "birthdate": data['birthdate'],
                "names": [
                    {
                        "givenName": data['given_name'],
                        "familyName": data['family_name'],
                        "preferred": True
                    }
                ]
            }
        }
        return payload
    @staticmethod
    def build_payload_create_patient_with_identifier_defined():
        data = generate_patients_source_data()
        payload = {
            "person": {
                "gender": 'M',
                "birthdate": data['birthdate'],
                "names": [
                    {
                        "givenName": data['given_name'],
                        "familyName": data['family_name'],
                        "preferred": True
                    }
                ]
            },
            "identifiers": [
                {
                    "identifier": "10001MJ",
                    "identifierType": "05a29f94-c0ed-11e2-94be-8c13b969e334",
                    "location": "1ce1b7d4-c865-4178-82b0-5932e51503d6",
                    "preferred": True
                }
            ]
        }
        return payload
    @staticmethod
    def build_payload_create_patient_with_optional_fields(auth_headers, address1=None, country=None, city_village=None,
                                                          state_province=None, postal_code=None):
        data = generate_patients_source_data()
        payload = {
            "person": {
                "gender": 'M',
                "birthdate": data['birthdate'],
                "names": [
                    {
                        "givenName": data['given_name'],
                        "familyName": data['family_name'],
                        "preferred": True
                    }
                ],
                "addresses": [
                    {
                        "address1": address1 or data['address1'],
                        "country": country or "Bolivia",
                        "cityVillage": city_village or "cbba",
                        "stateProvince": state_province or "cbba",
                        "postalCode": postal_code or "+591"
                    }
                ]
            },
            "identifiers": [
                {
                    "identifier": get_valid_openmrs_id(auth_headers),
                    "identifierType": "05a29f94-c0ed-11e2-94be-8c13b969e334",
                    "location": "1ce1b7d4-c865-4178-82b0-5932e51503d6",
                    "preferred": True
                }
            ]
        }
        return payload

    @staticmethod
    def build_payload_create_patient_with_identifiers_custom(auth_headers, identifier=None, identifier_type=None, location=None):
        data = generate_patients_source_data()
        payload = {
            "person": {
                "gender": 'M',
                "birthdate": data['birthdate'],
                "names": [
                    {
                        "givenName": data['given_name'],
                        "familyName": data['family_name'],
                        "preferred": True
                    }
                ]
            },
            "identifiers": [
                {
                    "identifier": identifier or get_valid_openmrs_id(auth_headers),
                    "identifierType": identifier_type or "05a29f94-c0ed-11e2-94be-8c13b969e334",
                    "location": location or"1ce1b7d4-c865-4178-82b0-5932e51503d6",
                    "preferred": True
                }
            ]
        }
        return payload

    @staticmethod
    def build_payload_create_patient_with_telephone_fields(auth_headers, telephone=None):
        data = generate_patients_source_data()
        payload = {
            "person": {
                "gender": 'M',
                "birthdate": data['birthdate'],
                "names": [
                    {
                        "givenName": data['given_name'],
                        "familyName": data['family_name'],
                        "preferred": True
                    }
                ],
                "attributes": [
                    {
                        "attributeType": "14d4f066-15f5-102d-96e4-000c29c2a5d7",
                        "value": telephone or data["telephone"]
                    }
                ],
            },
            "identifiers": [
                {
                    "identifier": get_valid_openmrs_id(auth_headers),
                    "identifierType": "05a29f94-c0ed-11e2-94be-8c13b969e334",
                    "location": "1ce1b7d4-c865-4178-82b0-5932e51503d6",
                    "preferred": True
                }
            ]
        }
        return payload