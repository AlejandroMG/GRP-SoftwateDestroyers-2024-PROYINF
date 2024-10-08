Se adjunta codigo base del proyecto, se trabaja con el framework Django. 

Se debe tener instalada la última versión de python.

Librerias a instalar previamente:
pip install pipenv


Para ejecutar la aplicación web, se debe descargar la carpeta "tarea", luego abrir la consola dentro de "tarea",
ejecutar:

"pipenv install django"  //para instalar django (solo la primera vez)
"pipenv shell"  //para iniciar el entorno virtual
"python manage.py runserver"  //para correr la aplicación web

seguidoi de esto aparecerá un link en consola que se podrá abrir con ctrl+click,
abierta la página ya se podrá navegar en esta mediante la barra de direcciones superior para acceder a la lista y subida de archivos de la aplicación.

Para ejecutar las pruebas unitarias, abrir una consola dentro de la carpeta tests y correr el siguiente comando: python -m unittest tests.py
