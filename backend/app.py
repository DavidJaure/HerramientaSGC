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

# Rutas ISO
@app.route("/iso9001")
def iso9001():
    if "usuario" not in session:
        return redirect(url_for("home"))
    return "<h1>Página ISO 9001 (prueba)</h1><a href='/dashboard'>Volver</a>"

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
