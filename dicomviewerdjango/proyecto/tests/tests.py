import unittest
import requests
import pydicom
import os
from PIL import Image

class TestDicomFile(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url = 'http://127.0.0.1:8000/archivos/subirArchivo/'
        cls.valid_dicom_file_path = 'test.dcm'
        cls.invalid_file_path = 'testinvalid.txt'
    
    @classmethod
    def tearDownClass(cls):
        if os.path.exists('test.png'):
            os.remove('test.png')

    # Endpoint 1: Verificación de archivos DICOM válidos/inválidos
    def test_valid_dicom_file(self):
        """Test para verificar si el archivo DICOM es válido."""
        with open(self.valid_dicom_file_path, "rb") as file:
            response = requests.post(self.url, files={"file": file})
            
            # Verificar que la respuesta sea 200 OK
            self.assertEqual(response.status_code, 200, f"Respuesta inesperada: {response.status_code}")
    
    def test_upload_invalid_file(self):
        #Prueba de un archivo inválido.
        with open(self.invalid_file_path, "rb") as file:
            response = requests.post(self.url, files={"file": file})
            self.assertEqual(response.status_code, 400)
            self.assertIn("error", response.json().get("message", "").lower())
            

class DICOMConversionTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        current_dir = os.getcwd()
        cls.dicom_file_path = os.path.join(current_dir, 'test.dcm')
        cls.png_file_path = os.path.join(current_dir, 'test.png')

    @classmethod
    def tearDownClass(cls):
        # Eliminar el archivo PNG después de la prueba
        if os.path.exists(cls.png_file_path):
            os.remove(cls.png_file_path)

    def test_dicom_to_png_conversion(self):
        #Verifica que el archivo DICOM puede ser convertido a un formato de imagen PNG.
        try:
            dicom = pydicom.dcmread(self.dicom_file_path)
            # Obtener el array de píxeles de la imagen
            pixel_array = dicom.pixel_array

            # Crear una imagen a partir del array de píxeles
            img = Image.fromarray(pixel_array)

            # Guardar como PNG
            img.save(self.png_file_path)

            # Verificar que el archivo PNG ha sido creado
            self.assertTrue(os.path.exists(self.png_file_path))
        except Exception as e:
            self.fail(f"No se pudo convertir el archivo DICOM a PNG: {e}")
class TestDicomMetadataExtraction(unittest.TestCase):
    def setUp(self):
        # Definir la ruta del archivo DICOM de prueba
        self.dicom_path = 'test.dcm'
        
        # Verificar si el archivo existe antes de correr la prueba
        self.assertTrue(os.path.exists(self.dicom_path))
        
        # Leer el archivo DICOM
        self.dicom = pydicom.dcmread(self.dicom_path)

    def test_patient_name(self):
        # Verificar el nombre del paciente en los metadatos del archivo DICOM
        expected_patient_name = 'Test^Patient'  # Ajusta este valor según el archivo de prueba
        actual_patient_name = self.dicom.PatientName
        self.assertEqual(actual_patient_name, expected_patient_name)

    def test_image_dimensions(self):
        # Verificar las dimensiones de la imagen (ejemplo de metadato)
        expected_rows = 512  # Ajusta según el archivo de prueba
        expected_columns = 512  # Ajusta según el archivo de prueba
        actual_rows = self.dicom.Rows
        actual_columns = self.dicom.Columns
        self.assertEqual(actual_rows, expected_rows)
        self.assertEqual(actual_columns, expected_columns)

    def test_modality(self):
        # Verificar que la modalidad del archivo DICOM sea la esperada (ej. CT, MR)
        expected_modality = 'CT'  # Ajusta según el archivo de prueba
        actual_modality = self.dicom.Modality
        self.assertEqual(actual_modality, expected_modality)




class TestDicomFileDeletion(unittest.TestCase):

    def setUp(self):
        # Crear un archivo DICOM temporal para la prueba
        self.test_dicom_path = 'test1.dcm'
        with open(self.test_dicom_path, 'wb') as f:
            f.write(b'Test DICOM file content')  # Contenido simulado de archivo DICOM

        # Verificar que el archivo fue creado correctamente
        self.assertTrue(os.path.exists(self.test_dicom_path))

    def test_delete_dicom_file(self):
        # Función que elimina el archivo (debería ser parte de tu aplicación)
        self.delete_dicom_file(self.test_dicom_path)

        # Verificar que el archivo ya no exista
        self.assertFalse(os.path.exists(self.test_dicom_path))

    def delete_dicom_file(self, filepath):
        """Simular la función que elimina el archivo DICOM."""
        if os.path.exists(filepath):
            os.remove(filepath)

    def tearDown(self):
        # Limpiar el entorno de prueba por si el archivo no se eliminó durante la prueba
        if os.path.exists(self.test_dicom_path):
            os.remove(self.test_dicom_path)
if __name__ == '__main__':
    unittest.main()
