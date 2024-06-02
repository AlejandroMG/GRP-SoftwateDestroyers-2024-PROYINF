import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk


class DicomView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("DICOM Viewer")
        self.geometry("1000x700")
        self.configure(bg="#303030")
        self.folder_path = None  # Añadir atributo folder_path
        self._create_widgets()

    def _create_widgets(self):
        # Frame superior para filtros
        filter_frame = tk.Frame(self, bg="#303030")
        filter_frame.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        # Barra de búsqueda
        tk.Label(filter_frame, text="Barra de búsqueda", bg="#303030", fg="#ffffff", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)
        search_entry = tk.Entry(filter_frame, bg="#ffffff", fg="#000000", font=("Helvetica", 12), bd=0)
        search_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

        # Filtro de fecha
        tk.Label(filter_frame, text="Filtro Fecha", bg="#303030", fg="#ffffff", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)
        date_entry = tk.Entry(filter_frame, bg="#ffffff", fg="#000000", font=("Helvetica", 12), bd=0)
        date_entry.pack(side=tk.LEFT, padx=5, pady=5)

        # ID Paciente
        tk.Label(filter_frame, text="Id Paciente", bg="#303030", fg="#ffffff", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)
        id_entry = tk.Entry(filter_frame, bg="#ffffff", fg="#000000", font=("Helvetica", 12), bd=0)
        id_entry.pack(side=tk.LEFT, padx=5, pady=5)

        # Frame central para la tabla y previsualización
        middle_frame = tk.Frame(self, bg="#303030")
        middle_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)

        # Tabla para mostrar archivos DICOM
        columns = ("Nombre", "ID Paciente", "Fecha")
        self.tree = ttk.Treeview(middle_frame, columns=columns, show="headings", height=10)
        self.tree.heading("Nombre", text="Archivos")
        self.tree.heading("ID Paciente", text="Id_paciente")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Vincular la selección del Treeview al controlador
        self.tree.bind("<ButtonRelease-1>", self.controller.select_dicom_file)

        # Frame para previsualización
        preview_frame = tk.Frame(middle_frame, bg="#303030")
        preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        # Previsualización de la imagen
        tk.Label(preview_frame, text="Previsualización", bg="#303030", fg="#ffffff", font=("Helvetica", 12)).pack(pady=5)
        self.image_label = tk.Label(preview_frame, bg="#404040")
        self.image_label.pack(fill=tk.BOTH, expand=True)

        # Etiqueta de información
        self.info_label = tk.Label(self, text="", font=("Helvetica", 12), bg="#303030", fg="#ffffff")
        self.info_label.pack(pady=10)

        # Botón para abrir archivos DICOM
        self.open_button = tk.Button(self, text="Abrir carpeta DICOM", command=self.controller.open_dicom_folder, bg="#007bff", fg="#ffffff", font=("Helvetica", 14))
        self.open_button.pack(side=tk.BOTTOM, pady=10)

    def show_image(self, image):
        tk_image = ImageTk.PhotoImage(image)
        self.image_label.config(image=tk_image)
        self.image_label.image = tk_image

    def open_folder_dialog(self):
        folder_path = filedialog.askdirectory(title="Selecciona una carpeta que contenga archivos DICOM")
        self.folder_path = folder_path  # Actualizar folder_path
        return folder_path

    def show_info(self, text1):
        self.info_label.config(text=text1)
