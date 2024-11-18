from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import DicomFile, Estudio
import pydicom
from PIL import Image
import numpy as np
import io
import base64
from django.contrib import messages
import zipfile
from io import BytesIO

from django.http import JsonResponse
read_error = 'Error al leer'
# Se le envía una solicitud y retorna una respuesta.
def inicio(request):
    return render(request, 'paginas/inicio.html')

def nosotros(request):
    return render(request, 'paginas/nosotros.html')

def archivos(request):
    archivos_dicom = DicomFile.objects.all()  # Obtiene todos los archivos DICOM
    return render(request, 'archivos/index.html', {'archivos': archivos_dicom})
'''

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
'''
#Subir archivo zip

def subirArchivo(request):
    if request.method == 'POST' and request.FILES.get('file'):
        zip_file = request.FILES['file']
        nombre_estudio = request.POST.get("nombreEstudio")
        # Obtener o crear el estudio con el nombre 'Nuevo Estudio'
        study = Estudio.objects.create(name=nombre_estudio)

        try:
            # Abre el archivo ZIP
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                for file_name in zip_ref.namelist():
                    with zip_ref.open(file_name) as dicom_file:
                        try:
                            # Lee y convierte el archivo DICOM a binario
                            dicom_data = dicom_file.read()
                            usuario = request.user if request.user.is_authenticated else None
                            dicom_bytes_io = BytesIO(dicom_data)
                            ds = pydicom.dcmread(dicom_bytes_io)
                            instance_number = ds.get("InstanceNumber",None)
                            
                            # Crea el objeto DicomFile en la base de datos
                            DicomFile.objects.create(
                                estudio=study,
                                usuario=usuario,
                                dicom_file=dicom_data,
                                instance_number = instance_number
                            )
                        except Exception as e:
                            print(f"Error al procesar {file_name}: {e}")
        except zipfile.BadZipFile:
            print("El archivo no es un archivo ZIP válido.")

        return redirect('verEstudios')

    return render(request, 'archivos/subirArchivo.html')




# Vista para ver un archivo DICOM desde la base de datos y mostrar su imagen y datos
def verArchivo(request, pk,study_id):
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
            'patient_sex': ds.PatientSex if 'PatientSex' in ds else 'Desconocido',
            'modality': ds.Modality if 'Modality' in ds else 'Desconocido',
            'study_date': ds.StudyDate if 'StudyDate' in ds else 'Desconocido',
            'study_id': ds.StudyID if 'StudyID' in ds else 'Desconocido',
            'patient_age': ds.PatientAge if 'PatientAge' in ds else 'Desconocido',
            'patient_birth_date': ds.PatientBirthDate if 'PatientBirthDate' in ds else 'Desconocido',
        
            'modality': ds.Modality if 'Modality' in ds else 'Desconocido',
            'study_date': ds.StudyDate if 'StudyDate' in ds else 'Desconocido',
            'study_id': ds.StudyID if 'StudyID' in ds else 'Desconocido',
            
            'protocol_name': ds.ProtocolName if 'ProtocolName' in ds else 'Desconocido',
            'series_number': ds.SeriesNumber if 'SeriesNumber' in ds else 'Desconocido',
            'series_description': ds.SeriesDescription if 'SeriesDescription' in ds else 'Desconocido',
            'instance_number': ds.InstanceNumber if 'InstanceNumber' in ds else -1,
            
            # Agrega más campos relevantes aquí si es necesario
        }

    except Exception as e:
        return HttpResponse(f"Error al procesar el archivo DICOM: {e}")

    return render(request, 'archivos/verArchivo.html', {
        'archivo': archivo,
        'img_data': img_str,
        'dicom_data': dicom_data,
        'id_estudio': study_id
    })


# Vista para eliminar un archivo DICOM
def eliminar_archivo(request, pk,study_id):
    archivo = get_object_or_404(DicomFile, pk=pk)
    
    if request.method == 'POST':
        archivo.delete()
        messages.success(request, 'Archivo eliminado exitosamente.')
        return redirect('archivos',pk=study_id)  # Redirige a la lista de archivos después de eliminar

    return redirect('archivos',pk=study_id)  # Si no es POST, redirige a la lista de archivos


