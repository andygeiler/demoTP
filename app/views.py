from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import requests
from django.http import JsonResponse
from .models import Favourite

def index_page(request):
    return render(request, 'index.html')


def home(request):
    
    url_api = "https://rickandmortyapi.com/api/character"

    
    respuesta = requests.get(url_api)

    if respuesta.status_code == 200:  
        datos_personajes = respuesta.json().get('results', [])

        
        personajes = []
        for personaje in datos_personajes:
            
            ultima_ubicacion = personaje.get('location', {}).get('name', 'Desconocida')
            primer_episodio = 'Desconocido'

            if personaje.get('episode'):
                url_episodio = personaje['episode'][0]
                respuesta_episodio = requests.get(url_episodio)
                if respuesta_episodio.status_code == 200:
                    primer_episodio = respuesta_episodio.json().get('name', 'Desconocido')

            personajes.append({
                'id': personaje['id'],
                'nombre': personaje['name'],
                'estado': personaje['status'],
                'imagen': personaje['image'],
                'ultima_ubicacion': ultima_ubicacion,
                'primer_episodio': primer_episodio,
                'url': personaje['url'],
            })

        
        favoritos_id = []
        if request.user.is_authenticated:
            favoritos_id = Favourite.objects.filter(user=request.user).values_list('url', flat=True)

        
        contexto = {
            'personajes': personajes,
            'favoritos_id': list(favoritos_id),  
        }
        return render(request, 'home.html', contexto)
    else:
        
        return render(request, 'home.html', {'personajes': [], 'favoritos_id': []})

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
    # Obtener los favoritos del usuario logueado
    favourites = Favourite.objects.filter(user=request.user)
    return render(request, 'favourites.html', {'favourite_list': favourites})

@login_required
def saveFavourite(request):
    if request.method == "POST":
        # Obtenemos los datos del formulario
        url = request.POST['url']
        name = request.POST['name']
        status = request.POST['status']
        last_location = request.POST['last_location']
        first_seen = request.POST['first_seen']

        # Verificamos si ya existe el favorito
        if not Favourite.objects.filter(user=request.user, url=url, name=name).exists():
            # Creamos el favorito si no existe
            Favourite.objects.create(
                user=request.user,
                url=url,
                name=name,
                status=status,
                last_location=last_location,
                first_seen=first_seen
            )

        # Redirigimos nuevamente al home
        return redirect('home')
    return redirect('home')


@login_required
def deleteFavourite(request):
    if request.method == "POST":
        fav_id = request.POST.get('id')
        try:
            favorito = Favourite.objects.get(id=fav_id, user=request.user)
            favorito.delete()
            return redirect('favourites')  # Redirige a la página de favoritos después de eliminar
        except Favourite.DoesNotExist:
            return JsonResponse({'error': 'Favorito no encontrado'}, status=404)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required
def exit(request):
    logout(request)  # Esto cierra la sesión del usuario
    return redirect('index-page')  # Redirige a la página de inicio 
