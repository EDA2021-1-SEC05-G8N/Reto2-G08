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
from DISClib.DataStructures import arraylistiterator as lit
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as mer
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
               'years': None,
               'countries': None}
               "category": None}

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
                                   maptype='PROBING',
                                   loadfactor=0.2,
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
                                maptype='CHAINING',
                                loadfactor=8.0,
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

    catalog['countries'] = mp.newMap(200,
                                 maptype='PROBING',
                                 loadfactor=0.5,
                                 comparefunction=None)
                                 
    catalog['category'] = mp.newMap(40,
                                 maptype='PROBING',
                                 loadfactor=0.5,
                                 comparefunction=compareCatNames)

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
    c = video['country']
    addVideoYear(catalog, video)
    addCountry(catalog,video)
    addVideoCategory(catalog, video)





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

def addCountry(catalog, video):
    countries = catalog['countries']
    pais = video['country']
    existcountry = mp.contains(countries, pais)
    if existcountry:
        entry = mp.get(countries, pais)
        m = me.getValue(entry)
    else:
        m = lt.newList('ARRAY_LIST')
        a = mp.put(countries, pais,m) 
    lt.addLast(m, video)

def getVideosByLikes(catalog, category, pais):
    cat_id = encontrarCat(catalog, category)
    country = encontrarPais(catalog, pais)
    r = lt.newList('ARRAY_LIST', cmpVideosByViews)
    for i in range(int(country['size'])):
        video = country['elements'][i]
        if video['category_id'] == cat_id['id']:
            lt.addLast(r, video)
    res = sortVideos1(r)
    return res

def trendingByCount(catalog, pais):
    country = encontrarPais(catalog, pais)
    mapa = mp.newMap(comparefunction = compareMapVideoIds)
    for i in range(int(country['size'])):
        video = country['elements'][i]
        existid = mp.contains(mapa, video['video_id'])
        if existid:
            entry = mp.get(mapa, video['video_id'])
            c = me.getValue(entry) 
            c+=1
        else: 
            entry = mp.put(mapa, video['video_id'], 1)
    a = "hola"

def encontrarPais(catalog, pais):
    countries = catalog['countries']
    existcountry = mp.contains(countries, pais)
    if existcountry:
        entry = mp.get(countries, pais)
        c = me.getValue(entry)
        return c
    else: 
        return None

def encontrarCat(catalog, category):
    categories = catalog['cats']
    existcat= mp.contains(categories, category)
    if existcat:
        entry = mp.get(categories, category)
        m = me.getValue(entry)
        return m
    else: 
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



def addVideoCategory(catalog, video):
    """
    Esta funcion adiciona un libro a la lista de libros que
    fueron publicados en un año especifico.
    Los años se guardan en un Map, donde la llave es el año
    y el valor la lista de libros de ese año.
    """
    try:
        categorias = catalog['category']
        if (video['category_id'] != ''):
            categoria = video['category_id']
            categoria = int(float(categoria))
        else:
            categoria = 0
        existcat = mp.contains(categorias, categoria)
        if existcat:
            entry = mp.get(categorias, categoria)
            cat = me.getValue(entry)
        else:
            cat = newCategory(categoria)
            mp.put(categorias, categoria, cat)
        lt.addLast(cat['videos'], video)
    except Exception:
        return None




def newCategory(category):
    """
    Esta funcion crea la estructura de libros asociados
    a un año.
    """
    entry = {'category_id': "", "videos": None}
    entry['category_id'] = category
    entry['videos'] = lt.newList('SINGLE_LINKED', compareCatIds)
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
    mp.put(catalog['catIds'], cat['id'], newcat)






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
    
    cat = {

    }
    cat['cat_name'] = name
    cat['id'] = id
    cat['videos'] = lt.newList()
    return cat

# Funciones de consulta


