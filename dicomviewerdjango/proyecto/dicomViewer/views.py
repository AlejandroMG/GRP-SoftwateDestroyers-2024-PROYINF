from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import DicomFile
import pydicom
from PIL import Image
import numpy as np
import io
import base64
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt



from django.shortcuts import render, get_object_or_404
from .models import DicomFile

# Se le envía una solicitud y retorna una respuesta.
def inicio(request):
    return render(request, 'paginas/inicio.html')

def nosotros(request):
    return render(request, 'paginas/nosotros.html')

def archivos(request):
    archivos_dicom = DicomFile.objects.all()  # Obtiene todos los archivos DICOM
    return render(request, 'archivos/index.html', {'archivos': archivos_dicom})

def subirArchivo(request):  
    return render(request, 'archivos/subirArchivo.html')

@csrf_exempt
def subirArchivo(request):
    if request.method == 'POST' and request.FILES['file']:
        dicom_file = request.FILES['file']

        # Si el usuario está autenticado, lo asigna; de lo contrario, lo deja nulo
        usuario = request.user if request.user.is_authenticated else None

        # Guardar el archivo usando FileSystemStorage
        fs = FileSystemStorage()
        filename = fs.save(dicom_file.name, dicom_file)

        # Guardar el archivo en la base de datos
        archivo = DicomFile(dicom_file=filename, usuario=usuario)
        archivo.save()

        return redirect('archivos')  # Redirigir a la página de archivos después de la subida

    return render(request, 'archivos/subirArchivo.html')




# Vista para ver un archivo DICOM y mostrar su imagen y datos
def verArchivo(request, pk):
    archivo = get_object_or_404(DicomFile, pk=pk)

    try:
        # Leer el archivo DICOM
        ds = pydicom.dcmread(archivo.dicom_file.path)

        # Verificar si el archivo tiene datos de imagen
        if hasattr(ds, 'pixel_array'):
            pixel_array = ds.pixel_array
            image = Image.fromarray(pixel_array).convert("L")  # Convertir a escala de grises (o eliminar "convert" si es color)

            # Guardar la imagen en un buffer para mostrar en HTML
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
        else:
            img_str = None

        # Extraer otros metadatos DICOM
        dicom_data = {
            'patient_name': ds.PatientName if 'PatientName' in ds else 'Desconocido',
            'study_description': ds.StudyDescription if 'StudyDescription' in ds else 'Desconocido',
            'modality': ds.Modality if 'Modality' in ds else 'Desconocido',
            'study_date': ds.StudyDate if 'StudyDate' in ds else 'Desconocido',
            'study_id': ds.StudyID if 'StudyID' in ds else 'Desconocido',
            # Agrega más campos relevantes aquí si es necesario
        }

    except Exception as e:
        return HttpResponse(f"Error al procesar el archivo DICOM: {e}")

    return render(request, 'archivos/verArchivo.html', {
        'archivo': archivo,
        'img_data': img_str,
        'dicom_data': dicom_data
    })
# Vista para eliminar un archivo DICOM
def eliminar_archivo(request, pk):
    archivo = get_object_or_404(DicomFile, pk=pk)
    
    if request.method == 'POST':
        archivo.delete()
        messages.success(request, 'Archivo eliminado exitosamente.')
        return redirect('archivos')  # Redirige a la lista de archivos después de eliminar

    return redirect('archivos')  # Si no es POST, redirige a la lista de archivos