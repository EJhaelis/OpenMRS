from src.routes.endpoint_patients import EndpointPatients
from src.routes.request import OpenMrsRequest

class PatientsCall:
    @classmethod
    def view(cls, headers):
        """Obtener las opciones disponibles"""
        response = OpenMrsRequest().get(EndpointPatients.patient(), headers)
        return response.json()

    @classmethod
    def create(cls, headers, payload):
        """Crear una nueva opción"""
        response = OpenMrsRequest().post(EndpointPatients.patient(), headers, payload)
        return response.json()

    @classmethod
    def update(cls, headers, payload, option_code):
        """Actualizar una opción existente"""
        response = OpenMrsRequest().put(EndpointPatients.code(option_code), headers, payload)
        return response.json()

    @classmethod
    def delete(cls, headers, option_code):
        """Eliminar una opción por código"""
        response = OpenMrsRequest().delete(EndpointPatients.code(option_code), headers)
        return response

    @classmethod
    def view_option(cls, headers, option_code):
        """Obtener una opción específica por código"""
        response = OpenMrsRequest().get(EndpointPatients.code(option_code), headers)
        return response.json() if response.status_code == 200 else None
