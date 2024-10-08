Se adjunta codigo base del proyecto, se trabaja con el framework Django. 

Se debe tener instalada la última versión de python.

Librerias a instalar previamente:
pip install pipenv

Para el Hito-3, en adelante, se implementó una BD en MySql, la que se puede crear instalando la ultima version de esta
y ejecutando en la command line client la siguiente linea: CREATE DATABASE dicomviewer;
cabe aclarar que por ahora no tiene implementación directa y el guardado de imágenes DICOM es local.
Para cargar imagenes crear un super usuario en django y subirlas mediante el admin de django.  

Para ejecutar la aplicación web, se debe descargar la carpeta "proyecto", luego abrir la consola dentro de "proyecto",
ejecutar:

"pipenv install django"  //para instalar django (solo la primera vez)
"pipenv shell"  //para iniciar el entorno virtual
"python manage.py runserver"  //para correr la aplicación web

seguido de esto aparecerá un link en consola que se podrá abrir con ctrl+click,
abierta la página ya se podrá navegar en esta mediante la barra de direcciones superior para acceder a la lista y subida de archivos de la aplicación.

Para ejecutar las pruebas unitarias, abrir una consola dentro de la carpeta tests y correr el siguiente comando: python -m unittest tests.py
