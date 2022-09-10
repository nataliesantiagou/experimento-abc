# Experimentación

## Descarga e instalación del proyecto

Para descargar el proyecto puedes clonar el repositorio:

    git clone https://github.com/nataliesantiagou/experimento-abc.git
    
Ir a la rama main:

    git checkout main

### Creación entorno virtual
Para crear un entorno virtual ejecutar el siguiente comando:

    python3 -m venv venv
    
Para activar entorno virtual ejecutar el siguiente comando:

    source venv/bin/activate

### Instalación de dependencias
En el proyecto se distribuye un fichero (requirements.txt) con todas las dependencias. Para instalarlas
basta con ejectuar:

    pip install -r requirements.txt
    
## Ejecución con el servidor que trae Flask

Una vez descargado el proyecto e instalado las dependencias, ejecutar el siguiente comando:

    flask run
