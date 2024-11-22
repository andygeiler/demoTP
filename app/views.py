# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import requests

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados que corresponden a las imágenes de la API y los favoritos del usuario, y los usa para dibujar el correspondiente template.
# si el opcional de favoritos no está desarrollado, devuelve un listado vacío.
def home(request):
    # URL de la API
    url_api = "https://rickandmortyapi.com/api/character"
    
    # Hacemos la solicitud a la API
    respuesta = requests.get(url_api)
    
    if respuesta.status_code == 200:  # Si la API responde correctamente
        datos_personajes = respuesta.json()['results']  # Obtenemos los datos de los personajes

        # Creamos una lista de personajes con la información necesaria
        personajes = []
        for personaje in datos_personajes:
            # Obtenemos la ubicación y el primer episodio (si están disponibles)
            ultima_ubicacion = personaje['location']['name'] if 'location' in personaje else 'Desconocida'
            primer_episodio = 'Desconocido'
            if 'episode' in personaje and len(personaje['episode']) > 0:
                url_episodio = personaje['episode'][0]
                respuesta_episodio = requests.get(url_episodio)
                if respuesta_episodio.status_code == 200:
                    primer_episodio = respuesta_episodio.json().get('name', 'Desconocido')

            # Agregamos el personaje a la lista
            personajes.append({
                'nombre': personaje['name'],
                'estado': personaje['status'],
                'imagen': personaje['image'],
                'ultima_ubicacion': ultima_ubicacion,
                'primer_episodio': primer_episodio,
            })

        # Enviamos los personajes al template
        contexto = {'personajes': personajes}
        return render(request, 'home.html', contexto)
    else:
        # Si hay un error, enviamos una lista vacía
        return render(request, 'home.html', {'personajes': []})

def search(request):
    search_msg = request.POST.get('query', '')

    # si el texto ingresado no es vacío, trae las imágenes y favoritos desde services.py,
    # y luego renderiza el template (similar a home).
    if (search_msg != ''):
        pass
    else:
        return redirect('home')


# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = []
    return render(request, 'favourites.html', { 'favourite_list': favourite_list })

@login_required
def saveFavourite(request):
    pass

@login_required
def deleteFavourite(request):
    pass

@login_required
def exit(request):
    pass
