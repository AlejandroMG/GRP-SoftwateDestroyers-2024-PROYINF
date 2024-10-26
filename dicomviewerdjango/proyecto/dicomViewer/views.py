from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import DicomFile
import pydicom
from PIL import Image
import numpy as np
import io
import base64
from django.contrib import messages

# Se le envía una solicitud y retorna una respuesta.
def inicio(request):
    return render(request, 'paginas/inicio.html')

def nosotros(request):
    return render(request, 'paginas/nosotros.html')

def archivos(request):
    archivos_dicom = DicomFile.objects.all()  # Obtiene todos los archivos DICOM
    return render(request, 'archivos/index.html', {'archivos': archivos_dicom})

def subirArchivo(request):
    if request.method == 'POST' and request.FILES['file']:
        dicom_file = request.FILES['file']

        # Si el usuario está autenticado, lo asigna; de lo contrario, lo deja nulo
        usuario = request.user if request.user.is_authenticated else None

        # Leer el archivo DICOM en bytes
        dicom_data = dicom_file.read()

        # Guardar el archivo DICOM en la base de datos
        archivo = DicomFile(dicom_file=dicom_data, usuario=usuario)
        archivo.save()

        return redirect('archivos/')  # Redirigir a la página de archivos después de la subida

    return render(request, 'archivos/subirArchivo.html')


# Vista para ver un archivo DICOM desde la base de datos y mostrar su imagen y datos
def verArchivo(request, pk):
    archivo = get_object_or_404(DicomFile, pk=pk)

    try:
        # Leer el archivo DICOM desde el campo de la base de datos (bytes)
        dicom_data = io.BytesIO(archivo.dicom_file)  # Usar los datos desde la base de datos
        ds = pydicom.dcmread(dicom_data)

        # Verificar si el archivo tiene datos de imagen
        if hasattr(ds, 'pixel_array'):
            pixel_array = ds.pixel_array

            # Normalizar los valores de los píxeles para visualización
            pixel_array = pixel_array.astype(np.float32)
            pixel_array = (pixel_array - np.min(pixel_array)) / (np.max(pixel_array) - np.min(pixel_array)) * 255.0
            pixel_array = pixel_array.astype(np.uint8)

            # Convertir la matriz a una imagen de PIL
            image = Image.fromarray(pixel_array)

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


from django.db.models import Q

def archivos(request):
    archivos_dicom = DicomFile.objects.all()  # Obtiene todos los archivos DICOM

    # Obtener los parámetros de búsqueda (filtros)
    study_id_filter = request.GET.get('study_id', '').strip()
    patient_id_filter = request.GET.get('patient_id', '').strip()
    study_date_filter = request.GET.get('study_date', '').strip()

    archivos_info = []
    for archivo in archivos_dicom:
        try:
            # Leer el archivo DICOM desde la base de datos
            dicom_data = io.BytesIO(archivo.dicom_file)
            ds = pydicom.dcmread(dicom_data)

            # Extraer el ID del paciente, la fecha de estudio y el ID de estudio si están presentes
            patient_id = ds.PatientID if 'PatientID' in ds else 'Desconocido'
            study_date = ds.StudyDate if 'StudyDate' in ds else 'Desconocido'
            study_id = ds.StudyID if 'StudyID' in ds else 'Desconocido'

            # Aplicar filtros si se han proporcionado
            if study_id_filter and study_id_filter not in study_id:
                continue
            if patient_id_filter and patient_id_filter not in patient_id:
                continue
            if study_date_filter and study_date_filter not in study_date:
                continue

            archivos_info.append({
                'archivo': archivo,
                'patient_id': patient_id,
                'study_date': study_date,
                'study_id': study_id,
            })

        except Exception as e:
            archivos_info.append({
                'archivo': archivo,
                'patient_id': 'Error al leer',
                'study_date': 'Error al leer',
                'study_id': 'Error al leer',
            })

    return render(request, 'archivos/index.html', {'archivos_info': archivos_info})


# Vista para editar y visualizar un archivo DICOM
def editar_archivo(request, pk):
    archivo = get_object_or_404(DicomFile, pk=pk)

    try:
        # Leer el archivo DICOM desde la base de datos
        dicom_data = io.BytesIO(archivo.dicom_file)
        ds = pydicom.dcmread(dicom_data)

        # Verificar si el archivo tiene datos de imagen
        if hasattr(ds, 'pixel_array'):
            pixel_array = ds.pixel_array
            pixel_array = pixel_array.astype(np.float32)
            pixel_array = (pixel_array - np.min(pixel_array)) / (np.max(pixel_array) - np.min(pixel_array)) * 255.0
            pixel_array = pixel_array.astype(np.uint8)

            # Convertir la matriz a una imagen de PIL
            image = Image.fromarray(pixel_array)

            # Guardar la imagen en un buffer para mostrar en HTML
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
        else:
            img_str = None

        # Extraer metadatos del archivo DICOM
        dicom_data = {
            'patient_name': ds.PatientName if 'PatientName' in ds else 'Desconocido',
            'study_description': ds.StudyDescription if 'StudyDescription' in ds else 'Desconocido',
            'modality': ds.Modality if 'Modality' in ds else 'Desconocido',
            'study_date': ds.StudyDate if 'StudyDate' in ds else 'Desconocido',
            'study_id': ds.StudyID if 'StudyID' in ds else 'Desconocido',
        }

    except Exception as e:
        return HttpResponse(f"Error al procesar el archivo DICOM: {e}")

    # Renderizar el template de edición
    return render(request, 'archivos/edicionArchivo.html', {
        'archivo': archivo,
        'img_data': img_str,
        'dicom_data': dicom_data
    })