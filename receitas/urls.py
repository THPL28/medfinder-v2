from django.urls import path
from django.contrib.auth import views as auth_views
from .views import inicio, ReceitaUploadView, resultado_view, historico_receitas, contato, register_view, list_medicines_view

urlpatterns = [
    path('', inicio, name='inicio'), 
    path('register/', register_view, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Corrigido o path para login
    path('upload_receita/', ReceitaUploadView.as_view(), name='upload_receita'),
    path('resultado/<int:pk>/', resultado_view, name='resultado'),
    path('historico/', historico_receitas, name='historico_receitas'),
    path('medicamentos/', list_medicines_view, name='medicamentos'),
    path('contato/', contato, name='contato'),
]
