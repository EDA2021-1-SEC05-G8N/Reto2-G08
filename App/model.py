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
    Tags
    Año de publicacion

    Retorna el catalogo inicializado.
    """
    catalog = {'videos': None,
               'videoIds': None,
               'canales': None,
               'tags': None,
               'tagIds': None,
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
    catalog['tags'] = mp.newMap(34500,
                                maptype='PROBING',
                                loadfactor=0.5,
                                comparefunction=compareTagNames)
    """
    Este indice crea un map cuya llave es el Id de la etiqueta
    """
    catalog['tagIds'] = mp.newMap(34500,
                                  maptype='CHAINING',
                                  loadfactor=4.0,
                                  comparefunction=compareTagIds)
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


def addTag(catalog, cat):
    """
    Adiciona un tag a la tabla de tags dentro del catalogo y se
    actualiza el indice de identificadores del tag.
    """
    newtag = newVideoTag(cat['name'], cat['id'])
    mp.put(catalog['tags'], cat['name'], newtag)
    print(catalog['tags'])
    mp.put(catalog['tagIds'], cat['id'], newtag)


def addVideoTag(catalog, tag):
    tagid = tag['id']
    videoid = tag['goodreads_book_id']
    entry = mp.get(catalog['tagIds'], tagid)
    if entry:
        tagvideo = mp.get(catalog['tags'], me.getValue(entry)['name'])
        tagvideo['value']['total_videos'] += 1
        video = mp.get(catalog['videoIds'], videoid)
        if video:
            lt.addLast(tagvideo['value']['videos'], video['value'])




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


def newVideoTag(name, id):
    """
    Esta estructura crea una relación entre un tag y los libros que han sido
    marcados con dicho tag.  Se guarga el total de libros y una lista con
    dichos libros.
    """
    tag = {'tag_name': '',
           'tag_id': '',
           'total_videos': 0,
           'videos': None}
    tag['tag_name'] = name
    tag['tag_id'] = id
    tag['videos'] = lt.newList()
    return tag

# Funciones de consulta

def getVideosByCanal(catalog, canalname):
    """
    Retorna un autor con sus libros a partir del nombre del autor
    """
    canal = mp.get(catalog['canales'], canalname)
    if canal:
        return me.getValue(canal)
    return None


def getVideosByTag(catalog, cat, number):
    ""
    videos = catalog["videos"]
    cmpcategoria = catalog["tags"]
    print(cmpcategoria)
    idname=getVideosByCat(cmpcategoria, cat)
    videoscat = lt.newList()
    i=1
    while i <= lt.size(videos):
        idvideo = lt.getElement(videos, i).get("category_id")
        if idname == idvideo:
            video = lt.getElement(videos, i)
            lt.addLast(videoscat, video)
        i=i+1

    #   obtenemos los id dentro de una lista
    new_list=[]
    j=1
    while j <= lt.size(videoscat):
        video_id=lt.getElement(videoscat, j).get("video_id")
        new_list.append(video_id)
        j=j+1

    return new_list


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


def tagsSize(catalog):
    """
    Numero de tags en el catalogo
    """
    return mp.size(catalog['tagIds'])



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


def compareTagNames(name, tag):
    tagentry = me.getKey(tag)
    if (name == tagentry):
        return 0
    elif (name > tagentry):
        return 1
    else:
        return -1


def compareTagIds(id, tag):
    tagentry = me.getKey(tag)
    if (int(id) == int(tagentry)):
        return 0
    elif (int(id) > int(tagentry)):
        return 1
    else:
        return 0


def compareMapYear(id, tag):
    tagentry = me.getKey(tag)
    if (id == tagentry):
        return 0
    elif (id > tagentry):
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