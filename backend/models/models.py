from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, Date

db = SQLAlchemy()

# ---------------------------
# Usuario con roles
# ---------------------------
class User(db.Model):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    rol = Column(String(20), nullable=False, default="auditor")  # admin, auditor, capacitado

# ---------------------------
# Auditoría ISO
# ---------------------------
class Auditoria(db.Model):
    __tablename__ = "auditorias"
    id = Column(Integer, primary_key=True)
    titulo = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    fecha = Column(Date, nullable=False)
    responsable_id = Column(Integer, db.ForeignKey("usuarios.id"))

# ---------------------------
# Cursos de capacitación
# ---------------------------
class Curso(db.Model):
    __tablename__ = "cursos"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    duracion_horas = Column(Integer, nullable=False)
