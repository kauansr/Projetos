from django.urls import path
from .views import Login,Logout,Cadastro,AtualizarPerfil, Deletarperfil
from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from perfil.api.views import MyTokenObtainPairView
from perfil.api.viewsets import UserViewset
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'usuarios', UserViewset)

urlpatterns = [
    path('', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('cadastro/', Cadastro.as_view(), name='cadastro'),
    path('atualizarperfil/', AtualizarPerfil.as_view(), name='atualizar'),
    path('deletarperfil/', Deletarperfil.as_view(), name='deletarperfil'),

    #api django rest framework urls
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/', include(router.urls), name='api'),
    path('api/token/', MyTokenObtainPairView.as_view(), name='Token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh'),

]
