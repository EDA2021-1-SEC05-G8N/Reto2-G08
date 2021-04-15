"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el cur1 ISIS1225 - Estructuras de Datos y Algoritmos
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
from DISClib.ADT import map as mp
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


def printVideosbyCat(videos):
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
    print("3- Encontrar n videos con mas views por pais")
    print("4- Encontrar video tendencia por categoría")
    print("5- Encontrar video tendencia por pais")
    print("6- Buscar los videos con más Likes")
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
        answer = controller.loadData(cont)
        print('videos cargados: ' + str(controller.videosSize(cont)))
        print('canales cargados: ' + str(controller.canalesSize(cont)))
        print('etiquetas cargadas: ' + str(controller.catsSize(cont)))
        print("Tiempo [ms]: ", f"{answer[0]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{answer[1]:.3f}")
    
    elif int(inputs[0]) == 3:
        pais=input("pais : ")
        categoria = " " + input("categoria a buscar: ")
        num = int(input("Numero de videos? : "))
        req1 = controller.getVideosByLikes(cont, categoria, pais)
        ans=req1[0]
        data=req1[1]
        print("Tiempo [ms]: ", f"{data[0]:.3f}", "  ||  ",
        "Memoria [kB]: ", f"{data[1]:.3f}")
        for i in range(1, num+1):
            print(lt.getElement(ans, i)['title'])

    elif int(inputs[0]) == 4:
        cat = input("categoria a buscar: ")
        cat= controller.getVideosByCat(cont, cat)
        videos = controller.getVideosByTendCat(cont, int(cat))
        ans=videos[0]
        data=videos[1]
        print("Tiempo [ms]: ", f"{data[0]:.3f}", "  ||  ",
        "Memoria [kB]: ", f"{data[1]:.3f}")
        print(ans)

    elif int(inputs[0]) == 5:
        pais=input("pais del cual desea conocer el video con mas dias de trending: ")
        s = controller.req2(cont, pais)
        ans=s[0]
        data=s[1]
        print("Tiempo [ms]: ", f"{data[0]:.3f}", "  ||  ",
        "Memoria [kB]: ", f"{data[1]:.3f}")
        print(ans)

    elif int(inputs[0]) == 6:
        cat = input("categoria a buscar: ")
        pais = input("país a buscar: ")
        num = input("nunmero de videos para listar: ")
        cat= controller.getVideosByCat(cont, cat)
        videos = controller.getVideosByLikesCatPais(cont,int(cat), pais, int(num))
        ans=videos[0]
        data=videos[1]
        print("Tiempo [ms]: ", f"{data[0]:.3f}", "  ||  ",
        "Memoria [kB]: ", f"{data[1]:.3f}")
        print(ans)
    
    else:
        sys.exit(0)
sys.exit(0)