def getVideosByTendCat(cont, cate):
    cat = mp.get(cont['category'], cate)
    if cat:
        videoscat = me.getValue(cat)['videos']
    new_list=[]
    j=1
    while j <= lt.size(videoscat):
        video_id=lt.getElement(videoscat, j).get("video_id")
        new_list.append(video_id)
        j=j+1
    print(new_list)

    countlista = [new_list.count(num) for num in new_list]

    # obtenemos el mayor elemeto y su indice
    max_num = max(countlista)
    max_index = countlista.index(max_num)
    max_id=new_list[max_index]
    # devolvemos el elemento
    k=1
    video_max1=lt.getElement(videoscat, k)
    while k <= lt.size(videoscat):
        video_max2=lt.getElement(videoscat, k).get("video_id")
        if video_max2 == max_id:
            video_max1=lt.getElement(videoscat, k)
            break
        k=k+1
    ########### presentacion de datos
    new_elem = {}
    new_elem['titulo'] = video_max1.get("title")
    new_elem['titulo_canal'] = video_max1.get("channel_title")
    new_elem['category_id'] = video_max1.get("category_id")
    new_elem['dias'] = max_num
    return new_elem 



def getVideosByLikesCatPais(cont, cat, pais, num):
    sortVideosLikes(cont)

    cat = mp.get(cont['category'], cat)
    if cat:
        videoscat = me.getValue(cat)['videos']
    videoslikes=lt.newList()
    new_datalist = []
    i=1
    while i <= lt.size(videoscat):
        country = lt.getElement(videoscat, i).get("country")
        if pais == country:
            video = lt.getElement(videoscat, i)
            lt.addLast(videoslikes, video)
        i=i+1
    if lt.size(videoslikes)>num+1:
        for cont in range(1, num+1):
            new_elem = {}
            new_elem['titulo'] = lt.getElement(videoslikes, cont).get("title")
            new_elem['titulo_canal'] = lt.getElement(videoslikes, cont).get("channel_title")
            new_elem['publish_time'] = lt.getElement(videoslikes, cont).get("publish_time")
            new_elem['vistas'] = lt.getElement(videoslikes, cont).get("views")
            new_elem['likes'] = lt.getElement(videoslikes, cont).get("likes")
            new_elem['dislikes'] = lt.getElement(videoslikes, cont).get("dislikes")
            new_elem['tags'] = lt.getElement(videoslikes, cont).get("tags")
            new_datalist.append(new_elem)
    else:
        for cont in range(1, lt.size(videoslikes)+1):
            new_elem = {}
            new_elem['titulo'] = lt.getElement(videoslikes, cont).get("title")
            new_elem['titulo_canal'] = lt.getElement(videoslikes, cont).get("channel_title")
            new_elem['publish_time'] = lt.getElement(videoslikes, cont).get("publish_time")
            new_elem['vistas'] = lt.getElement(videoslikes, cont).get("views")
            new_elem['likes'] = lt.getElement(videoslikes, cont).get("likes")
            new_elem['dislikes'] = lt.getElement(videoslikes, cont).get("dislikes")
            new_elem['tags'] = lt.getElement(videoslikes, cont).get("tags")
            new_datalist.append(new_elem)
    return new_datalist

def getVideosByCanal(catalog, canalname):
    """
    Retorna un autor con sus libros a partir del nombre del autor
    """
    canal = mp.get(catalog['canales'], canalname)
    if canal:
        return me.getValue(canal)
    return None

def getVideosByCountry(catalog, pais):
    exist = mp.contains(catalog['countries'], pais)
    if exist:
        entry = mp.get(catalog['countries'], pais)
        count = me.getValue(entry)
    else:
        count = "No existe el pais"
    return count


def getVideosByYear(catalog, year):
    """
    Retorna los libros publicados en un año
    """
    year = mp.get(catalog['years'], year)
    print(year)
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
    return mp.size(catalog['cats'])



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


def cmpVideosByViews(video1, video2):
    return(int(video1['views']) > int (video2['views']))
        
# Funciones de ordenamiento
def sortVideosLikes(catalog):
    sa.sort(catalog["videos"], cmpVideosByLikes)


def getVideosByCat(catalog, name):
    idname=""
    while i <= lt.size(catalog):
        categoria = lt.getElement(catalog, i).get("name") 
        if str(categoria) == name:
            idname = lt.getElement(catalog, i).get("id")
            break
        else:
            i=i+1
    return idname

def sortVideos(catalog):
    namecat = mp.get(catalog['cats'], name)
    idname = int(me.getValue(namecat)["id"])
    return idname

def sortVideos1(catalog):
    sub_list = catalog.copy()
    sorted_list = sa.sort(sub_list, cmpVideosByViews) 
    return sorted_list
