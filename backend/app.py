import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask import send_from_directory #Para las plantillas
from urllib.parse import unquote  # al inicio de tu archivo, si no lo tienes ya

# Carpeta raíz del frontend
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "../frontend")

app = Flask(
    __name__,
    template_folder=os.path.join(FRONTEND_DIR, "templates"),
    static_folder=os.path.join(FRONTEND_DIR, "static")
)

app.secret_key = "super_secret_key"

# ----------------------------
# Usuarios simulados con roles
# ----------------------------
usuarios_simulados = [
    {"nombre": "David", "email": "david@gmail.com", "password": "1234", "rol": "admin"},
    {"nombre": "Ana", "email": "ana@gmail.com", "password": "1234", "rol": "auditor"},
    {"nombre": "Luis", "email": "luis@gmail.com", "password": "1234", "rol": "capacitado"}
]

# ----------------------------
# Rutas
# ----------------------------

# Login / pantalla inicial
@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

# Procesar login
@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    # Verificar usuario simulado
    usuario = next((u for u in usuarios_simulados if u["email"] == email and u["password"] == password), None)
    if usuario:
        session["usuario"] = usuario["nombre"]
        session["rol"] = usuario["rol"]
        return redirect(url_for("dashboard"))
    else:
        return "Usuario o contraseña incorrectos", 401

# Dashboard principal
@app.route("/dashboard")
def dashboard():
    if "usuario" not in session:
        return redirect(url_for("home"))

    usuario = session["usuario"]
    rol = session["rol"]
    return render_template("dashboard.html", usuario=usuario, rol=rol)

# Logout
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    session.pop("rol", None)
    return redirect(url_for("home"))

#boton iso9001

@app.route("/iso9001")
def iso9001():
    if "usuario" not in session:
        return redirect(url_for("home"))
    return render_template("iso9001.html")

@app.route("/iso9001/inicio", methods=["GET", "POST"])
def iso9001_inicio():
    if request.method == "POST":
        datos = request.form.to_dict()
        print("Registro ISO recibido:", datos)

        # Guardamos en sesión de forma temporal
        session['ultimo_registro_iso'] = datos

        # 👉 Aquí en un futuro pondrás la lógica para guardar en la base de datos
        # nuevo_registro = RegistroISO(**datos)
        # db.session.add(nuevo_registro)
        # db.session.commit()

        # Luego redirigimos a opcionesISO9001.html
        return render_template("opcionesISO9001.html", datos=datos)
    return render_template("registroISO.html")


#implementacion
@app.route("/iso9001/implementacion", methods=["GET"])
def implementacion():
    return render_template("implementacion.html")


@app.route("/iso9001/evidencias", methods=["POST"])
def subir_evidencias():
    archivo = request.files.get("archivo")
    if archivo:
        print("Archivo recibido:", archivo.filename)
        # En un futuro lo guardas en una carpeta o BD
    return "Evidencia subida con éxito."

# Carpeta principal de las plantillas
PLANTILLAS_DIR = os.path.join(FRONTEND_DIR, "plantillasISO9001")

# Página que muestra la lista de categorías (opcional)
@app.route("/plantillas")
def plantillas():
    return render_template("plantillas.html")  # luego ajustaremos el HTML para listar dinámicamente

# Descargar archivo por categoría y nombre
@app.route("/plantillas/<categoria>/<archivo>")
def descargar_plantilla(categoria, archivo):
    archivo = unquote(archivo)  # decodifica %20 y signos
    ruta = os.path.join(PLANTILLAS_DIR, categoria)
    print("📂 Buscando archivo en:", ruta)
    print("📄 Archivo solicitado:", archivo)
    return send_from_directory(ruta, archivo, as_attachment=True)






@app.route("/iso9001/objetivos")
def iso9001_objetivos():
    return "<h1>Objetivos ISO 9001</h1>"

@app.route("/iso9001/beneficios")
def iso9001_beneficios():
    return "<h1>Beneficios ISO 9001</h1>"

@app.route("/iso9001/pvha")
def iso9001_pvha():
    return "<h1>Ciclo PHVA (Planear, Hacer, Verificar, Actuar)</h1>"

@app.route("/iso9001/organizacion")
def iso9001_organizacion():
    return "<h1>Organización</h1>"

@app.route("/iso9001/liderazgo")
def iso9001_liderazgo():
    return "<h1>Liderazgo</h1>"

@app.route("/iso9001/planificacion")
def iso9001_planificacion():
    return "<h1>Planificación</h1>"

@app.route("/iso9001/apoyo")
def iso9001_apoyo():
    return "<h1>Apoyo</h1>"

@app.route("/iso9001/operacion")
def iso9001_operacion():
    return "<h1>Operación</h1>"

@app.route("/iso9001/desempeno")
def iso9001_desempeno():
    return "<h1>Desempeño</h1>"

@app.route("/iso9001/mejora")
def iso9001_mejora():
    return "<h1>Mejora</h1>"

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
    app.run(debug=True, host="0.0.0.0", port=5000)



