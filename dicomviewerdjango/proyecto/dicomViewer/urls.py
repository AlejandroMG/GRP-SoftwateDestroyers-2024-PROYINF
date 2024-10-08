from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('archivos/', views.archivos, name='archivos'),
    path('archivos/subirArchivo/', views.subirArchivo, name='subirArchivo'),
    path('archivos/ver/<int:pk>/', views.verArchivo, name='verArchivo'),  # Ruta para ver archivo
    path('eliminar/<int:pk>/', views.eliminar_archivo, name='eliminar_archivo'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)