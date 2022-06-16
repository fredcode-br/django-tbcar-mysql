"""tbcar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import urls

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path ('accounts/registrar/', Registrar.as_view(), name='url_register'),
    path('admin/', admin.site.urls),
    path('', home, name='url_principal'),
    path('cadastro_cliente/', cadastro_cliente, name='url_cadastro_cliente'),
    path('lista_clientes/', lista_clientes, name='url_lista_clientes'),
    path('cadastro_veiculo/',cadastro_veiculo, name='url_cadastro_veiculo'),
    path('lista_veiculos/', lista_veiculos, name='url_lista_veiculos'),
    #path('tabela/', tabela, name='url_tabela'),
    path ('cadastro_fabricante/', cadastro_fabricante, name ='url_cadastro_fabricante'),
    path ('lista_fabricantes/', lista_fabricantes, name ='url_lista_fabricantes'),
    path ('altera_cliente/<int:id>/', altera_cliente, name='url_altera_cliente'),
    path ('exclua_cliente/<int:id>/', exclua_cliente, name='url_exclua_cliente'),
    path ('altera_veiculo/<int:id>/', altera_veiculo, name='url_altera_veiculo'),
    path ('exclua_veiculo/<int:id>/', exclua_veiculo, name='url_exclua_veiculo'),
    path ('altera_fabricante/<int:id>/', altera_fabricante, name='url_altera_fabricante'),
    path ('exclua_fabricante/<int:id>/', exclua_fabricante, name='url_exclua_fabricante'),
    path ('cadastro_tabela/', cadastro_tabela, name = 'url_cadastro_tabela'),
    path ('lista_tabela/', lista_tabela, name='url_lista_tabela'),
    path ('altera_tabela/<int:id>/', altera_tabela, name='url_altera_tabela'),
    path ('exclua_tabela/<int:id>/', exclua_tabela, name='url_exclua_tabela'),
    path ('cadastro_rotativo/', cadastro_rotativo, name='url_cadastro_rotativo'),
    path ('atualiza_rotativo/<int:id>/', atualiza_rotativo, name='url_atualiza_rotativo'),
    path ('lista_rotativos/', lista_rotativos, name='url_lista_rotativos'),
    path ('exclua_rotativo/<int:id>/', exclua_rotativo, name='url_exclua_rotativo'),
    path ('cadastro_mensalista/', cadastro_mensalista, name='url_cadastro_mensalista'),
    path ('atualiza_mensalista/<int:id>/', atualiza_mensalista, name='url_atualiza_mensalista'),
    path ('lista_mensalistas/', lista_mensalistas, name='url_lista_mensalistas'),
    path ('exclua_mensalista/<int:id>/', exclua_mensalista, name='url_exclua_mensalista'),
]
from django.conf.urls.static import static


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
