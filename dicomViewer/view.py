import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk

class DicomView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("DICOM Viewer")
        self.geometry("800x600")
        
        self.image_label = tk.Label(self)
        self.image_label.pack(expand=True)

        self.text_init = tk.Label(self,text = "Texto Inicial de Prueba",font=("Arial",24))
        self.text_init.pack(pady=20)


        self.open_button = tk.Button(self, text="Open DICOM File", command=self.controller.open_dicom_file)
        self.open_button.pack(side=tk.LEFT, padx=10, pady=10)


    def show_image(self, image):
        tk_image = ImageTk.PhotoImage(image)
        self.image_label.config(image=tk_image)
        self.image_label.image = tk_image

    def open_file_dialog(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("DICOM files", "*.dcm"), ("All files", "*.*")]
        )
        return filepath
    
    def show_info(self,text1):
        self.text_init.config(text = text1)
