# Grupo SoftwareDestroyers 2.0

Integrantes:  
* Alejandro Fierro - 202173600-k  
* Cristobal Pino - 202104597-k  
* Jorge Toro - 202173613-1  
* Nicolas Horta - 202173532-1  

# Proyecto a trabajar:
Visualizador de imágenes DICOM, barra de búsqueda.

# Wiki
Podrá acceder a la wiki mediante el siguiente [enlace](https://github.com/AlejandroMG/GRP-SoftwateDestroyers-2024-PROYINF/wiki)

# Hito 2 notas:
Se ha elegido la historia de usuario:
<HU-400: Subir imágenes DICOM al sitio web> como HU prioritaria, dentro de ella se puede encontrar su justificación.  

# Hito 3 Notas:
* Progreso <HU-400: Subir imágenes DICOM al sitio web>: se ha podido incorporar un visor de imagenes de archivos DICOM en el sitio web. Se incluye una sección donde el usuario puede acceder a cualquiera de los archivos que subió.
* Se eligieron las historias de usuario <HU-500: Ampliar y reducir Imagen DICOM (Zoom)> y <HU-600: Herramientas que permitan el cambio de contraste, imagen en negativo y el uso de distintos tipos de mapas de colores.> como las HU's con mayor prioridad de las pendientes. Tienen comentarios dentro de su respectiva issue (HU).  
* Justificacion: Se han escogido las HU-400 y HU-600, zoom y filtros respectivamente debido a que son un poco más rápidas de implementar y aportan suficiente valor al proyecto, completando así una versión mas completa y dejando el tiempo restante para abordar con mayor enfoque las HU mas complejas.   
* Las pruebas unitarias verifican el funcionamiento de poder subir archivos al sitio web y si se aplican filtros a una imagen de manera correcta.
* Las pruebas unitarias se encuentran en la carpeta tests dentro del proyecto.

# Hito 4 Notas:  
* Progreso <HU-700: Herramientas de Edición y Visualización de Imagen>: Se agregó una sección nueva a cada archivo DICOM que permite trazar 3 tipos de figuras geometricas, luego le entregará información relevante de la región seleccionada (area, perimetro, diametro, etc.).
* El sitio web ahora cuenta con una barra de búsqueda.
* Se ha actualizado la Wiki agregando concerns, trade-offs y otra sección para la iteración/evaluación de HUs.
* Se agrega la evalucación de pruebas y modificaciones.
* Nos reunimos con el cliente nuevamente para evaluar el progreso y discutir que se podría agregar/modificar.

# Hito 5 Notas:
* Se planificó y aplicó un plan de pruebas con Apache jmeter, se midieron los tiempos de respuesta para muchos usuarios consultando la app. Se presentan los gráficos de resultados que muestran la latencia de los procesos y en que casos no se logró el tiempo de respuesta máximo de 1 segundo.
* En la direccion dicomviewerdjango/inspections/v1.0 se incluyeron capturas de pantalla sobre la inspección de código usando el sitio web Sonarqube. Elegimos 2 'issues': definir una constante en lugar de repetir un prompt varias veces y reducir la complejidad de una función auxiliar en el código.
* Actualizamos la sección de Story Point HU en la Wiki con nuestro análisis sobre la escala utilizada y nuestra justificación por las estimaciones de las HU.
* Progreso <HU-800: Visualizar un volumen en las 3 direcciones ortogonales>: Se incorporó un botón en la vista de un estudio que permite cambiar de  solo una vista a las 3 vistas ortogonales. Cada vista funciona por separado, por lo que se puede elegir distintos fotogramas en cada vista.
* Ahora al cargar archivos DICOM la sitio web se pide un "estudio" en vez de un solo archivo. Esto quiere decir que se incntiva subir una carpeta de archivos de un mismo estudio, ya que de esta forma se podrán ver todos en una sola página que permite usar un slider para elegir un fotograma específico.
