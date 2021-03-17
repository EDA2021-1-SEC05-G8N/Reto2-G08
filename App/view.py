"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printCanalData(canal):
    """
    Imprime la información del canal seleccionado
    """
    if canal:
        print('canal encontrado: ' + canal['name'])
        print('Promedio: ' + str(canal['average_rating']))
        print('Total de videos: ' + str(lt.size(canal['videos'])))
        for video in lt.iterator(canal['videos']):
            print('Titulo: ' + video['title'] )
        print("\n")
    else:
        print('No se encontro el canal.\n')


def printVideosbyTag(videos):
    """
    Imprime los libros que han sido clasificados con
    una etiqueta
    """
    if (videos):
        print('Se encontraron: ' + str(lt.size(videos)) + ' videos.')
        for video in lt.iterator(videos):
            print(video['title'])
        print("\n")
    else:
        print("No se econtraron videos.\n")


def printVideosbyYear(videos):
    """
    Imprime los libros que han sido publicados en un
    año
    """
    if(videos):
        print('Se encontraron: ' + str(lt.size(videos)) + ' videos')
        for video in lt.iterator(videos):
            print(video['title'])
        print("\n")
    else:
        print("No se encontraron videos.\n")


def printBestVideos(videos):
    """
    Imprime la información de los mejores libros
    por promedio
    """
    size = lt.size(videos)
    if size:
        print(' Estos son los mejores videos: ')
        for video in lt.iterator(videos):
            print('Titulo: ' + video['title'] + ' Rating: ' + video['trending_date'])
        print("\n")
    else:
        print('No se encontraron videos.\n')


# Menu de opciones

def printMenu():
    print("Bienvenido")
    print("1- Inicializar Catálogo")
    print("2- Cargar información en el catálogo")
    print("3- Consultar los videos de un año")
    print("4- Consultar los videos de un canal")
    print("5- Consultar los n videos con mas likes por etiqueta")
    print("0- Salir")


# Funciones de inicializacion

def initCatalog():
    """
    Inicializa el catalogo de libros
    """
    return controller.initCatalog()


def loadData(catalog):
    """
    Carga los libros en el catalogo
    """
    controller.loadData(catalog)

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Inicializando Catálogo ....")
        cont = controller.initCatalog()

    elif int(inputs[0]) == 2:
        print("Cargando información de los archivos ....")
        controller.loadData(cont)
        print('videos cargados: ' + str(controller.videosSize(cont)))
        print('canales cargados: ' + str(controller.canalesSize(cont)))
        print('etiquetas cargadas: ' + str(controller.tagsSize(cont)))
    
    elif int(inputs[0]) == 3:
        number = input("Buscando videos del año?: ")
        videos = controller.getVideosYear(cont, int(number))
        printVideosbyYear(videos)

    elif int(inputs[0]) == 4:
        canalname = input("Nombre del canal a buscar: ")
        canalinfo = controller.getVideosByCanal(cont, canalname)
        printCanalData(canalinfo)

    elif int(inputs[0]) == 5:
        numero=input("top :")
        label = input("Etiqueta a buscar: ")
        videos = controller.getVideosByTag(cont, label, int(numero))
        print(videos)
    else:
        sys.exit(0)
sys.exit(0)
