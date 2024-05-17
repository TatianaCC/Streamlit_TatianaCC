import py7zr
import os
import pathlib

dirname = str(pathlib.Path(__file__).parent.parent)
archivos_pkl = [dirname+'/models/vectorizer.pkl', dirname+'/models/vectorizer_matrix.pkl', dirname+'/models/cosine_similarity.pkl']
archivo_salida = dirname+'/models/Models.7z'

with py7zr.SevenZipFile(archivo_salida, 'w') as archivo:
    for archivo_pkl in archivos_pkl:
        archivo.write(archivo_pkl, os.path.basename(archivo_pkl))