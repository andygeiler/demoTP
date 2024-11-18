import requests
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user

def getAllImages(input=None):
    json_collection = []

    
    response = requests.get("https://rickandmortyapi.com/api/character")
    if response.status_code == 200:
        json_collection = response.json()
    else:
        return []  

    images = []
    for data in json_collection:
        card = card(
            name=data['name'],
            status=data['status'],
            url=data['image'],
            last_location=data['location']['name'], 
            first_seen=data['episode'][0]  
        )
        images.append(card)

    return images



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