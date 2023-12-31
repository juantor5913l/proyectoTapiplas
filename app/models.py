from app import db #El punto se reconoce como el archivo "__init__.py" igual el app

#dependencia para fecha y hora
from datetime import datetime

#crear los modelos 
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Text, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin


# Crear una instancia de Base


#dependencia para fecha y hora
from datetime import datetime

#crear los modelos 
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Text, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Crear una instancia de Base


# Modelo para los roles de usuario
class RolUsuario(db.Model):
    __tablename__ = 'rol_usuario'

    id = Column(Integer, primary_key=True)
    nombre_rol = Column(String(255))


# Modelo para usuarios
class Usuario(UserMixin,db.Model):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(255))
    apellido = Column(String(255))
    telefono = Column(String(10))
    correo_electronico = Column(String(255))
    direccion = Column(String(255))
    rol_id = Column(Integer)
    contrasena = Column(String(255))
    codigo_verificacion = Column(String(4))
    contraseña_provisional = db.Column(db.String(100))
    rol_id = Column(Integer, ForeignKey('rol_usuario.id'))

    rol = relationship('RolUsuario', backref='usuarios')



# Modelo para materiales
class Material(db.Model):
    __tablename__ = 'material'

    id = Column(Integer, primary_key=True)
    nombre_material = Column(String(255))
    descripcion = Column(Text)
    precio = Column(DECIMAL(10, 2))
    cantidad_stock = Column(Integer)
    unidad_medida = Column(String(50))
    color = Column(String(50))
    imagen_material = Column(String(50))




# Modelo para cotizaciones
class Cotizacion(db.Model):
    __tablename__ = 'cotizacion'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(255))
    telefono = Column(String(10))
    correo_electronico = Column(String(255))
    ciudad = Column(String(255))
    tipoServicio = Column(String(255))
    detallesAdicionales = Column(String(255))
    incluye = Column(Text)
    precioTotal = Column(DECIMAL(10, 2))

# Modelo para órdenes de servicio
class OrdenServicio(db.Model):
    __tablename__ = 'orden_servicio'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(255))
    telefono = Column(String(10))
    correo_electronico = Column(String(255))
    materialFk = Column(Integer)
    materialFk = Column(Integer, ForeignKey('material.id'))
    material = relationship('Material', backref='orden_servicio')
    tipoServicio = Column(String(255))
    detallesAdicionales = Column(String(255))
    imagen1 = Column(String(50))
    imagen2 = Column(String(50))
    imagen3 = Column(String(50))
    usuario_id = Column(Integer, ForeignKey('usuario.id'))
    usuario = relationship('Usuario', backref='ordenes_servicio')

    

class Catalogo(db.Model):
    __tablename__ = 'catalogo'

    id = Column(Integer, primary_key=True)
    nombre_catalogo = Column(String(255))
    imagen_catalogo = Column(String(50))
