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
    loadVideos(catalog)
    loadTags(catalog)


def loadVideos(catalog):
    """
    Carga los libros del archivo.  Por cada libro se indica al
    modelo que debe adicionarlo al catalogo.
    """
    booksfile = cf.data_dir + 'videos-small.csv'
    input_file = csv.DictReader(open(booksfile, encoding='utf-8'))
    for book in input_file:
        model.addVideo(catalog, book)


def loadTags(catalog):
    """
    Carga todos los tags del archivo e indica al modelo
    que los adicione al catalogo
    """
    tagsfile = cf.data_dir + 'category-id.csv'
    input_file = csv.DictReader(open(tagsfile, encoding='utf-8'),  delimiter='\t')
    for tag in input_file:
        model.addTag(catalog, tag)



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


def tagsSize(catalog):
    """
    Numero de tags cargados al catalogo
    """
    return model.tagsSize(catalog)


def getVideosByCanal(catalog, canalname):
    """
    Retorna los libros de un autor
    """
    canalinfo = model.getVideosByCanal(catalog, canalname)
    return canalinfo


def getVideosByTag(catalog, tagname, numero):
    """
    Retorna los libros que han sido marcados con
    una etiqueta
    """
    videos = model.getVideosByTag(catalog, tagname, numero)
    return videos


def getVideosYear(catalog, year):
    """
    Retorna los libros que fueron publicados
    en un año
    """
    videos = model.getVideosByYear(catalog, year)
    return videos

