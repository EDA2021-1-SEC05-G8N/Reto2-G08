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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog():
    """ Inicializa el catálogo de libros

    Crea una lista vacia para guardar todos los libros

    Se crean indices (Maps) por los siguientes criterios:
    Autores
    ID libros
    cats
    Año de publicacion

    Retorna el catalogo inicializado.
    """
    catalog = {'videos': None,
               'videoIds': None,
               'canales': None,
               'cats': None,
               'catIds': None,
               'years': None}

    """
    Esta lista contiene todo los libros encontrados
    en los archivos de carga.  Estos libros no estan
    ordenados por ningun criterio.  Son referenciados
    por los indices creados a continuacion.
    """
    catalog['videos'] = lt.newList('SINGLE_LINKED', compareVideoIds)

    """
    A continuacion se crean indices por diferentes criterios
    para llegar a la informacion consultada.  Estos indices no
    replican informacion, solo referencian los libros de la lista
    creada en el paso anterior.
    """

    """
    Este indice crea un map cuya llave es el identificador del libro
    """
    catalog['videoIds'] = mp.newMap(10000,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareMapVideoIds)

    """
    Este indice crea un map cuya llave es el autor del libro
    """
    catalog['canales'] = mp.newMap(800,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareCanalesByName)
    """
    Este indice crea un map cuya llave es la etiqueta
    """
    catalog['cats'] = mp.newMap(34500,
                                maptype='PROBING',
                                loadfactor=0.5,
                                comparefunction=compareCatNames)
    """
    Este indice crea un map cuya llave es el Id de la etiqueta
    """
    catalog['catIds'] = mp.newMap(34500,
                                  maptype='CHAINING',
                                  loadfactor=4.0,
                                  comparefunction=compareCatIds)
    """
    Este indice crea un map cuya llave es el año de publicacion
    """
    catalog['years'] = mp.newMap(40,
                                 maptype='PROBING',
                                 loadfactor=0.5,
                                 comparefunction=compareMapYear)

    return catalog


# Funciones para agregar informacion al catalogo

def addVideo(catalog, video):
    """
    Esta funcion adiciona un libro a la lista de libros,
    adicionalmente lo guarda en un Map usando como llave su Id.
    Adicionalmente se guarda en el indice de autores, una referencia
    al libro.
    Finalmente crea una entrada en el Map de años, para indicar que este
    libro fue publicaco en ese año.
    """
    lt.addLast(catalog['videos'], video)
    mp.put(catalog['videoIds'], video['video_id'], video)
    canales = video['channel_title'].split(",")  # Se obtienen los autores
    for canal in canales:
        addVideoCanal(catalog, canal.strip(), video)
    addVideoYear(catalog, video)


def addVideoYear(catalog, video):
    """
    Esta funcion adiciona un libro a la lista de libros que
    fueron publicados en un año especifico.
    Los años se guardan en un Map, donde la llave es el año
    y el valor la lista de libros de ese año.
    """
    try:
        years = catalog['years']
        if (video['publish_time'] != ''):
            pubyear = video['publish_time'][0:4]
            pubyear = int(float(pubyear))
        else:
            pubyear = 2020
        existyear = mp.contains(years, pubyear)
        if existyear:
            entry = mp.get(years, pubyear)
            year = me.getValue(entry)
        else:
            year = newYear(pubyear)
            mp.put(years, pubyear, year)
        lt.addLast(year['videos'], video)
    except Exception:
        return None


def newYear(pubyear):
    """
    Esta funcion crea la estructura de libros asociados
    a un año.
    """
    entry = {'year': "", "videos": None}
    entry['year'] = pubyear
    entry['videos'] = lt.newList('SINGLE_LINKED', compareYears)
    return entry


def addVideoCanal(catalog, canalname, video):
    """
    Esta función adiciona un libro a la lista de libros publicados
    por un autor.
    Cuando se adiciona el libro se actualiza el promedio de dicho autor
    """
    canales = catalog['canales']
    existcanal = mp.contains(canales, canalname)
    if existcanal:
        entry = mp.get(canales, canalname)
        canal = me.getValue(entry)
    else:
        canal = newAuthor(canalname)
        mp.put(canales, canalname, canal)
    lt.addLast(canal['videos'], video)
    canal['views'] += float(canal['views'])
    totcanales = lt.size(canal['videos'])
    if (totcanales > 0):
        canal['average_rating'] = canal['views'] / totcanales


