Instrucciones para levantar el proyecto.

1- instalar el requirements.txt, puede hacerlo en un ambiente virtual si lo desea.

2- Crear base de datos 'dicomviewer' ( recomendacion de uso xampp) en phpmyadmin o crear bd con consola de mysql, usando el comando:
CREATE DATABASE dicomviewer; (Puede usar MySQL9.0 Command Line Client)

3- Realizar migraciones a la base de datos: python manage.py makemigrations y python manage.py migrate.

4- Crear el super usuario para poder realizar la subida de archivos, asociados a al ususario: python manage.py createsuperuser.

5-Ejecutar el main, python manage,py runserver
