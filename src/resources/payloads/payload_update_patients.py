class PayloadUpdatePatients:

    @staticmethod
    def build_payload_update_patient_custom(uuid, json_schema, given_name=None, middle_name=None, family_name=None,
                                            preferred=None, gender=None, birthdate=None):
        payload = {
            "uuid": uuid,
            "person": {
                "uuid": uuid,
                "names": [
                    {
                        # Usar given_name si fue proporcionado (incluso si es vacío),
                        # otherwise usar el valor del schema
                        "givenName": given_name if given_name is not None else json_schema["person"]["names"][0][
                            "givenName"],
                        "middleName": middle_name if middle_name is not None else json_schema["person"]["names"][0][
                            "middleName"],
                        "familyName": family_name if family_name is not None else json_schema["person"]["names"][0][
                            "familyName"],
                        "preferred": preferred if preferred is not None else json_schema["person"]["names"][0][
                            "preferred"]
                    }
                ],
                "gender": gender if gender is not None else json_schema["person"]["gender"],
                "birthdate": birthdate if birthdate is not None else json_schema["person"]["birthdate"]
            }
        }
        return payload

    @staticmethod
    def build_payload_update_patient_field_addresses_custom(uuid, json_schema, address1=None, city_village=None, state_province=None,
                                            postal_code=None, country=None):
        payload = {
            "uuid": uuid,
            "person": {
                "uuid": uuid,
                "addresses": [
                    {
                        "address1": address1 if address1 is not None else json_schema["person"]["addresses"][0]["address1"],
                        "cityVillage": city_village if city_village is not None else json_schema["person"]["addresses"][0]["cityVillage"],
                        "stateProvince": state_province if state_province is not None else json_schema["person"]["addresses"][0]["stateProvince"],
                        "postalCode": postal_code if postal_code is not None else json_schema["person"]["addresses"][0]["postalCode"],
                        "country": country if country is not None else json_schema["person"]["addresses"][0]["country"],
                    }
                ]
            }
        }
        return payload
    @staticmethod
    def build_payload_update_birthdate(uuid, json_schema, birthdate):
        """
        Payload específico para actualizar solo el birthdate
        """
        # Convertir a formato ISO 8601
        formatted_birthdate = f"{birthdate}T00:00:00.000+0000"

        payload = {
            "uuid": uuid,
            "person": {
                "uuid": uuid,
                "names": [
                    {
                        "preferred": json_schema["person"]["names"][0]["preferred"],
                        "givenName": json_schema["person"]["names"][0]["givenName"],
                        "middleName": json_schema["person"]["names"][0]["middleName"],
                        "familyName": json_schema["person"]["names"][0]["familyName"]
                    }
                ],
                "gender": json_schema["person"]["gender"],
                "birthdate": formatted_birthdate
            }
        }
        return payload

    @staticmethod
    def build_payload_update_invalid_patient(uuid):
        """
        Payload simple para pruebas negativas - no requiere datos de paciente existente
        """
        payload = {
            "uuid": uuid,
            "person": {
                "uuid": uuid,
                "names": [
                    {
                        "preferred": True,
                        "givenName": "Test",
                        "familyName": "Patient"
                    }
                ],
                "gender": "M"
            }
        }
        return payload