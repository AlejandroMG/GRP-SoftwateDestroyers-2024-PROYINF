import os
import pydicom               
from model import DicomModel
from view import DicomView
from PIL import Image
import tkinter as tk
from tkinter import ttk


class DicomController:
    def __init__(self):
        self.model = DicomModel()
        self.view = DicomView(self)
        self.original_image = None

    def run(self):
        self.view.mainloop()

    def open_dicom_folder(self):
        folder_path = self.view.open_folder_dialog()
        if folder_path:
            dicom_files = []
            for root, _, files in os.walk(folder_path):
                for file in files:
                    if file.lower().endswith('.dcm'):
                        dicom_files.append(os.path.join(root, file))

            if not dicom_files:
                self.view.show_info("No se encontraron archivos DICOM en la carpeta seleccionada.")
                return

            self.view.tree.delete(*self.view.tree.get_children())  # Limpiar la tabla antes de agregar nuevos archivos

            for filepath in dicom_files:
                try:
                    dicom_data = pydicom.dcmread(filepath)
                    self.view.tree.insert("", tk.END, values=(os.path.basename(filepath), dicom_data.PatientID, dicom_data.StudyDate))
                except Exception as e:
                    self.view.show_info(f"Error al cargar archivo: {e}")

            self.view.folder_path = folder_path  # Actualizar la ruta de la carpeta en la vista
            self.view.show_info(f"{len(dicom_files)} archivo(s) cargado(s).")

    def convert_to_image(self, dicom_data):
        image_array = dicom_data.pixel_array
        image = Image.fromarray(image_array)
        return image

    def mostrar_info(self,var):
        self.view.show_info(f": {var}")

    #ACTUALIZACIÓN
    def select_dicom_file(self, event):
        selected_item = self.view.tree.selection()
        if selected_item:
            selected_file = self.view.tree.item(selected_item)["values"][0]
            for root, _, files in os.walk(self.view.folder_path):
                if selected_file in files:
                    dicom_path = os.path.join(root, selected_file)
                    
                    self.selected_dicom_path = dicom_path
                    break
            else:
                self.view.show_info(f"Archivo {selected_file} no encontrado en la carpeta.")
                return

            try:
                dicom_data = pydicom.dcmread(dicom_path)
                image = self.convert_to_image(dicom_data)
                self.view.show_image(image)
                self.original_image = image  #Guardar la imagen original

                #Extraer fecha del estudio
                StudyDate = dicom_data.StudyDate if hasattr(dicom_data, 'StudyDate') else "Desconocido"
                self.mostrar_info(StudyDate) 
            except Exception as e:
                self.view.show_info(f"Error al cargar archivo: {e}")


    def get_original_image(self):
        return self.original_image


    #ACTUALIZACIÓN
    def show_dicom_header(self):
        try:
            # Obtener la cabecera DICOM del archivo seleccionado
            dicom_data = pydicom.dcmread(self.selected_dicom_path)

            # Obtener la cabecera DICOM como un diccionario
            dicom_header = {}
            for tag in dicom_data.keys():
                dicom_header[tag] = str(dicom_data[tag].value)

            # Mostrar la cabecera DICOM en la vista
            self.view.show_dicom_header_window(dicom_header)
        except Exception as e:
                print(f"Error al cargar la cabecera DICOM: {e}")