def eliminar_estudio(request, pk):
    estudio = get_object_or_404(Estudio, pk=pk)
    
    if request.method == 'POST':
        estudio.delete()
        messages.success(request, 'Estudio eliminado exitosamente.')
        return redirect('verEstudios')  # Redirige a la lista de archivos después de eliminar

    return redirect('verEstudios')


from django.db.models import Q

def obtener_dicom_info(archivo):
    """Obtiene la información de un archivo DICOM"""
    try:
        dicom_data = io.BytesIO(archivo.dicom_file)
        id_bd = archivo.id
        #print(id_bd)
        ds = pydicom.dcmread(dicom_data)
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


        return {
            'patient_id': ds.PatientID if 'PatientID' in ds else 'Desconocido',
            'study_date': ds.StudyDate if 'StudyDate' in ds else 'Desconocido',
            'study_id': ds.StudyID if 'StudyID' in ds else 'Desconocido',
            'image': img_str,
            'patient_name': ds.PatientName if 'PatientName' in ds else 'Desconocido',
            'study_description': ds.StudyDescription if 'StudyDescription' in ds else 'Desconocido',
            'patient_sex': ds.PatientSex if 'PatientSex' in ds else 'Desconocido',
            'patient_age': ds.PatientAge if 'PatientAge' in ds else 'Desconocido',
            'patient_birth_date': ds.PatientBirthDate if 'PatientBirthDate' in ds else 'Desconocido',
            'protocol_name': ds.ProtocolName if 'ProtocolName' in ds else 'Desconocido',
            'series_number': ds.SeriesNumber if 'SeriesNumber' in ds else 'Desconocido',
            'series_description': ds.SeriesDescription if 'SeriesDescription' in ds else 'Desconocido',
            'instance_number': ds.InstanceNumber if 'InstanceNumber' in ds else -1,
            'id_bd': id_bd,
        }
    except Exception:
        return {
            'patient_id': read_error,
            'study_date': read_error,
            'study_id': read_error,
            'image':read_error,
        }

def aplicar_filtros(dicom_info, study_id_filter, patient_id_filter, study_date_filter):
    """Aplica filtros de búsqueda a la información DICOM"""
    if study_id_filter and study_id_filter not in dicom_info['study_id']:
        return False
    if patient_id_filter and patient_id_filter not in dicom_info['patient_id']:
        return False
    if study_date_filter and study_date_filter not in dicom_info['study_date']:
        return False
    return True


def estudios(request):
    estudios = Estudio.objects.all()

    studies = []
    for estudio in estudios:
        studies.append(estudio)
    return render(request,'archivos/verEstudio.html',{'estudios' : studies })



def archivos(request,pk):
    estudio = Estudio.objects.get(id=pk)
    archivos_dicom = estudio.dicom_images.all()
    #archivos_dicom = DicomFile.objects.filter(estudio=pk)
    study_id_filter = request.GET.get('study_id', '').strip()
    patient_id_filter = request.GET.get('patient_id', '').strip()
    study_date_filter = request.GET.get('study_date', '').strip()

    archivos_info = []

    for archivo in archivos_dicom:
        dicom_info = obtener_dicom_info(archivo)

        if aplicar_filtros(dicom_info, study_id_filter, patient_id_filter, study_date_filter):
            dicom_info['archivo'] = archivo
            archivos_info.append(dicom_info)

    return render(request, 'archivos/vistaGeneral.html', {'archivos_info': archivos_info,'id_estudio':pk})

def listadoArchivos(request,pk):
    estudio = Estudio.objects.get(id=pk)
    archivos_dicom = estudio.dicom_images.all()
    #archivos_dicom = DicomFile.objects.filter(estudio=pk)
    study_id_filter = request.GET.get('study_id', '').strip()
    patient_id_filter = request.GET.get('patient_id', '').strip()
    study_date_filter = request.GET.get('study_date', '').strip()

    archivos_info = []

    for archivo in archivos_dicom:
        dicom_info = obtener_dicom_info(archivo)

        if aplicar_filtros(dicom_info, study_id_filter, patient_id_filter, study_date_filter):
            dicom_info['archivo'] = archivo
            archivos_info.append(dicom_info)

    return render(request, 'archivos/index.html', {'archivos_info': archivos_info,'id_estudio':pk})
    #vistaGeneral.html





