import os
import pydicom               
from model import DicomModel
from view import DicomView
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk


class DicomController:
    def __init__(self):
        self.model = DicomModel()
        self.view = DicomView(self)
        self.original_image = None
        self.dicom_files = []  # Lista para almacenar los datos DICOM cargados
        self.filtered_files = []  # Lista para almacenar los datos DICOM filtrados

    def run(self):
        self.view.mainloop()

    def apply_filters(self):
        search_filter = self.view.search_entry.get().lower()
        date_filter = self.view.date_entry.get()
        id_filter = self.view.id_entry.get()
        self.update_treeview(search_filter, date_filter, id_filter)

    def update_treeview(self, search_filter, date_filter, id_filter):
        self.view.tree.delete(*self.view.tree.get_children())  # Limpiar la tabla antes de agregar nuevos archivos

        # Filtrar los datos DICOM por los filtros especificados
        self.filtered_files = [dicom for dicom in self.dicom_files if
                               (search_filter in dicom["Archivos"].lower() if search_filter else True) and
                               (dicom["Fecha"] == date_filter if date_filter else True) and
                               (id_filter in dicom["Id_paciente"] if id_filter else True)]

        # Actualizar la tabla con los datos filtrados
        for dicom in self.filtered_files:
            self.view.tree.insert("", tk.END, values=(dicom["Archivos"], dicom["Id_paciente"], dicom["Fecha"]))


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

            self.dicom_files = []  # Limpiar la lista antes de agregar nuevos archivos
            for filepath in dicom_files:
                try:
                    dicom_data = pydicom.dcmread(filepath)
                    dicom_entry = {
                        "Archivos": os.path.basename(filepath),
                        "Id_paciente": dicom_data.PatientID,
                        "Fecha": dicom_data.StudyDate if hasattr(dicom_data, 'StudyDate') else "Desconocido",
                        "FilePath": filepath  # Agregar la ruta del archivo
                    }
                    self.dicom_files.append(dicom_entry)
                except Exception as e:
                    self.view.show_info(f"Error al cargar archivo: {e}")

            self.update_treeview("", "", "")  # Mostrar todos los archivos inicialmente
            self.view.folder_path = folder_path  # Actualizar la ruta de la carpeta en la vista
            self.view.show_info(f"{len(dicom_files)} archivo(s) cargado(s).")

    def convert_to_image(self, dicom_data):
        image_array = dicom_data.pixel_array
        image = Image.fromarray(image_array)
        return image

    def mostrar_info(self, var):
        self.view.show_info(f": {var}")

    def select_dicom_file(self, event):
        selected_item = self.view.tree.selection()
        if selected_item:
            selected_file = self.view.tree.item(selected_item)["values"][0]
            selected_file_path = next((dicom["FilePath"] for dicom in self.filtered_files if dicom["Archivos"] == selected_file), None)

            if not selected_file_path:
                self.view.show_info(f"Archivo {selected_file} no encontrado en la carpeta.")
                return

            try:
                dicom_data = pydicom.dcmread(selected_file_path)
                image = self.convert_to_image(dicom_data)
                self.view.show_image(image)
                self.original_image = image  # Guardar la imagen original

                # Extraer fecha del estudio
                StudyDate = dicom_data.StudyDate if hasattr(dicom_data, 'StudyDate') else "Desconocido"
                self.mostrar_info(StudyDate)

                # Guardar la ruta seleccionada para la cabecera DICOM
                self.selected_dicom_path = selected_file_path

            except Exception as e:
                self.view.show_info(f"Error al cargar archivo: {e}")

    def get_original_image(self):
        return self.original_image

    def show_dicom_header(self):
        try:
            if hasattr(self, 'selected_dicom_path') and self.selected_dicom_path:
                dicom_data = pydicom.dcmread(self.selected_dicom_path)
                dicom_header = {tag: str(dicom_data[tag].value) for tag in dicom_data.keys()}
                self.view.show_dicom_header_window(dicom_header)
            else:
                self.view.show_info("No se ha seleccionado ningún archivo DICOM.")
        except Exception as e:
            self.view.show_info(f"Error al cargar la cabecera DICOM: {e}")

    def show_full_image(self):
        if self.original_image:
            full_image_window = tk.Toplevel(self.view)
            full_image_window.title("Imagen Completa")
            tk_image = ImageTk.PhotoImage(self.original_image)
            image_label = tk.Label(full_image_window, image=tk_image)
            image_label.image = tk_image  
            image_label.pack(fill=tk.BOTH, expand=True)


