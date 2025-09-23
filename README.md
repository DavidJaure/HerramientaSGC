#ISO 9001 Quality Management System - Flask Web Application

Este proyecto es una aplicación web desarrollada con Flask para facilitar la implementación y auditoría de un Sistema de Gestión de Calidad ISO 9001 en una empresa. Permite gestionar plantillas, realizar auditorías, registrar capacitaciones y generar informes en formato PDF.

##Características principales

###Gestión de usuarios: Roles simulados de administrador, auditor y capacitado para acceder a diferentes funcionalidades.

###Gestión de plantillas: Subida, descarga y seguimiento de plantillas de implementación de ISO 9001.

###Auditorías: Realiza auditorías de calidad, marca checklist y genera observaciones.

###Generación de informes PDF: Crea un informe de auditoría en formato PDF que incluye datos sobre la implementación y observaciones del auditor.

###Capacitación: Seguimiento de capacitaciones relacionadas con la implementación de ISO 9001.

#Requisitos

Python 3.x

Flask

fpdf

WeasyPrint

Instalación

##Clona el repositorio:

git clone https://github.com/tu-usuario/iso9001-flask-app.git
cd iso9001-flask-app


##Instala las dependencias:
Se recomienda crear un entorno virtual para gestionar las dependencias:

python3 -m venv venv
source venv/bin/activate  # En Linux/Mac
venv\Scripts\activate  # En Windows


Luego, instala las dependencias necesarias:

pip install -r requirements.txt


##Configuración:

Asegúrate de tener una estructura de carpetas como la siguiente:

├── frontend/
    ├── plantillasISO9001/
    ├── static/
    └── templates/
├── app.py
├── requirements.txt


Si no tienes requirements.txt, crea uno usando:

pip freeze > requirements.txt


Ejecuta la aplicación:

python app.py


La aplicación debería estar disponible en http://localhost:5001.

Rutas disponibles

/: Página de inicio.

/login: Formulario de inicio de sesión para acceder a la aplicación (usuario: "admin", "auditor", "capacitado").

/dashboard: Dashboard del usuario no admin.

/dashboard_admin: Dashboard para administradores.

/registro_iso: Registro de implementación de ISO 9001 para administradores.

/iso9001/implementacion: Gestión de plantillas de implementación ISO 9001.

/iso9001/subir_plantilla: Subir nuevas plantillas de implementación.

/iso9001/descargar/<nombre>: Descargar plantillas de implementación.

/iso9001/capacitacion: Visualizar capacitaciones y plantillas completadas.

/iso9001/auditoria: Realizar auditorías de calidad.

/generar_pdf: Generar y descargar un informe de auditoría en PDF.

Cómo usar la aplicación

Iniciar sesión:

Inicia sesión como uno de los siguientes usuarios:

Admin: Email: david@gmail.com, Contraseña: 1234

Auditor: Email: ana@gmail.com, Contraseña: 1234

Capacitado: Email: luis@gmail.com, Contraseña: 1234

Gestión de plantillas:

Como admin, puedes subir nuevas plantillas de implementación desde /iso9001/implementacion.

Los usuarios pueden ver y descargar las plantillas completadas.

Auditorías:

Los auditores pueden acceder a /iso9001/auditoria para completar un checklist de auditoría y dejar observaciones.

Al completar la auditoría, pueden generar un informe en PDF accediendo a /generar_pdf.

Capacitación:

Los administradores pueden gestionar las capacitaciones en /iso9001/capacitacion, donde pueden ver los documentos completados y las capacitaciones en curso.

Generación de informes PDF

Al finalizar una auditoría, se puede generar un informe en PDF con los resultados de la auditoría, las plantillas implementadas y las observaciones del auditor.

Tecnologías utilizadas

Flask: Framework web para Python.

FPDF: Biblioteca para generar PDFs (para el informe de auditoría).

WeasyPrint: Para generar PDFs a partir de HTML.

HTML/CSS: Plantillas web para la interfaz de usuario.

JavaScript: Para la interacción con el front-end (opcional).

Contribuir

Fork del repositorio.

Crea tu rama de trabajo (git checkout -b feature-nueva-funcionalidad).

Haz commit de tus cambios (git commit -am 'Agrega nueva funcionalidad').

Push a tu rama (git push origin feature-nueva-funcionalidad).

Crea un Pull Request para que los cambios sean revisados y aceptados.

Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.