# Vista para editar y visualizar un archivo DICOM
def editar_archivo(request, pk,study_id):
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
        'dicom_data': dicom_data,
        'id_estudio': study_id
    })




def ver_vistas_ortogonales(request, archivo_id,study_id):
    archivo = get_object_or_404(DicomFile, pk=archivo_id)

    try:

        dicom_data = io.BytesIO(archivo.dicom_file)
        ds = pydicom.dcmread(dicom_data)

        if hasattr(ds, 'pixel_array'):
            pixel_array = ds.pixel_array

            if pixel_array.ndim == 2:
                pixel_array = np.expand_dims(pixel_array, axis=-1)

            def average_slices(data, axis, num_slices=5):
                if data.shape[axis] > 1:
                    center = data.shape[axis] // 2
                    slices = [data.take(center + i, axis=axis) for i in range(-num_slices // 2, num_slices // 2 + 1)
                              if 0 <= center + i < data.shape[axis]]
                    return np.mean(slices, axis=0)
                else:
                    return data.take(0, axis=axis)

            axial_view = average_slices(pixel_array, axis=0)
            coronal_view = average_slices(pixel_array, axis=1)
            sagittal_view = average_slices(pixel_array, axis=2)

            axial_image = Image.fromarray(normalize_image(axial_view))
            coronal_image = Image.fromarray(normalize_image(coronal_view))
            sagittal_image = Image.fromarray(normalize_image(sagittal_view))

            axial_img_str = image_to_base64(axial_image)
            coronal_img_str = image_to_base64(coronal_image)
            sagittal_img_str = image_to_base64(sagittal_image)
        else:
            return HttpResponse("El archivo DICOM no contiene datos de imagen.")

    except Exception as e:
        return HttpResponse(f"Error al procesar el archivo DICOM: {e}")

    return render(request, 'archivos/vistas_ortogonales.html', {
        'axial_view': axial_img_str,
        'coronal_view': coronal_img_str,
        'sagittal_view': sagittal_img_str,
        'id_estudio':study_id
    })

def normalize_image(view):
    view = view.astype(np.float32)
    view = (view - np.min(view)) / (np.max(view) - np.min(view)) * 255.0
    return view.astype(np.uint8)

def image_to_base64(image):

    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def image_base64(image_array):
    # Convertir la matriz de imagen a una imagen PNG usando PIL
    image = Image.fromarray(image_array)
    image = image.convert('L')  # Convertir a escala de grises si es necesario
    
    # Crear un buffer en memoria para almacenar la imagen en formato PNG
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    
    # Codificar la imagen en base64
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    
    return img_str


def vistas_ortogonales(request,pk):
    estudio = Estudio.objects.get(id=pk)
    archivos_dicom = estudio.dicom_images.all()
    dicom_files =[]
    for arch in archivos_dicom:
        dicom_data = io.BytesIO(arch.dicom_file) 
        dicom_files.append(dicom_data)
    
    slices = [pydicom.dcmread(f) for f in dicom_files]
    slices = sorted(slices, key=lambda x: float(x.ImagePositionPatient[2]))
    image_data = np.stack([s.pixel_array for s in slices], axis=-1)


    x_dim,y_dim,z_dim = image_data.shape
    sagittal_slices =[]
    axial_slices = []
    coronal_slices=[]
    
    for i in range(z_dim):
        axial_slice = image_data[:, :, i]  # Cortar a lo largo del eje Z (tomando todos los valores de X y Y para un valor específico de Z)
        axial_slices.append(image_base64(axial_slice))
        #print(image_base64(axial_slice))

    for i in range(x_dim):
        sagittal_slice = image_data[i, :, :]  # Cortar a lo largo del eje X (tomando todos los valores de Y y Z para un valor específico de X)
        sagittal_slices.append(image_base64(sagittal_slice))

    # Extraer todos los cortes coronales (a lo largo del eje Y)
    for i in range(y_dim):
        coronal_slice = image_data[:, i, :]  # Cortar a lo largo del eje Y (tomando todos los valores de X y Z para un valor específico de Y)
        coronal_slices.append(image_base64(coronal_slice))

    context = {
        'axial_images': axial_slices,
        'sagittal_images': sagittal_slices,
        'coronal_images': coronal_slices,
        'id_estudio':pk,
    }

    return render(request, 'archivos/vistas_ortogonales.html', context)


