from app import mongo

def insert_filename(filename):
    mongo.db.read_files.insert_one({'name': filename})

def search_file(filename):
    file = mongo.db.read_files.find_one({'name': filename})
    if file:
        return True
    return False

def insert_devolucion(ciudad, local, anio, mes, dia, bandejas):
    mongo.db.devoluciones.insert_one({'ciudad': ciudad, 'local': local, 'anio': anio, 'mes': mes, 'dia': dia, 'bandejas': bandejas})