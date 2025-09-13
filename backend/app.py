import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from flask import Flask, render_template, request, redirect, url_for, session


# Carpeta raíz del frontend
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "../frontend")

app = Flask(
    __name__,
    template_folder=os.path.join(FRONTEND_DIR, "templates"),  # ← aquí van tus templates
    static_folder=os.path.join(FRONTEND_DIR, "static")       # ← aquí van tus archivos estáticos
)

app.secret_key = "super_secret_key"

# 🔹 conexión a MySQL remoto (ajusta tus credenciales)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://usuario:password@host/nombre_bd"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo usuario
class User(db.Model):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

# Rutas
@app.route("/")
def home():
    return render_template("home.html", usuario=session.get("usuario"))

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

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    print("Templates en:", os.path.join(FRONTEND_DIR, "templates"))
    print("Static en:", os.path.join(FRONTEND_DIR, "static"))
    app.run(debug=True, host="0.0.0.0", port=5000)
