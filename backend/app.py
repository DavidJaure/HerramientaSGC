import os, io
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, send_file, make_response
from urllib.parse import unquote  
from fpdf import FPDF
from datetime import datetime
from weasyprint import HTML
# ----------------------------
# Configuración
# ----------------------------
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "../frontend")
PLANTILLAS_DIR = os.path.join(FRONTEND_DIR, "plantillasISO9001")

app = Flask(
    __name__,
    template_folder=os.path.join(FRONTEND_DIR, "templates"),
    static_folder=os.path.join(FRONTEND_DIR, "static")
)
app.secret_key = "super_secret_key"

# ----------------------------
# Usuarios simulados
# ----------------------------
usuarios_simulados = [
    {"nombre": "David", "email": "david@gmail.com", "password": "1234", "rol": "admin"},
    {"nombre": "Ana", "email": "ana@gmail.com", "password": "1234", "rol": "auditor"},
    {"nombre": "Luis", "email": "luis@gmail.com", "password": "1234", "rol": "capacitado"}
]

# Flag de registro ISO (solo para admin)
registro_completo = False

# ----------------------------
# Rutas
# ----------------------------

@app.route("/")
def home():
    return render_template("home.html")  

@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    usuario = next((u for u in usuarios_simulados if u["email"] == email and u["password"] == password), None)
    if usuario:
        session["usuario"] = usuario["nombre"]
        session["rol"] = usuario["rol"]

        if usuario["rol"] == "admin":
            if not registro_completo:
                return redirect(url_for("registro_iso"))
            return redirect(url_for("dashboard_admin"))
        else:
            return redirect(url_for("dashboard"))
    else:
        return "Usuario o contraseña incorrectos", 401

@app.route("/dashboard")
def dashboard():
    if "usuario" not in session or session.get("rol") == "admin":
        return redirect(url_for("home"))
    return render_template("dashboard.html", usuario=session["usuario"])

@app.route("/dashboard_admin")
def dashboard_admin():
    if session.get("rol") != "admin":
        return redirect(url_for("home"))
    return render_template("dashboard_admin.html")

@app.route("/registro_iso", methods=["GET", "POST"])
def registro_iso():
    global registro_completo
    if session.get("rol") == "admin":
        if registro_completo:
            return redirect(url_for("dashboard_admin"))
        
        if request.method == "POST":
            # Guardar formulario en DB (simulado)
            registro_completo = True
            return redirect(url_for("dashboard_admin"))
        
        return render_template("registroISO.html")
    
    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))



PLANTILLAS_DIR = "plantillas/implementacion"  # carpeta donde guardas los archivos

PLANTILLAS_DIR = "plantillas/implementacion"

# Datos de ejemplo: nombre_id (para tu JS) y si está completada
plantillas_ejemplo = [
    {"id": "alcance", "nombre": "Plantilla Alcance formato.xlsx", "completada": True},
    {"id": "mapa", "nombre": "Mapa de Procesos formato.xlsx", "completada": False},
    {"id": "ficha", "nombre": "Ficha de Procesos formato.xlsx", "completada": True},
    {"id": "partes", "nombre": "Plantilla Partes interesadas.xlsx", "completada": False},
    {"id": "foda", "nombre": "Plantilla FODA formato.xlsx", "completada": True},
    {"id": "pestal", "nombre": "Plantilla PESTAL formato.xlsx", "completada": False},
    {"id": "fuerzas", "nombre": "Plantilla 5 Fuerzas Porter.xlsx", "completada": True},
    {"id": "liderazgo1", "nombre": "Checklist Liderazgo.xlsx", "completada": True},
    {"id": "liderazgo2", "nombre": "Plantilla Política de Calidad.xlsx", "completada": False},
    {"id": "indicadores1", "nombre": "Multiplantilla Indicadores por Área.xlsx", "completada": True},
    {"id": "indicadores2", "nombre": "Seguimiento Medición.xlsx", "completada": False},
    {"id": "operacion1", "nombre": "Planificación y Control Operacional.xlsx", "completada": True},
    {"id": "planificacion1", "nombre": "Objetivos de Calidad.xlsx", "completada": False},
    {"id": "soporte1", "nombre": "Medición de Condiciones Físicas.xlsx", "completada": True},
]

