from django.db import models
import os
from django.utils.timezone import now

# Función para generar la ruta donde se guardarán los archivos DICOM
def dicom_directory_path(instance, filename):
    # Guardar el archivo en una carpeta separada por el nombre de usuario y la fecha actual
    return os.path.join('dicoms', str(instance.usuario.id), now().strftime('%Y/%m/%d'), filename)


# Modelo para los usuarios
class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    password = models.CharField(max_length=100, verbose_name='Contraseña')

    def __str__(self):
        return self.nombre
    
# Modelo para los archivos DICOM


class DicomFile(models.Model):
    dicom_file = models.FileField(upload_to='dicom_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return self.dicom_file.name