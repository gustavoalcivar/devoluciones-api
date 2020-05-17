# -*- coding: UTF-8 -*-
import app.core.consts
from zipfile import ZipFile
from os import listdir, remove
from os.path import isfile, join, sep, isdir
from io import open
from app.core.data_base import insert_filename, search_file, insert_devolucion
from app.core import consts

# Método para leer los archivos de un directorio, no lista los sub-directorios
def read_file(ruta, extension, inicio_nombre):
    lista_final = []
    lista_archivos = [arch for arch in listdir(ruta) if isfile(join(ruta, arch))]
    for archivo in lista_archivos:
        # Se verifica si el archivo tiene extensión requerida y el nombre inicia con lo que se solicita
        if archivo[-len(consts.extension_comprimidos):].lower() == extension and archivo[:len(inicio_nombre)] == inicio_nombre:
            path_global = ruta + sep + archivo
            lista_final.append(path_global)
    return lista_final


def exec_process():
    if not isdir(consts.descargas):
        return {'ok': False, 'message': 'No existe la ruta con los archivos que se deben procesar'}, 500
    
    # Se listan los archivos comprimidos descargados
    archivos_comprimidos = read_file(consts.descargas, consts.extension_comprimidos, consts.nombre_comprimido_devoluciones)

    if len(archivos_comprimidos) > 0:
        for archivo_comprimido in archivos_comprimidos:
            # Se descomprimime el archivo
            archivo_zip = ZipFile(archivo_comprimido)
            try:
                archivo_zip.extractall(consts.descargas)
                # print('Extrayendo el archivo ' + archivo_comprimido)
            except Exception as e:
                print('Error al extraer el archivo ' + archivo_comprimido)
                print('Detalle del error' + str(e))
                pass
            archivo_zip.close()
            # Una vez descomprimido, se puede eliminar el archivo comprimido
            remove(archivo_comprimido)
            # print('Eliminando el archivo ' + archivo_comprimido)

    # Se vuelve a listar los archivos en busca de los .txt de las devoluciones
    archivos_txt = read_file(consts.descargas, consts.extension_txt, consts.nombre_txt)

    if len(archivos_txt) > 0:
        for archivo_txt in archivos_txt:
            # print('Archivo: ' + archivo_txt)
            # Lectura del archivo
            archivo_texto = open(archivo_txt, 'r')
            contenido = archivo_texto.read()
            archivo_texto.seek(0)
            # Verificamos si aún no ha sido leído el archivo previamente
            if search_file(archivo_txt.split(sep)[-1]):
                print('El archivo ' + archivo_txt.split(sep)[-1] + ' ya fue procesado')
            # Verificamos si el archivo corresponde a un archivo de devoluciones de empanadas Joselo
            elif contenido.count(consts.proveedor) > 0 and contenido.count(consts.codigo_proveedor) > 0:
                # Se lee línea por ĺínea para obtener los valores
                lineas = archivo_texto.readlines()
                numero_linea = 0
                linea_local = -99
                ciudad = ''
                local = ''
                fecha = ''
                numero_bandejas = 0
                for linea in lineas:
                    if linea.count(consts.etiqueta_local) == 1:
                        # El local está en la siguiente línea de etiquetaLocal = 'Tda/Alm/CDI:'
                        linea_local = numero_linea + 1
                    if numero_linea == linea_local:
                        # Se trata de la línea del local, el cual se encuentra desde el inicio de la línea
                        local = linea[0:linea.index(consts.codigo_proveedor)].strip()
                    if linea.count(consts.pais) == 1:
                        # Se trata de la línea donde se encuentra la ciudad ej. PORTOVIEJO - ECUADOR
                        ciudad = linea[0:linea.index(consts.pais) - 3].strip()
                    if linea.count(consts.etiqueta_fecha_elaboracion) == 1:
                        # Se trata de la línea en la que se encuentra la fecha
                        fecha = linea[linea.index(consts.etiqueta_fecha_elaboracion) + len(consts.etiqueta_fecha_elaboracion):len(
                            linea) - 1].strip()
                    if linea.count(consts.etiqueta_total) == 1:
                        # Se trata de la línea en la que se encuentra el total de la devolución
                        valor = float(linea[linea.index(consts.etiqueta_total) + len(consts.etiqueta_total):len(linea) - 1].strip())
                        # Se verifica que el valor sea múltipo de alguno de los precios de las bandejas
                        for precio in consts.precios:
                            if round((valor % precio), consts.decimales_a_considerar) == 0 or consts.precios.count(round((valor % precio), consts.decimales_a_considerar)) > 0:
                                numero_bandejas = int(valor / precio)

                    numero_linea = numero_linea + 1
                
                if numero_bandejas == 0:
                    print('El valor del archivo: ' + archivo_txt + ' no es correcto')
                else:
                    # Se ingresan los valores del archivo y el nombre del archivo leído a la base de datos
                    insert_filename(archivo_txt.split(sep)[-1])
                    # Se separa la fecha en día, mes y año
                    insert_devolucion(ciudad, local, int(fecha.split('/')[2]), mes(fecha.split('/')[1]), int(fecha.split('/')[0]), numero_bandejas)
                    print('Datos del archivo ' + archivo_txt.split(sep)[-1] + ':')
                    print(ciudad)
                    print(local)
                    print(fecha)
                    print(str(numero_bandejas) + ' bandejas\n')
            # Una vez obtenido los valores, se puede eliminar el archivo txt
            remove(archivo_txt)
            archivo_texto.close()
    return {'ok': True, 'message': 'Proceso finalizado correctamente', 'archivos_procesados': archivos_txt}

def mes(mes_leido):
    if mes_leido.lower() == 'ene':
        return 1
    elif mes_leido.lower() == 'feb':
        return 2
    elif mes_leido.lower() == 'mar':
        return 3
    elif mes_leido.lower() == 'abr':
        return 4
    elif mes_leido.lower() == 'may':
        return 5
    elif mes_leido.lower() == 'jun':
        return 6
    elif mes_leido.lower() == 'jul':
        return 7
    elif mes_leido.lower() == 'ago':
        return 8
    elif mes_leido.lower() == 'sep':
        return 9
    elif mes_leido.lower() == 'oct':
        return 10
    elif mes_leido.lower() == 'nov':
        return 11
    elif mes_leido.lower() == 'dic':
        return 12
    else:
        return 0