@app.route("/iso9001/implementacion")
def implementacion():
    return render_template("implementacion.html", plantillas=plantillas_ejemplo)

# Subir plantilla
@app.route("/iso9001/subir_plantilla", methods=["POST"])
def subir_plantilla():
    archivo = request.files.get("archivo")
    if archivo:
        ruta_guardado = os.path.join(PLANTILLAS_DIR, archivo.filename)
        archivo.save(ruta_guardado)
        print("Archivo subido:", archivo.filename)
        # Actualizar estado en los datos de ejemplo
        for p in plantillas_ejemplo:
            if p["nombre"] == archivo.filename:
                p["completada"] = True
    return redirect(url_for("implementacion"))

# Descargar plantilla (simulación)
@app.route("/iso9001/descargar/<nombre>")
def descargar(nombre):
    ruta_archivo = os.path.join(PLANTILLAS_DIR, nombre)
    if os.path.exists(ruta_archivo):
        return f"Descargando {nombre}..."  # Simulación
    return "Archivo no encontrado"

@app.route("/iso9001/descargar/<categoria>/<archivo>")
def descargar_plantilla(categoria, archivo):
    ruta_archivo = os.path.join(FRONTEND_DIR, "plantillasISO9001", categoria, archivo)
    if os.path.exists(ruta_archivo):
        return send_from_directory(
            os.path.join(FRONTEND_DIR, "plantillasISO9001", categoria),
            archivo,
            as_attachment=True
        )
    return "Archivo no encontrado"



# ----------------------------
# ISO 9001
# ----------------------------
@app.route("/iso9001")
def iso9001():
    if "usuario" not in session:
        return redirect(url_for("home"))
    return render_template("iso9001.html")

@app.route("/iso9001/inicio", methods=["GET", "POST"])
def iso9001_inicio():
    if request.method == "POST":
        datos = request.form.to_dict()
        session['ultimo_registro_iso'] = datos
        return render_template("opcionesISO9001.html", datos=datos)
    return render_template("registroISO.html")

from flask import render_template, session

#Capacitacionea
@app.route("/iso9001/capacitacion")
def capacitacion():
    # lista de documentos completados (puede venir de la base de datos)
    plantillas_completadas = ['Política de Calidad', 'Objetivos de Calidad', 'FODA']

    # lista de capacitaciones existentes
    capacitaciones = get_capacitaciones()  # función que retorna los registros

    return render_template(
        "capacitacion.html",
        plantillas_completadas=plantillas_completadas,
        capacitaciones=capacitaciones,
        rol=session.get("rol", "capacitado")  # opcional, si quieres pasar el rol al template
    )

#Capacitaciones con BD
#def get_capacitaciones():
    # Ejemplo: consulta a la tabla capacitaciones
   # result = db.session.execute("SELECT * FROM capacitaciones")
    # Convierte a lista de diccionarios
   # return [dict(row) for row in result]

#Eejemplo get sin base de datos
def get_capacitaciones():
    return [
        {
            "responsable": "Carlos Pérez",
            "persona": "Ana Gómez",
            "documento": "Política de Calidad",
            "fecha": "2025-09-30",
            "objetivo": "Fortalecer conocimiento en ISO 9001",
            "evidencia": False
        },
        {
            "responsable": "Luis Martínez",
            "persona": "Juan Torres",
            "documento": "FODA",
            "fecha": "2025-10-05",
            "objetivo": "Analizar fortalezas y debilidades",
            "evidencia": True
        }
    ]



# Datos de ejemplo: responsables de cada capítulo
capacitaciones = [
    {"responsable": "Carlos Pérez"},
    {"responsable": "Ana Gómez"},
    {"responsable": "Luis Ramírez"},
]
# Datos de ejemplo: plantillas completadas
plantillas_implementacion = [
    {"nombre": "Alcance", "completada": True, "fecha": "2025-09-22"},
    {"nombre": "Mapa de Procesos", "completada": False, "fecha": ""},
    {"nombre": "Ficha de Procesos", "completada": True, "fecha": "2025-09-20"},
    {"nombre": "Partes Interesadas", "completada": True, "fecha": "2025-09-21"},
]