def addCat(catalog, cat):
    """
    Adiciona uns categoria a la tabla de cats dentro del catalogo y se
    actualiza el indice de identificadores de las categorias.
    """
    newcat = newVideoCat(cat['name'], cat['id'])
    mp.put(catalog['cats'], cat['name'], newcat)
    #print(catalog['cats'])
    mp.put(catalog['catIds'], cat['id'], newcat)


def addVideoCat(catalog, cat):
    catid = cat['id']
    videoid = cat['goodreads_book_id']
    entry = mp.get(catalog['catIds'], catid)
    if entry:
        catvideo = mp.get(catalog['cats'], me.getValue(entry)['name'])
        catvideo['value']['total_videos'] += 1
        video = mp.get(catalog['videoIds'], videoid)
        if video:
            lt.addLast(catvideo['value']['videos'], video['value'])




# Funciones para creacion de datos

def newAuthor(name):
    """
    Crea una nueva estructura para modelar los libros de un autor
    y su promedio de ratings. Se crea una lista para guardar los
    libros de dicho autor.
    """
    canal = {'name': "",
              "videos": None,
              "views": 0,
              "average_rating": 0}
    canal['name'] = name
    canal['videos'] = lt.newList('SINGLE_LINKED', compareCanalesByName)
    return canal


def newVideoCat(name, id):
    """
    Esta estructura crea una relación entre un cat y los libros que han sido
    marcados con dicho cat.  Se guarga el total de libros y una lista con
    dichos libros.
    """
    cat = {'cat_name': '',
           'id': '',
           'total_videos': 0,
           'videos': None}
    cat['cat_name'] = name
    cat['id'] = id
    cat['videos'] = lt.newList()
    return cat

# Funciones de consulta

def getVideosByCanal(catalog, canalname):
    """
    Retorna un autor con sus libros a partir del nombre del autor
    """
    canal = mp.get(catalog['canales'], canalname)
    if canal:
        return me.getValue(canal)
    return None




def getVideosByYear(catalog, year):
    """
    Retorna los libros publicados en un año
    """
    year = mp.get(catalog['years'], year)
    if year:
        return me.getValue(year)['videos']
    return None


def videosSize(catalog):
    """
    Número de libros en el catago
    """
    return lt.size(catalog['videos'])


def canalesSize(catalog):
    """
    Numero de autores en el catalogo
    """
    return mp.size(catalog['canales'])


def catsSize(catalog):
    """
    Numero de tags en el catalogo
    """
    return mp.size(catalog['catIds'])



# Funciones utilizadas para comparar elementos dentro de una lista

def compareVideoIds(id1, id2):
    """
    Compara dos ids de dos videos
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1


def compareMapVideoIds(id, entry):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    identry = me.getKey(entry)
    if ((id) == (identry)):
        return 0
    elif ((id) > (identry)):
        return 1
    else:
        return -1


def compareCanalesByName(keyname, canal):
    """
    Compara dos nombres de autor. El primero es una cadena
    y el segundo un entry de un map
    """
    authentry = me.getKey(canal)
    if (keyname == authentry):
        return 0
    elif (keyname > authentry):
        return 1
    else:
        return -1


def compareCatNames(name, cat):
    catentry = me.getKey(cat)
    if (name == catentry):
        return 0
    elif (name > catentry):
        return 1
    else:
        return -1


def compareCatIds(id, cat):
    catentry = me.getKey(cat)
    if (int(id) == int(catentry)):
        return 0
    elif (int(id) > int(catentry)):
        return 1
    else:
        return 0


def compareMapYear(id, cat):
    catentry = me.getKey(cat)
    if (id == catentry):
        return 0
    elif (id > catentry):
        return 1
    else:
        return 0


def compareYears(year1, year2):
    if (int(year1) == int(year2)):
        return 0
    elif (int(year1) > int(year2)):
        return 1
    else:
        return 0

def cmpVideosByLikes(video1, video2):
    return (float(video1["likes"]) < float(video2["likes"]))


# Funciones de ordenamiento
def sortVideosLikes(catalog):
    sa.sort(catalog["videos"], cmpVideosByLikes)


def getVideosByCat(catalog, name):
    i=1
    idname=""
    while i <= lt.size(catalog):
        categoria = lt.getElement(catalog, i).get("name") 
        if str(categoria) == name:
            idname = lt.getElement(catalog, i).get("id")
            break
        else:
            i=i+1
    return idname