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


class Estudio(models.Model):
    name = models.CharField(max_length=255)




class DicomFile(models.Model):
    dicom_file = models.BinaryField()  # Campo para almacenar el contenido binario del archivo DICOM
    uploaded_at = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    estudio = models.ForeignKey(Estudio,related_name='dicom_images',on_delete=models.CASCADE)
    instance_number = models.IntegerField(null=True,blank=True)

    class Meta:
        ordering = ['instance_number']

    def __str__(self):
        return f'DICOM file uploaded on {self.uploaded_at}'