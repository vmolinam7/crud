# usuarios/urls.py

from django.urls import path
from . import views  
from . import api_views

urlpatterns = [
    path('', views.login_vista, name='login'),
    path('login/', views.login_vista, name='login'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/editar/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('logout/', views.logout_vista, name='logout'),
    path('registro/', views.registro_vista, name='registro'),

    #rutas api
    path('api/register/', api_views.RegisterAPIView.as_view(), name='api_register'),
    path('api/login/', api_views.LoginAPIView.as_view(), name='api_login'),
    path('api/logout/', api_views.LogoutAPIView.as_view(), name='api_logout'),
    path('api/users/', api_views.UserListAPIView.as_view(), name='api_user_list'),
    path('api/users/<int:pk>/', api_views.UserDetailAPIView.as_view(), name='api_user_detail'),
]
