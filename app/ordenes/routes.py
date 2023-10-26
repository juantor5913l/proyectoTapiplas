from datetime import datetime
from flask import abort, redirect, render_template, request, url_for
from . import ordenes_blueprint
import app 

import os
from werkzeug.utils import secure_filename 
from random import sample

@ordenes_blueprint.route('/listar')
def listar_ordenes():
    ordenes = app.models.OrdenServicio.query.all()
    return render_template('listar_ordenes.html', ordenes=ordenes)



@ordenes_blueprint.route('/mostrar/<int:id>')
def mostrar_registro(id):
    usuario = app.models.Usuario.query.get(id)
    if usuario is None:
        abort(404)  # Manejo de error si el cliente no existe

    ordenes = usuario.ordenes_servicio  # Obtiene las órdenes de servicio relacionadas con el cliente
    return render_template('listar_ordenesCliente.html',usuario=usuario, ordenes=ordenes)


# Ruta para agregar una nueva orden de servicio (CREATE)

@ordenes_blueprint.route('/agregar/<int:id>', methods=['GET', 'POST'])
def agregar_orden(id):
    usuario = app.models.Usuario.query.get(id)
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        correo_electronico = request.form['correo_electronico']
        materialFk =  request.form['materialFk']
        if(request.files['imagen1'] !=''):
            file     = request.files['imagen1'] #recibiendo el archivo
            imagen_1 = recibeFoto(file)
        if(request.files['imagen2'] !=''):
            file     = request.files['imagen2'] #recibiendo el archivo
            imagen_2 = recibeFoto(file)
        if(request.files['imagen3'] !=''):
            file     = request.files['imagen3'] #recibiendo el archivo
            imagen_3 = recibeFoto(file)
        tipoServicio = request.form['tipoServicio']
        detallesAdicionales = request.form['detallesAdicionales']
        usuario_id = usuario.id
        orden = app.models.OrdenServicio(nombre=nombre, telefono=telefono, correo_electronico=correo_electronico,materialFk=materialFk,
                                         imagen1=imagen_1,imagen2=imagen_2,imagen3=imagen_3,
                                         tipoServicio=tipoServicio,detallesAdicionales=detallesAdicionales,usuario_id=usuario_id)
    
        
        app.db.session.add(orden)
        app.db.session.commit()
        
        url = url_for('ordenes_blueprint.mostrar_registro', id=usuario.id)
        return redirect(url)
    materialFk =app.models.Material.query.all()
    
    return render_template('agregar_orden.html', usuario=usuario, materialFk=materialFk) 

# Ruta para editar una orden de servicio (UPDATE)
@ordenes_blueprint.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_orden(id):
    orden = app.models.OrdenServicio.query.get(id)
    
    if request.method == 'POST':
        orden.nombre = request.form['nombre']
        orden.telefono = request.form['telefono']
        orden.correo_electronico = request.form['correo_electronico']
        orden.materialFk = request.form['materialFk']
        orden.tipoServicio = request.form['tipoServicio']
        orden.detallesAdicionales = request.form['detallesAdicionales']
        if(request.files['imagen1'] !=''):
            file     = request.files['imagen1'] #recibiendo el archivo
            orden.imagen1 = recibeFoto(file)
        if(request.files['imagen2'] !=''):
            file     = request.files['imagen2'] #recibiendo el archivo
            orden.imagen2 = recibeFoto(file)
        if(request.files['imagen3'] !=''):
            file     = request.files['imagen3'] #recibiendo el archivo
            orden.imagen3 = recibeFoto(file)
        
        app.db.session.commit()
        
        return redirect('/ordenes/listar')
    
    usuarios = app.models.Usuario.query.all()
    return render_template('editar_orden.html', orden=orden, usuarios=usuarios)

# Ruta para eliminar una orden de servicio (DELETE)
@ordenes_blueprint.route('/eliminar/<int:id>')
def eliminar_orden(id):
    orden = app.models.OrdenServicio.query.get(id)
    
    if orden:
        app.db.session.delete(orden)
        app.db.session.commit()
    
    return redirect('/ordenes/listar')




def recibeFoto(file):
    print(file)
    basepath = os.path.dirname (__file__) #La ruta donde se encuentra el archivo actual
    filename = secure_filename(file.filename) #Nombre original del archivo

    #capturando extensión del archivo ejemplo: (.png, .jpg, .pdf ...etc)
    extension           = os.path.splitext(filename)[1]
    nuevoNombreFile     = stringAleatorio() + extension
    #print(nuevoNombreFile)
        
    upload_path = os.path.join (basepath,'./../static/imagenes_OrdenServicio', nuevoNombreFile) 
    file.save(upload_path)

    return nuevoNombreFile



def stringAleatorio():
    string_aleatorio = "0123456789abcdefghijklmnopqrstuvwxyz_"
    longitud         = 20
    secuencia        = string_aleatorio.upper()
    resultado_aleatorio  = sample(secuencia, longitud)
    string_aleatorio     = "".join(resultado_aleatorio)
    return string_aleatorio