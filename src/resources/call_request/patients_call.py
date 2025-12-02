from src.routes.endpoint_patients import EndpointPatients
from src.routes.request import OpenMrsRequest

class PatientsCall:
    @classmethod
    def view(cls, headers):
        response = OpenMrsRequest().get(EndpointPatients.patient(), headers)
        return response.json()

    @classmethod
    def create(cls, headers, payload):
        response = OpenMrsRequest().post(EndpointPatients.patient(), headers, payload)
        return response.json()

    @classmethod
    def update(cls, headers, payload, option_code):
        response = OpenMrsRequest().put(EndpointPatients.code(option_code), headers, payload)
        return response.json()

    @classmethod
    def delete(cls, headers, option_code):
        response = OpenMrsRequest().delete(EndpointPatients.code(option_code), headers)
        return response

    @classmethod
    def view_option(cls, headers, option_code):
        response = OpenMrsRequest().get(EndpointPatients.code(option_code), headers)
        return response.json() if response.status_code == 200 else None
