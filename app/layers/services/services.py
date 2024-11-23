import requests
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user

def getAllImages(filtro=None):
    # URL base de la API
    url= "https://rickandmortyapi.com/api/character"
    
    # Si se pasa un filtro, lo añadimos a la URL
    if filtro:
        url += "?name=" + filtro

    # Hacemos la solicitud a la API
    respuesta = requests.get(url)

    # Verificamos si la solicitud fue exitosa
    if respuesta.status_code != 200:
        return {"error": "No se pudo obtener la información"}

    # Obtenemos los datos de la respuesta
    datos = respuesta.json()

    # Lista para guardar las tarjetas de los personajes
    tarjetas = []

    # Recorremos los personajes en los resultados
    for personaje in datos['results']:
        # Creamos una tarjeta con información básica del personaje
        tarjeta = {
            'nombre': personaje['name'],  # Nombre del personaje
            'estado': personaje['status'],  # Estado (vivo, muerto, desconocido)
            'especie': personaje['species'],  # Especie (humano, alien, etc.)
            'imagen': personaje['image'],  # URL de la imagen
            'descripcion': f"Estado: {personaje['status']}, Especie: {personaje['species']}"  # Descripción
        }
        tarjetas.append(tarjeta)  # Añadimos la tarjeta a la lista

    return tarjetas

def saveFavourite(request):
    fav = '' # transformamos un request del template en una Card.
    fav.user = '' # le asignamos el usuario correspondiente.

    return repositories.saveFavourite(fav) # lo guardamos en la base.

# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = [] # buscamos desde el repositories.py TODOS los favoritos del usuario (variable 'user').
        mapped_favourites = []

        for favourite in favourite_list:
            card = '' # transformamos cada favorito en una Card, y lo almacenamos en card.
            mapped_favourites.append(card)

        return mapped_favourites

def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.deleteFavourite(favId) # borramos un favorito por su ID.
