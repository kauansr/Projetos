from django.urls import path
from .views import Dashboard, Busca

app_name='inicialsite'

urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),
    path('busca/', Busca.as_view(), name='busca'),
]
