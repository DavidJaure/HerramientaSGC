import os
from flask import Flask, render_template, request, redirect, url_for, session

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

@app.route("/iso9001/inicio")
def iso9001_inicio():
    return "<h1>Inicio: Implementación, Auditoría y Capacitación</h1>"

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



# ----------------------------
# Formulario implementación
# ----------------------------
@app.route("/registro", methods=["GET", "POST"])
def registro_iso():
    if request.method == "POST":
        # Aquí capturas los datos enviados desde el formulario
        datos = request.form.to_dict()
        print("Datos recibidos:", datos)  # temporal (muestra en consola)
        return redirect(url_for("dashboard"))  # después de guardar, volver al dashboard
    return render_template("registro.html")

#boton iso9001
@app.route("/iso9001")
def iso9001():
    return render_template("iso9001.html")

@app.route("/iso9001/inicio")
def iso9001_inicio():
    return "<h1>Inicio: Implementación, Auditoría y Capacitación</h1>"

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
