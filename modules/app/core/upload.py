# -*- coding: UTF-8 -*-
# Esto se lo debe hacer desde la aplicación cliente (en el lenguaje que corresponda)
#from requests import post (pip3 install requests)

#url = 'http://localhost:3000/subirfile'

#def subir_files():
#    files = {'file': open('/home/gustavo/Downloads/RED1051935000125.txt', 'r')}
#    req = post(url,files=files)
#    print(req.text)
#    return {'message': req.text}
from app.core import consts
from werkzeug.utils import secure_filename
from os.path import join
from os import makedirs

ALLOWED_EXTENSIONS = {'txt', 'zip'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file(request):
    if 'file' not in request.files:
        return {'ok': False, 'message': 'No se ha cargado el archivo (se debe cargar son el nombre -file- en la petición POST)'}, 400
    
    file = request.files['file']
    if file.filename == '':
        return {'ok': False, 'message': 'No se ha seleccionado ningún archivo'}, 400
    
    if not (file and allowed_file(file.filename) and (file.filename[-len(consts.extension_comprimidos):].lower() == consts.extension_comprimidos and file.filename[:len(consts.nombre_comprimido_devoluciones)] == consts.nombre_comprimido_devoluciones or file.filename[-len(consts.extension_comprimidos):].lower() == consts.extension_txt and file.filename[:len(consts.nombre_txt)] == consts.nombre_txt)):
        return {'ok': False, 'message': 'El archivo tiene errores o no corresponde a un archivo de devoluciones'}, 400

    makedirs(consts.ubicacion_archivos_subidos, exist_ok=True)
    file.save(join(consts.ubicacion_archivos_subidos, secure_filename(file.filename)))
    return {'ok': True, 'message': 'Archivo cargado con correctamente', 'filename': secure_filename(file.filename)}
    