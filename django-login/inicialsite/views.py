from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from .models import Filme
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

class Dashboard(LoginRequiredMixin,ListView):
    login_url = '/'
    redirect_field_name = 'login'
    model = Filme
    template_name = 'inicialsite/dashboard.html'
    context_object_name = 'dashboard'
    paginate_by = 10
    ordering  = ['-visualizacoes']


class Busca(Dashboard):
    def get_queryset(self, *args, **kwargs):
        termo = self.request.GET.get('termo') or self.request.session['termo']
        qs = super().get_queryset(*args, **kwargs)

        if not termo:
            return qs        
        self.request.session['termo'] = termo
        qs = qs.filter(
            Q(titulo__icontains=termo)|
            Q(categoria__icontains=termo)
        )

        self.request.session.save()

        return qs
        
