from model import DicomModel
from view import DicomView
from PIL import ImageEnhance

class DicomController:
    def __init__(self):
        self.model = DicomModel()
        self.view = DicomView(self)
        self.original_image = None

    def run(self):
        self.view.mainloop()

    def open_dicom_file(self):
        filepath = self.view.open_file_dialog()
        if filepath:
            self.model.load_dicom_file(filepath)
            self.original_image = self.model.get_image()
            self.view.show_image(self.original_image)
            if self.model.dataset != None:
                fecha = self.model.dataset.get("StudyDate", "Desconocido")
                date = "Fecha del estudio: {}".format(fecha)
                self.view.show_info(date)

    
    def mostrar_info(self):
        if self.model.dataset != None:
            fecha = self.model.dataset.get("StudyDate", "Desconocido")
            date = "Fecha del estudio: {}".format(fecha)
            self.view.show_info(date)
            
    
    def get_Original_image(self):
        return self.original_image
    