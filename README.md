# DIPLOMADO INGENIERÍA DE CALIDAD DE SOFTWARE COMERCIAL (3ra Edición)

## Pruebas Manuales y Automatizadas API Para el Módulo de Pacientes de OpenMRS3
### Autor: Erika Jhaelis Soto Diaz

### Descripción:
Este repositorio contiene las pruebas automatizadas del CRUD (Crear, Leer, Actualizar, Eliminar) para el módulo de Pacientes de OpenMRS3. Las pruebas están diseñadas para validar la funcionalidad del API RESTful que maneja las operaciones relacionadas con los pacientes en el sistema OpenMRS.

### Requisitos:
* **Python 3.12** o superior.
* **pip** (gestor de paquetes de Python).
* **Git** (para control de versiones).
* **Docker** (Recomendado para levantar el entorno de pruebas local).
* **Allure CLI** (Opcional, para visualizar reportes avanzados).
* **IDE:** PyCharm o Visual Studio Code.

## Configuración del Entorno 

Las pruebas están configuradas por defecto para ejecutarse contra una instancia local de OpenMRS en Docker. Esto garantiza estabilidad y control sobre los datos.

**1. Levantar OpenMRS en Docker:**
```bash
docker run -dp 80:8080 --name openmrs openmrs/openmrs-reference-application-3-gateway
```

## Instalación:
1. Clona este repositorio en tu máquina local:
   ```bash
   git clone https://github.com/EJhaelis/OpenMRS.git      
2. Navega al directorio del proyecto
3. Crea un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   source venv\Scripts\activate
   ```
4. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```
5. Configura las variables de entorno necesarias en un archivo `.env`
    - `BASE_URL`: http://localhost/openmrs
    - `USERNAME`: Admin
    - `PASSWORD`: Admin123
    - `BASIC_TOKEN`: YWRtaW46QWRtaW4xMjM=

Las credenciales son públicas para la instalación local de OpenMRS.

## Ejecución de Pruebas:
Para ejecutar las pruebas automatizadas, utiliza el siguiente comando:
```bash
pytest
```

Para ejecutar por tipo de prueba, utilice la opción -m de pytest junto con la marca correspondiente:
```bashbash
pytest -m functional
pytest -m negative
pytest -m boundary
pytest -m high
pytest -m medium
pytest -m low
```

## Generación y Visualización de Reportes:
Después de ejecutar las pruebas, puedes generar un reporte HTML utilizando el siguiente comando:
```bash
pytest --html=report.html
```
Luego, abre el archivo `report.html` en tu navegador para visualizar los resultados de las pruebas. 

También puedes utilizar la herramienta Allure para generar reportes más detallados:
- Primero se debe crear una carpeta para los reportes llamada `reports` y luego ejecutar el siguiente comando:

```bash
pytest --alluredir=reports 
```
- Para visualizar el reporte, utiliza el siguiente comando:
```bash
allure serve reports
```

