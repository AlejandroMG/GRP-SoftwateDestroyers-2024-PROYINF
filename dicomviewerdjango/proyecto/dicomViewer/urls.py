from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('archivos/<int:pk>/', views.archivos, name='archivos'),
    path('estudios/',views.estudios,name='verEstudios'),
    path('archivos/subirArchivo/', views.subirArchivo, name='subirArchivo'),
    path('archivos/ver/<int:pk>/<int:study_id>/', views.verArchivo, name='verArchivo'),
    path('archivos/ver/listado/<int:pk>/', views.listadoArchivos, name='verListado'),   # Ruta para ver archivo
    path('eliminar/<int:pk>/<int:study_id>/', views.eliminar_archivo, name='eliminar_archivo'),
    path('editar/<int:pk>/<int:study_id>/', views.editar_archivo, name='editar_archivo'),
    path('archivos/<int:archivo_id>/<int:study_id>/vistas/', views.ver_vistas_ortogonales, name='ver_vistas_ortogonales'),
    path('archivos/<int:pk>/vistas/', views.vistas_ortogonales, name='vistas_ortogonales'),
    path('eliminar/<int:pk>/',views.eliminar_estudio,name='eliminar_estudio'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)