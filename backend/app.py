import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from flask import Flask, render_template, request, redirect, url_for, session


FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "../frontend")

app = Flask(
    __name__,
    template_folder=os.path.join(FRONTEND_DIR, "templates"),
    static_folder=os.path.join(FRONTEND_DIR, "static")
)

app.secret_key = "super_secret_key"

# Ruta de login (pantalla inicial)
@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

# Procesar login
@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]
    # Login simulado: cualquier correo y contraseña funciona
    session["usuario"] = email
    return redirect(url_for("dashboard"))

# Pantalla principal después del login
@app.route("/dashboard")
def dashboard():
    usuario = session.get("usuario")
    if not usuario:
        return redirect(url_for("home"))  # Si no hay sesión, vuelve al login
    return render_template("dashboard.html", usuario=usuario)

# Logout
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("home"))

# Rutas ISO temporales
@app.route("/iso9001")
def iso9001():
    return "<h1>Página ISO 9001 (prueba)</h1><a href='/dashboard'>Volver</a>"

@app.route("/iso27001")
def iso27001():
    return "<h1>Página ISO 27001 (prueba)</h1><a href='/dashboard'>Volver</a>"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

"""
@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]
    usuario = User.query.filter_by(email=email, password=password).first()
    if usuario:
        session["usuario"] = usuario.nombre
        return redirect(url_for("home"))
    else:
        return "Usuario o contraseña incorrectos", 401
"""
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("home"))

@app.route("/iso9001")
def iso9001():
    return "<h1>Página ISO 9001 (prueba)</h1><a href='/'>Volver</a>"

if __name__ == "__main__":
    print("Templates en:", os.path.join(FRONTEND_DIR, "templates"))
    print("Static en:", os.path.join(FRONTEND_DIR, "static"))
    app.run(debug=True, host="0.0.0.0", port=5000)
