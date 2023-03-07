"""principal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path

from SisteWeb_Boleto.views import InicioTemplateView, login_admin, ListaUser, InicioAdministrador, CerrarSecion, \
    NewUser, UpdateUser, DeleteUser, login_User, CerrarSecionUser, list_terramoza_adm, new_terramoza_adm, \
    list_chofer_adm, new_chofer_adm, list_buses_adm, new_buses_adm, Mantenimientos_Administrador, UpdateChofer_adm, \
    DeleteChofer_adm, Update_buses_adm, DeleteBuses_adm, Update_Terramoza_adm, DeleteTerramoza_adm, list_buses_user, \
    list_terramoza_user, list_chofer_user, InicioUsuario, DetalleBuses_adm, DetalleTerramoza_adm, DetalleChofer_adm, \
    List_Venta_adm, new_Venta_user, List_Venta_user, FacturaVenta_user, list_Boletos_user, \
    Facturaboletos_user, FacturaVenta_adm, list_Boletos_adm, Facturaboletos_adm, DetalleBuses_user, \
    DetalleTerramoza_user, DetalleChofer_user

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', InicioTemplateView.as_view(), name="inicio"),
    ####################################### URLS DE INICIOS DE SESION ##################################################
    path('login_admin', login_admin, name='login_admin'),
    path('cerrarsecion', CerrarSecion, name='cerrarsecion'),
    path('login_user', login_User, name='login_user'),
    path('cerrarsecion_user', CerrarSecionUser, name='cerrarsecion_user'),

    ####################################### URLS DE PANTALLAS PRINCIPALES ##############################################
    path('InicioAdministrador', InicioAdministrador.as_view(), name="InicioAdministrador"),
    path('Mantenimientos_Administrador', Mantenimientos_Administrador.as_view(), name="Mantenimientos_Administrador"),
    path('InicioUsuario', InicioUsuario.as_view(), name="InicioUsuario"),

    ####################################### URLS DE LAS LISTAS ##################################################
    path('listausuario', ListaUser.as_view(), name="listausuario"),
    path('list_buses_adm', list_buses_adm.as_view(), name='list_buses_adm'),
    path('list_chofer_adm', list_chofer_adm.as_view(), name='list_chofer_adm'),
    path('list_terramoza_adm', list_terramoza_adm.as_view(), name='list_terramoza_adm'),
    path('list_Venta_adm', List_Venta_adm.as_view(), name='list_Venta_adm'),
    path('list_boletos_adm', list_Boletos_adm.as_view(), name='list_boletos_adm'),
    path('list_chofer_user', list_chofer_user.as_view(), name='list_chofer_user'),
    path('list_terramoza_user', list_terramoza_user.as_view(), name='list_terramoza_user'),
    path('list_buses_user', list_buses_user.as_view(), name='list_buses_user'),
    path('list_Venta_user', List_Venta_user.as_view(), name='list_Venta_user'),
    path('list_boletos_user', list_Boletos_user.as_view(), name='list_boletos_user'),

    ####################################### URLS DE LOS CREATES ##################################################
    path('newuser', NewUser.as_view(), name="newuser"),
    path('new_buses_adm', new_buses_adm.as_view(), name='new_buses_adm'),
    path('new_chofer_adm', new_chofer_adm.as_view(), name='new_chofer_adm'),
    path('new_terramoza_adm', new_terramoza_adm.as_view(), name='new_terramoza_adm'),
    path('new_Venta_user', new_Venta_user.as_view(), name='new_Venta_user'),

    ####################################### URLS DE LOS UPDATES ##################################################
    path('updateUser/<int:pk>', UpdateUser.as_view(), name="updateUser"),
    path('Update_buses_adm/<int:pk>', Update_buses_adm.as_view(), name='Update_buses_adm'),
    path('UpdateChofer_adm/<int:pk>', UpdateChofer_adm.as_view(), name='UpdateChofer_adm'),
    path('Update_Terramoza_adm/<int:pk>', Update_Terramoza_adm.as_view(), name='Update_Terramoza_adm'),

    ####################################### URLS DE LOS DELETES ##################################################
    path('deleteuser/<int:pk>', DeleteUser.as_view(), name="deleteuser"),
    path('DeleteBuses_adm/<int:pk>', DeleteBuses_adm.as_view(), name="DeleteBuses_adm"),
    path('DeleteChofer_adm/<int:pk>', DeleteChofer_adm.as_view(), name="DeleteChofer_adm"),
    path('DeleteTerramoza_adm/<int:pk>', DeleteTerramoza_adm.as_view(), name="DeleteTerramoza_adm"),

    ####################################### URLS DE LOS DETALLES ##################################################
    path('DetalleBuses_adm/<int:pk>', DetalleBuses_adm.as_view(), name="DetalleBuses_adm"),
    path('DetalleChofer_adm/<int:pk>', DetalleChofer_adm.as_view(), name="DetalleChofer_adm"),
    path('DetalleTerramoza_adm/<int:pk>', DetalleTerramoza_adm.as_view(), name="DetalleTerramoza_adm"),
    path('DetalleBuses_user/<int:pk>', DetalleBuses_user.as_view(), name="DetalleBuses_user"),
    path('DetalleChofer_user/<int:pk>', DetalleChofer_user.as_view(), name="DetalleChofer_user"),
    path('DetalleTerramoza_user/<int:pk>', DetalleTerramoza_user.as_view(), name="DetalleTerramoza_user"),

    ####################################### URLS DE LAS FACTURAS ##################################################
    path('FacturaVenta_adm/<int:pk>', FacturaVenta_adm.as_view(), name="FacturaVenta_adm"),
    path('Facturaboletos_adm/<int:pk>', Facturaboletos_adm.as_view(), name="Facturaboletos_adm"),
    path('FacturaVenta_user/<int:pk>', FacturaVenta_user.as_view(), name="FacturaVenta_user"),
    path('Facturaboletos_user/<int:pk>', Facturaboletos_user.as_view(), name="Facturaboletos_user"),


]
