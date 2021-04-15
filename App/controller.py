"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """
import time
import tracemalloc
import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def initCatalog():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.newCatalog()
    return catalog

# Funciones para la carga de datos

def loadData(catalog):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
####################################
    loadVideos(catalog)
    loadCats(catalog)

####################################

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return delta_time, delta_memory


def loadVideos(catalog):
    """
    Carga los libros del archivo.  Por cada libro se indica al
    modelo que debe adicionarlo al catalogo.
    """
    booksfile = cf.data_dir + 'videos-small.csv'
    input_file = csv.DictReader(open(booksfile, encoding='utf-8'))
    for video in input_file:
        model.addVideo(catalog, video)
        


def loadCats(catalog):
    """
    Carga todos los tags del archivo e indica al modelo
    que los adicione al catalogo
    """
    catsfile = cf.data_dir + 'category-id.csv'
    input_file = csv.DictReader(open(catsfile, encoding='utf-8'),  delimiter='\t')
    for cat in input_file:
        model.addCat(catalog, cat)


# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo


def getBestVideos(catalog, number):
    """
    Retorna los mejores libros según su promedio
    """
    bestvideos=1
    #bestvideos = model.getBestVideos(catalog, number)
    return bestvideos



def videosSize(catalog):
    """
    Numero de libros cargados al catalogo
    """
    return model.videosSize(catalog)


def canalesSize(catalog):
    """
    Numero de autores cargados al catalogo
    """
    return model.canalesSize(catalog)


def catsSize(catalog):
    """
    Numero de tags cargados al catalogo
    """
    return model.catsSize(catalog)


def getVideosByCanal(catalog, canalname):
    """
    Retorna los libros de un autor
    """
    canalinfo = model.getVideosByCanal(catalog, canalname)
    return canalinfo


def getVideosByCat(catalog, catname):
    """
    Retorna los libros que han sido marcados con
    una etiqueta
    """
    videos = model.getVideosByCat(catalog, catname)
    return videos


def getVideosYear(catalog, year):
    """
    Retorna los libros que fueron publicados
    en un año
    """
    videos = model.getVideosByYear(catalog, year)
    return videos



def getVideosByTendCat(cont, cat):
    videos = model.getVideosByTendCat(cont, cat)
    return videos

def getVideosByLikesCatPais(cont, cat, pais, num):

    videos = model.getVideosByLikesCatPais(cont, cat, pais, num)
    return videos


# ======================================
# Funciones para medir tiempo y memoria
# ======================================


def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory