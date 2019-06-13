# Dashboard para proyectos

Dashboard para mostrar información de proyectos de Github y Discord.

## Extracción de Datos

El dashboard necesita datos de Discord y de Github para presentar las gráficas. Para la generación de dichos datos es necesario configurar y ejecutar los scripts almacenados en `dataextractor`. Actualmente la configuración de tokens, servidor de discord, repositorios, etc. se hace desde código por lo que será necesario modificar los scripts para que se puedan generar los datos que nos interesen.

## Despliegue

Para lanzar el dashboard es necesario tener instalado [Docker](https://www.docker.com/). Una vez instalado:

1. Copiar a la carpeta `data` el archivo `commits.csv`, generado con la aplicación (por determinar) 
1. Lanzar los servicios del dashboard con `docker-compose up`
2. Acceso a través de <http://127.0.0.1>
3. Una vez usado, tirar abajo los servicios con `docker-compose down`

Para el despliegue con Docker se ha utilizado la configuración descrita en el siguiente repositorio:

- <https://github.com/sladkovm/docker-flask-gunicorn-nginx>


## Implementación

El dashboard ha sido implementado usando [Dash](https://dash.plot.ly/) y el código fuente está en el directorio `web`. Para editarlo se recomienda comenzar ejecutando el archivo `web\devenv.sh`, que crea un entorno virtual con los módulos de Python usados en su desarrollo. 