@app.route("/iso9001/auditoria", methods=["GET", "POST"])
def auditoria():
    if request.method == "POST":
        # Recoger checklist marcado
        checklist_completado = {key: True if request.form.get(key) == "on" else False for key in request.form if key != "observaciones"}
        observaciones = request.form.get("observaciones")
        fecha = datetime.now().strftime("%Y-%m-%d")
        print("Checklist:", checklist_completado)
        print("Observaciones:", observaciones)
        print("Fecha de auditoría:", fecha)
        # Aquí se podría generar PDF
        return redirect(url_for("auditoria"))

    return render_template(
        "auditoria.html",
        plantillas=plantillas_implementacion,
        fecha=datetime.now().strftime("%Y-%m-%d")
    )

checklist_example = {
    "4.1": True, "4.2": True, "4.3": True, "4.4": False,
    "5.1": True, "5.2": False, "5.3": True,
}

@app.route("/generar_pdf")
def generar_pdf():
    # Datos de auditor (ejemplo)
    auditor = {
        "nombre": "Luis",
        "correo": "Luis@gmail.com"
    }

    # Datos de la empresa
    empresa = {
        "Registro": "ISO 9001",
        "Razón Social": "Empresa Ejemplo S.A.S.",
        "NIT": "900.123.456-7",
        "Representante Legal": "Juan Pérez",
        "Sector Económico": "Tecnología",
        "Tipo de Empresa": "Sociedad por Acciones Simplificada",
        "Dirección": "Calle Falsa 123, Bogotá",
        "Teléfonos": "+57 1 2345678 / +57 300 1234567",
        "Número de Empleados": "45",
        "E-mail": "contacto@empresa.com",
        "Web": "www.empresa.com",
        "Facebook": "facebook.com/empresa",
        "Instagram": "instagram.com/empresa"
    }

    # Checklist completo
    checklist_example = {
        "4.1": True, "4.2": False, "4.3": True, "4.4": True,
        "5.1": True, "5.2": False, "5.3": True,
        "6.1": True, "6.2": True, "6.3": False,
        "7.1": True, "7.2": True, "7.3": True, "7.4": False, "7.5": True,
        "8.1": True, "8.2": True, "8.3": False, "8.4": True, "8.5": True, "8.6": False, "8.7": True,
        "9.1": True, "9.2": True, "9.3": True,
        "10.1": True, "10.2": False, "10.3": True
    }

    # Plantillas de implementación
    plantillas_implementacion = [
        {"nombre": "Plantilla Alcance", "completada": True, "fecha": "2025-09-22"},
        {"nombre": "Mapa de Procesos", "completada": True, "fecha": "2025-09-21"},
        {"nombre": "Ficha de Procesos", "completada": True, "fecha": "2025-09-20"},
        {"nombre": "Registro de Capacitación", "completada": False, "fecha": None},
        {"nombre": "Matriz de Riesgos", "completada": True, "fecha": "2025-09-19"}
    ]

    observaciones = "Aquí van las observaciones completas del auditor sobre la implementación del SGC."

    # Renderizar HTML para PDF
    html_content = render_template(
        "auditoria_pdf.html",
        auditor=auditor,
        empresa=empresa,
        checklist=checklist_example,
        plantillas=plantillas_implementacion,
        observaciones=observaciones,
        fecha=datetime.now().strftime('%Y-%m-%d')
    )

    pdf = HTML(string=html_content).write_pdf()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=Informe_Auditoria_Empresa.pdf'
    return response


# ----------------------------
# ISO 27001 (placeholder)
# ----------------------------
@app.route("/iso27001")
def iso27001():
    if "usuario" not in session:
        return redirect(url_for("home"))
    return "<h1>Página ISO 27001 (prueba)</h1><a href='/dashboard'>Volver</a>"

# ----------------------------
# Ejecutar app
# ----------------------------
if __name__ == "__main__":
    print("Templates en:", os.path.join(FRONTEND_DIR, "templates"))
    print("Static en:", os.path.join(FRONTEND_DIR, "static"))
    app.run(debug=True, host="0.0.0.0", port=5001)
