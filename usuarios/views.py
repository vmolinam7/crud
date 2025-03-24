from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import logout
from django.views.decorators.cache import cache_control


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_vista(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_superuser:
                login(request, user)
                return redirect('lista_usuarios')
            else:
                messages.info(request, 'Debes ser SA para ingresar.')
                form = AuthenticationForm()
    else:
        form = AuthenticationForm()
    return render(request, 'principal.html', {'form': form})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def lista_usuarios(request):
    users = User.objects.filter(is_superuser=False)
    return render(request, 'lista_usuarios.html', {'users': users})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def editar_usuario(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        if username and email:
            user.username = username
            user.email = email
            user.save()
            messages.info(request, 'Usuario editado con éxito.')
            return redirect('lista_usuarios')

    return render(request, 'editar_usuarios.html', {'user': user})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@require_POST
@login_required
def eliminar_usuario(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    # if request.user.is_superuser:
    user.delete()
    messages.error(request, 'Usuario eliminado con éxito.')
    # else:
    # messages.error(
    #     request, 'No tienes permisos para eliminar este usuario.')
    return redirect('lista_usuarios')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def crear_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        if username and password:
            if not User.objects.filter(username=username).exists():
                user = User(
                    username=username,
                    email=email,
                    password=make_password(password)
                )
                user.save()
                messages.success(request, 'Usuario agregado con éxito.')
                return redirect('lista_usuarios')
            else:
                return render(request, 'crear_usuario.html', {'error': 'El nombre de usuario ya existe'})

    return render(request, 'crear_usuario.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def logout_vista(request):
    logout(request)
    return redirect('login')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def registro_vista(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not username or not password:
            return render(request, 'register.html', {'error': 'Por favor, completa todos los campos.'})

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'El nombre de usuario ya está en uso.'})

        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password)
        )
        user.save()

        messages.success(request, 'Usuario registrado con éxito.')
        return redirect('login')

    return render(request, 'registrar_usuario.html')
