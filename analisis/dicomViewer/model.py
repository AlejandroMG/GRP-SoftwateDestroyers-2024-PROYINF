import pydicom
from PIL import Image

class DicomModel:
    def __init__(self):
        self.filepath = None
        self.dataset = None
        self.image = None

    def load_dicom_file(self, filepath):
        self.filepath = filepath
        self.dataset = pydicom.dcmread(filepath)
        pixel_array = self.dataset.pixel_array
        self.image = Image.fromarray(pixel_array).convert("L")

    def get_image(self):
        return self.image
    
