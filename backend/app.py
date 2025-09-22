import os
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from urllib.parse import unquote  

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



#ruta subir plantilla implementacion
@app.route("/iso9001/subir_plantilla", methods=["POST"])
def subir_plantilla():
    archivo = request.files.get("archivo")
    if archivo:
        # Aquí guardas el archivo en tu carpeta correspondiente
        ruta_guardado = os.path.join(PLANTILLAS_DIR, archivo.filename)
        archivo.save(ruta_guardado)
        print("Archivo subido:", archivo.filename)
    return redirect(url_for("plantillas"))


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

@app.route("/iso9001/capacitacion")
def capacitacion():
    return render_template("capacitacion.html")

@app.route("/iso9001/auditoria")
def auditoria():
    return render_template("auditoria.html")

@app.route("/iso9001/implementacion")
def implementacion():
    return render_template("implementacion.html")

@app.route("/guardar_checklist", methods=["POST"])
def guardar_checklist():
    datos = request.form.to_dict()
    print("Checklist recibido:", datos)
    return "Checklist guardado correctamente ✅"

@app.route("/iso9001/evidencias", methods=["POST"])
def subir_evidencias():
    archivo = request.files.get("archivo")
    if archivo:
        print("Archivo recibido:", archivo.filename)
    return "Evidencia subida con éxito."

@app.route("/plantillas")
def plantillas():
    return render_template("plantillas.html")

@app.route("/plantillas/<categoria>/<archivo>")
def descargar_plantilla(categoria, archivo):
    archivo = unquote(archivo)
    ruta = os.path.join(PLANTILLAS_DIR, categoria)
    return send_from_directory(ruta, archivo, as_attachment=True)

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
    app.run(debug=True, host="0.0.0.0", port=5000)
