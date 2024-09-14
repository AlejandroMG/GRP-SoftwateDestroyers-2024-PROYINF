from django.shortcuts import render

#Aregado
def main(request):
    return render(request, 'DICOM_viewer.html')

