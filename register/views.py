from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import MercadoForm
from .models import Mercado, Supermercado
import pandas as pd
import geopandas as gp
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Create your views here.

def home(request):
    ''' La función genera la vista incicial de la aplicación
    '''
    return render(request, 'home.html')

def signup(request):
    ''' Genera el formulario de registro y valida la creación de los usuarios
    '''

    # Valida si el methodo es get o post
    if request.method == 'GET':
        # Genera el formulario de regitro
        return render(request, 'signup.html', {
            'formulario' : UserCreationForm
        })
    else:
        # Compara si las contraseñas son iguales
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Creamos el usuario
                user = User.objects.create_user(
                    username = request.POST['username'],
                    password = request.POST['password1']
                )
                # Guardamos el usuario en la base de datos
                user.save()
                # Redireccionamos a la principal
                login(request, user)
                return redirect(main)
            except:
                # Genera la vista nuevamente pero con un error
                return render(request, 'signup.html', {
                    'formulario' : UserCreationForm,
                    'error' : 'El usuario ya existe'
                })
        # Genera la vista nuevamente pero con un error
        return render(request, 'signup.html', {
            'formulario' : UserCreationForm,
            'error' : 'Las contraseñas no coinciden'
            })

def signout(request):
    ''' Cierra la sesión '''
    logout(request)
    return redirect(home)

def main(request):
    ''' Genera la pantalla principal '''

    # Verifica el método request, si es GET o POST
    if request.method == 'GET':
        return render(request, 'main.html', {
            'formulario' : MercadoForm
        })
    else:
        form = MercadoForm(request.POST)
        new_compra = form.save(commit=False)
        new_compra.usuario = request.user
        new_compra.save()
        return render(request, 'main.html', {
            'formulario' : MercadoForm
        })

def signin(request):
    ''' Genera el inicio de sesión
    '''

    # Verifica el método request, si es GET o POST
    if request.method == 'GET':
        # Si es GET genera la vista
        return render(request, 'signin.html', {
        'formulario' : AuthenticationForm
        })
    else:
        # Si es POST
        # Obtiene los datos del formulario
        user = authenticate(request, 
                     username = request.POST['username'],
                     password = request.POST['password'])
        # Verifica si existe o no el usuario
        if user is None:
            # Si no existe genera un error
            return render(request, 'signin.html', {
                'formulario' : AuthenticationForm,
                'error' : 'Usuario o contraseña incorrecto'
            })
        else:
            # Si exite, inicia sesión
            login(request, user)
            return redirect(main)

def registros(request):
    ''' Muestra todas las compras realizadas y gráficos de ayuda '''
    compras = Mercado.objects.filter(
        usuario = request.user
    )

    df_compras = pd.DataFrame(list(compras.values()))

    # Número de compras por supermercado
    com_super = df_compras[['supermercado_id', 'producto']].groupby('supermercado_id').count()

    # Costo total por tipo de producto
    com_tipo = df_compras[['tipo_id', 'costo']].groupby('tipo_id').sum()

    # Crear una figura con dos subgráficos
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(10, 8))

    # Graficar el número de compras por supermercado como puntos (scatter plot)
    com_super.reset_index().plot(kind='scatter', x='supermercado_id', y='producto', ax=ax1, color='black', s=100)
    ax1.set_title('Número de Compras por Supermercado', fontsize=16)
    ax1.set_xlabel('Supermercado ID', fontsize=14)
    ax1.set_ylabel('Número de Compras', fontsize=14)

    # Graficar el costo total por tipo de producto como
    com_tipo.plot(kind='bar', ax=ax2, legend=False, color='black', fontsize=12)
    ax2.set_title('Costo Total por Tipo de Producto', fontsize=16)
    ax2.set_xlabel('Tipo de Producto', fontsize=14)
    ax2.set_ylabel('Costo total', fontsize=14)

    # Ajustar el diseño para evitar solapamiento
    plt.tight_layout()

    # Guardar la figura en un búfer de bytes
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Codificar la figura en base64
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return render(request, 'registros.html', {
        'compras' : compras,
        'image' : image_base64
    })

def supermercados(request):
    # Obtener los datos de los supermercados desde la base de datos
    supermercados = pd.DataFrame(list(Supermercado.objects.all().values()))

    # Crear un GeoDataFrame con los datos de los supermercados
    geo_super = gp.GeoDataFrame(supermercados, 
                                geometry=gp.points_from_xy(supermercados.longitud, supermercados.latitud), 
                                crs='EPSG:21897')

    # Cargar el GeoDataFrame del mapa de Medellín desde un archivo GeoJSON
    mapa_med = gp.read_file('register/maps/med.geojson')
    
    # Limitar el mapa a los primeros 15 elementos (si es necesario)
    mapa_med = mapa_med.iloc[0:15]

    # Crear la figura y el eje
    fig, ax = plt.subplots(figsize=(10, 10))

    # Graficar el mapa de Medellín
    mapa_med.plot(ax=ax, color='lightblue', edgecolor='gray', linewidth=1)

    # Graficar los supermercados sobre el mapa
    geo_super.plot(ax=ax, color='red', marker='o')

    # Añadir etiquetas a los puntos
    for x, y, label in zip(geo_super.geometry.x, geo_super.geometry.y, geo_super['nombre']):
        ax.text(x, y, label, fontsize=8)

    # Ajustar el diseño para evitar solapamientos
    plt.tight_layout()

    # Guardar la figura en un búfer de bytes
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Codificar la figura en base64
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return render(request, 'supermercados.html', {'image': image_base64})