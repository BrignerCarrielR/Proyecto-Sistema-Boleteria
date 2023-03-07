from django.shortcuts import render
import json
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from datetime import datetime

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from SisteWeb_Boleto.forms import Userform, Choferform, BusesForm, CopilotoForm, VentaForm
from SisteWeb_Boleto.models import Administrador, Usuario, Chofer, Buses, Copiloto, CabeceraVenta, DetalleVenta, Ruta


class InicioTemplateView(TemplateView):
    template_name = "Inicio.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rol'] = 'ELIGA SU ROL'
        context['query'] = self.request.GET.get("query") or ""
        return context

########################################################################################################################
############################################ VISTAS DE LOGUEO ##########################################################
########################################################################################################################


"""------------------------------------------------ADMINISTRADOR-----------------------------------------------------"""

def login_admin(request):
    data = {
        'rol': "ADMINISTRADOR",
        'Inic': '/InicioAdministrador'
    }
    if request.method == 'POST':
        try:
            detalleAdmin = Administrador.objects.get(nombre=request.POST['nombre'],
                                                     contraseña=request.POST['contraseña'])
            request.session['id'] = detalleAdmin.id
            request.session['nombre'] = detalleAdmin.nombre
            return render(request, 'Administrador/Base_admin.html', data)
        except Administrador.DoesNotExist as e:
            messages.success(request, 'Nombre de Administrador o Contraseña incorrecta..!')
    return render(request, 'loginAdmin.html', data)

def CerrarSecion(request):
    try:
        del request.session['nombre']
    except:
        return render(request, 'Inicio.html')
    return render(request, 'Inicio.html')


"""------------------------------------------------USUARIO-----------------------------------------------------------"""

def login_User(request):
    data = {
        'rol': 'OFICINISTA',
        'Inic': '/InicioUsuario'
    }
    if request.method == 'POST':
        try:
            detalleUsuario = Usuario.objects.get(nom_user=request.POST['nom_user'],
                                                 contraseña=request.POST['contraseña'])
            print('Usuario= ', detalleUsuario)
            request.session['id'] = detalleUsuario.id
            request.session['nom_user'] = detalleUsuario.nom_user
            return render(request, 'Usuario/Base_user.html', data)
        except Usuario.DoesNotExist as e:
            messages.success(request, 'Nombre de Usuario o Contraseña incorrecta..!')
    return render(request, 'loginUser.html', data)

def CerrarSecionUser(request):
    try:
        del request.session['nom_user']
    except:
        return render(request, 'Inicio.html')
    return render(request, 'Inicio.html')

########################################################################################################################
########################################## VISTAS DE PANTALLAS INICIOS #################################################
########################################################################################################################


"""------------------------------------------------ADMINISTRADOR-----------------------------------------------------"""

class InicioAdministrador(TemplateView):
    template_name = 'Administrador/Base_admin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'INICIO ADMIN'
        context['rol'] = "ADMINISTRADOR"
        context['Inic'] = "/InicioAdministrador"
        context['url_anterior'] = "/"
        return context
class Mantenimientos_Administrador(TemplateView):
    template_name = 'Administrador/mantenimientos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'MANTENIMIENTOS'
        context['rol'] = "MANTENIMIENTOS"
        context['Inic'] = "/InicioAdministrador"
        context['url_anterior'] = "/"
        return context


"""------------------------------------------------USUARIO-----------------------------------------------------------"""

class InicioUsuario(TemplateView):
    template_name = 'Usuario/Base_user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'INICIO USER'
        context['rol'] = "USUAIRO"
        context['Inic'] = "/InicioUsuario"
        context['url_anterior'] = "/"
        return context
########################################################################################################################
############################################# VISTAS DE LAS LISTAS #####################################################
########################################################################################################################

"""------------------------------------------------ADMINISTRADOR-----------------------------------------------------"""

class ListaUser(ListView):
    template_name = "Administrador/usuarios/lista_user.html"
    context_object_name = 'lis_user'
    model = Usuario

    def get_queryset(self):
        query = self.request.GET.get("query")
        print(query)
        if query:
            return self.model.objects.filter(nombres__icontains=query)
        else:
            return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'LISTADO DE USUARIOS'
        context['cancelar_url'] = '/InicioAdministrador'
        context['crear_url'] = '/newuser'
        context['rol'] = 'LISTADO DE USUARIOS'
        context['Inic'] = '/InicioAdministrador'
        context['query'] = self.request.GET.get("query") or ""
        return context

class list_chofer_adm(ListView):
    template_name = "Administrador/chofer/list_chofer.html"
    model = Chofer
    context_object_name = 'choferes'

    def get_queryset(self):
        queryset = super().get_queryset()
        nombre = self.request.GET.get('nombre')
        apellido = self.request.GET.get('apellido')
        provincia = self.request.GET.get('provincia')
        ciudad = self.request.GET.get('ciudad')
        t_licencia = self.request.GET.get('t_licencia')
        if nombre:
            queryset = queryset.filter(nombres__contains=nombre)
        if apellido:
            queryset = queryset.filter(apellidos__contains=apellido)
        if provincia:
            queryset = queryset.filter(provincia__contains=provincia)
        if ciudad:
            queryset = queryset.filter(ciudad__contains=ciudad)
        if t_licencia:
            queryset = queryset.filter(tipo_licencia__contains=t_licencia)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rol'] = 'LISTA DE CHOFERES'
        context['Inic'] = '/InicioAdministrador'
        context['crear_url'] = '/new_chofer_adm'
        context['cancelar_url'] = '/Mantenimientos_Administrador'
        context['query'] = self.request.GET.get("query") or ""
        return context

class list_buses_adm(ListView):
    template_name = "Administrador/buses/list_buses.html"
    context_object_name = 'buses'
    model = Buses

    def get_queryset(self):
        queryset = super().get_queryset()
        marca = self.request.GET.get('marca')
        modelo = self.request.GET.get('modelo')
        asiento = self.request.GET.get('asiento')
        if marca:
            queryset = queryset.filter(marca__contains=marca)
        if modelo:
            queryset = queryset.filter(modelo__contains=modelo)
        if asiento:
            queryset = queryset.filter(capacidad_pasajero__contains=asiento)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rol'] = 'LISTA DE BUSES'
        context['Inic'] = '/InicioAdministrador'
        context['crear_url'] = '/new_buses_adm'
        context['cancelar_url'] = '/Mantenimientos_Administrador'
        context['query'] = self.request.GET.get("query") or ""
        return context

class list_terramoza_adm(ListView):
    template_name = "Administrador/terramoza/list_terramoza.html"
    model = Copiloto
    context_object_name = 'copiloto'

    def get_queryset(self):
        queryset = super().get_queryset()
        nombre = self.request.GET.get('nombre')
        apellido = self.request.GET.get('apellido')
        provincia = self.request.GET.get('provincia')
        ciudad = self.request.GET.get('ciudad')
        if nombre:
            queryset = queryset.filter(nombres__contains=nombre)
        if apellido:
            queryset = queryset.filter(apellidos__contains=apellido)
        if provincia:
            queryset = queryset.filter(provincia__contains=provincia)
        if ciudad:
            queryset = queryset.filter(ciudad__contains=ciudad)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rol'] = 'LISTA DE COPILOTO'
        context['Inic'] = '/InicioAdministrador'
        context['crear_url'] = '/new_terramoza_adm'
        context['cancelar_url'] = '/Mantenimientos_Administrador'
        context['query'] = self.request.GET.get("query") or ""
        return context


"""------------------------------------------------USUARIO-----------------------------------------------------------"""

class list_chofer_user(ListView):
    template_name = "Usuario/chofer/list_chofer.html"
    model = Chofer
    context_object_name = 'choferes'

    def get_queryset(self):
        queryset = super().get_queryset()
        nombre = self.request.GET.get('nombre')
        apellido = self.request.GET.get('apellido')
        provincia = self.request.GET.get('provincia')
        ciudad = self.request.GET.get('ciudad')
        t_licencia = self.request.GET.get('t_licencia')
        if nombre:
            queryset = queryset.filter(nombres__contains=nombre)
        if apellido:
            queryset = queryset.filter(apellidos__contains=apellido)
        if provincia:
            queryset = queryset.filter(provincia__contains=provincia)
        if ciudad:
            queryset = queryset.filter(ciudad__contains=ciudad)
        if t_licencia:
            queryset = queryset.filter(tipo_licencia__contains=t_licencia)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rol'] = 'LISTADO DE CHOFERES'
        context['Inic'] = '/InicioUsuario'
        context['cancelar_url'] = '/InicioUsuario'
        context['query'] = self.request.GET.get("query") or ""
        return context


class list_buses_user(ListView):
    template_name = "Usuario/buses/list_buses.html"
    context_object_name = 'buses'
    model = Buses

    def get_queryset(self):
        queryset = super().get_queryset()
        marca = self.request.GET.get('marca')
        modelo = self.request.GET.get('modelo')
        asiento = self.request.GET.get('asiento')
        if marca:
            queryset = queryset.filter(marca__contains=marca)
        if modelo:
            queryset = queryset.filter(modelo__contains=modelo)
        if asiento:
            queryset = queryset.filter(capacidad_pasajero__contains=asiento)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rol'] = 'LISTADO DE BUSES'
        context['Inic'] = '/InicioUsuario'
        context['cancelar_url'] = '/InicioUsuario'
        context['query'] = self.request.GET.get("query") or ""
        return context


class list_terramoza_user(ListView):
    template_name = "Usuario/terramoza/list_terramoza.html"
    model = Copiloto
    context_object_name = 'copiloto'

    def get_queryset(self):
        queryset = super().get_queryset()
        nombre = self.request.GET.get('nombre')
        apellido = self.request.GET.get('apellido')
        provincia = self.request.GET.get('provincia')
        ciudad = self.request.GET.get('ciudad')
        if nombre:
            queryset = queryset.filter(nombres__contains=nombre)
        if apellido:
            queryset = queryset.filter(apellidos__contains=apellido)
        if provincia:
            queryset = queryset.filter(provincia__contains=provincia)
        if ciudad:
            queryset = queryset.filter(ciudad__contains=ciudad)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rol'] = 'LISTADO DE COPILOTOS'
        context['Inic'] = '/InicioUsuario'
        context['cancelar_url'] = '/InicioUsuario'
        context['query'] = self.request.GET.get("query") or ""
        return context

########################################################################################################################
########################################### VISTAS DE LOS CREATES ######################################################
########################################################################################################################


"""------------------------------------------------ADMINISTRADOR-----------------------------------------------------"""

class NewUser(CreateView):
    template_name = 'Administrador/usuarios/nuevo_user.html'
    model = Usuario
    success_url = reverse_lazy('listausuario')
    form_class = Userform

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'REGISTRAR USUARIO'
        context['action_save'] = '/newuser'
        context['rol'] = 'NUEVO USUARIO'
        context['Inic'] = '/InicioAdministrador'
        context['cancelar_url'] = '/listausuario'
        context['action'] = 'add'
        return context


class new_chofer_adm(CreateView):
    template_name = "Administrador/chofer/create_chofer.html"
    model = Chofer
    success_url = reverse_lazy('list_chofer_adm')
    form_class = Choferform

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_save'] = '/new_chofer_adm'
        context['titulo'] = 'REGISTRAR CHOFER'
        context['rol'] = 'REGISTRAR CHOFER'
        context['Inic'] = '/InicioAdministrador'
        context['cancelar_url'] = '/list_chofer_adm'
        context['action'] = 'add'
        return context

class new_buses_adm(CreateView):
    template_name = "Administrador/buses/create_buses.html"
    model = Buses
    success_url = reverse_lazy('list_buses_adm')
    form_class = BusesForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_save'] = '/new_buses_adm'
        context['titulo'] = 'REGISTRAR BUS'
        context['rol'] = 'REGISTRAR BUS'
        context['Inic'] = '/InicioAdministrador'
        context['cancelar_url'] = '/list_buses_adm'
        context['action'] = 'add'
        return context

class new_terramoza_adm(CreateView):
    template_name = "Administrador/terramoza/create_terramoza.html"
    model = Copiloto
    success_url = reverse_lazy('list_terramoza_adm')
    form_class = CopilotoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_save'] = '/new_terramoza_adm'
        context['titulo'] = 'REGISTRAR COPILOTO'
        context['rol'] = 'REGISTRAR COPILOTO'
        context['Inic'] = '/InicioAdministrador'
        context['cancelar_url'] = '/list_terramoza_adm'
        context['action'] = 'add'
        return context


########################################################################################################################
########################################### VISTAS DE LOS UPDATES ######################################################
########################################################################################################################

"""------------------------------------------------ADMINISTRADOR-----------------------------------------------------"""

class UpdateUser(UpdateView):
    model = Usuario
    template_name = 'Administrador/usuarios/nuevo_user.html'
    success_url = reverse_lazy('listausuario')
    form_class = Userform

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_save'] = self.request.path
        context['titulo'] = 'MODIFICAR USUARIO'
        context['rol'] = 'MODIFICAR USUARIO'
        context['Inic'] = '/InicioAdministrador'
        context['cancelar_url'] = '/listausuario'
        return context



class UpdateChofer_adm(UpdateView):
    template_name = "Administrador/chofer/create_chofer.html"
    model = Chofer
    success_url = reverse_lazy('list_chofer_adm')
    form_class = Choferform

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_save'] = self.request.path
        context['titulo'] = 'MODIFICAR CHOFER'
        context['rol'] = 'MODIFICAR CHOFER'
        context['Inic'] = '/InicioAdministrador'
        context['cancelar_url'] = '/list_chofer_adm'
        return context

class Update_buses_adm(UpdateView):
    model = Buses
    template_name = "Administrador/buses/create_buses.html"
    success_url = reverse_lazy('list_buses_adm')
    form_class = BusesForm

    # queryset = Cliente.objects.get(pk=request.GET.get("id"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_save'] = self.request.path
        context['titulo'] = 'MODIFICAR BUS'
        context['rol'] = 'MODIFICAR BUS'
        context['Inic'] = '/InicioAdministrador'
        context['cancelar_url'] = '/list_buses_adm'
        return context


class Update_Terramoza_adm(UpdateView):
    model = Copiloto
    template_name = "Administrador/terramoza/create_terramoza.html"
    success_url = reverse_lazy('list_terramoza_adm')
    form_class = CopilotoForm

    # queryset = Cliente.objects.get(pk=request.GET.get("id"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_save'] = self.request.path
        context['titulo'] = 'MODIFICAR COPILOTO'
        context['rol'] = 'MODIFICAR COPILOTO'
        context['Inic'] = '/InicioAdministrador'
        context['cancelar_url'] = '/list_terramoza_adm'
        return context
########################################################################################################################
########################################### VISTAS DE LOS DELETES ######################################################
########################################################################################################################


"""------------------------------------------------ADMINISTRADOR-----------------------------------------------------"""

class DeleteUser(DeleteView):
    model = Usuario
    template_name = "Administrador/usuarios/deleteUser.html"
    success_url = reverse_lazy('listausuario')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_save'] = self.request.path
        context['titulo'] = 'ELIMINAR USUARIO'
        context['rol'] = 'ELIMINAR USUARIO'
        context['cancelar_url'] = '/listausuario'
        return context


class DeleteChofer_adm(DeleteView):
    model = Chofer
    template_name = "Administrador/chofer/deleteChofer.html"
    success_url = reverse_lazy('list_chofer_adm')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_save'] = self.request.path
        context['titulo'] = 'ELIMINAR CHOFER'
        context['rol'] = 'ELIMINAR CHOFER'
        context['cancelar_url'] = '/list_chofer_adm'
        return context


class DeleteBuses_adm(DeleteView):
    model = Buses
    template_name = "Administrador/buses/deleteBuses.html"
    success_url = reverse_lazy('list_buses_adm')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_save'] = self.request.path
        context['titulo'] = 'ELEMINAR BUS'
        context['rol'] = 'ELIMINAR BUS'
        context['Inic'] = '/InicioAdministrador'
        context['cancelar_url'] = '/list_buses_adm'
        return context

class DeleteTerramoza_adm(DeleteView):
    model = Copiloto
    template_name = "Administrador/terramoza/deleteTerramoza.html"
    success_url = reverse_lazy('list_terramoza_adm')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_save'] = self.request.path
        context['titulo'] = 'ELEMINAR COPILOTO'
        context['rol'] = 'ELIMINAR COPILOTO'
        context['Inic'] = '/InicioAdministrador'
        context['cancelar_url'] = '/list_terramoza_adm'
        return context

########################################################################################################################
########################################### VISTAS DE LAS DETALLES #####################################################
########################################################################################################################


"""------------------------------------------------ADMINISTRADOR-----------------------------------------------------"""

class DetalleChofer_adm(DeleteView):
    model = Chofer
    template_name = "Administrador/chofer/detalleco.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_save'] = self.request.path
        context['titulo'] = 'DETALLE DEL CHOFER'
        context['rol'] = 'DETALLE DEL CHOFER'
        context['cancelar_url'] = '/list_chofer_adm'
        return context



class DetalleBuses_adm(DeleteView):
    model = Buses
    template_name = "Administrador/buses/detallebus.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_save'] = self.request.path
        context['titulo'] = 'DETALLE DEL BUS'
        context['rol'] = 'DETALLE DEL BUS'
        context['Inic'] = '/InicioAdministrador'
        context['cancelar_url'] = '/list_buses_adm'
        return context


class DetalleTerramoza_adm(DeleteView):
    model = Copiloto
    template_name = "Administrador/terramoza/detalleteramoza.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_save'] = self.request.path
        context['titulo'] = 'DETALLE DEL COPILOTO'
        context['rol'] = 'DETALLE DEL COPILOTO'
        context['Inic'] = '/InicioAdministrador'
        context['cancelar_url'] = '/list_terramoza_adm'
        return context


"""------------------------------------------------USUARIO-----------------------------------------------------------"""

class DetalleChofer_user(DeleteView):
    model = Chofer
    template_name = "Usuario/chofer/detalleco.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_save'] = self.request.path
        context['titulo'] = 'DETALLE DEL CHOFER'
        context['rol'] = 'DETALLE DEL CHOFER'
        context['Inic'] = '/InicioUsuario'
        context['cancelar_url'] = '/list_chofer_user'
        return context

class DetalleTerramoza_user(DeleteView):
    model = Copiloto
    template_name = "Usuario/terramoza/detalleteramoza.html"
    success_url = reverse_lazy('list_terramoza_adm')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_save'] = self.request.path
        context['titulo'] = 'DETALLE DEL COPILOTO'
        context['rol'] = 'DETALLE DEL COPILOTO'
        context['Inic'] = '/InicioUsuario'
        context['cancelar_url'] = '/list_terramoza_user'
        return context

class DetalleBuses_user(DeleteView):
    model = Buses
    template_name = "Usuario/buses/detallebus.html"
    success_url = reverse_lazy('list_buses_adm')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_save'] = self.request.path
        context['titulo'] = 'DETALLE DEL BUS'
        context['rol'] = 'DETALLE DEL BUS'
        context['Inic'] = '/InicioUsuario'
        context['cancelar_url'] = '/list_buses_user'
        return context
########################################################################################################################
############################################# VISTAS DE LAS VENTAS #####################################################
########################################################################################################################


"""------------------------------------------------ADMINISTRADOR-----------------------------------------------------"""

class List_Venta_adm(ListView):
    template_name = "Administrador/venta/Listaventa.html"
    context_object_name = 'lis_venta'
    model = CabeceraVenta

    def get_queryset(self):
        queryset = super().get_queryset()
        chofer = self.request.GET.get('chofer')
        copiloto = self.request.GET.get('copiloto')
        fechafin = self.request.GET.get('fechafin')
        fechainicio = self.request.GET.get('fechainicio')
        oficinista = self.request.GET.get('oficinista')
        ruta = self.request.GET.get('ruta')
        print('ruta', ruta)
        if chofer:
            queryset = queryset.filter(chofer__nombres__contains=chofer)
        if copiloto:
            queryset = queryset.filter(copiloto__nombres__contains=copiloto)
        if fechafin:
            queryset = queryset.filter(fecha_hora__lt=fechafin)
        if fechainicio:
            queryset = queryset.filter(fecha_hora__gt=fechainicio)
        if oficinista:
            queryset = queryset.filter(oficinista__nom_user__contains=oficinista)
        if ruta:
            queryset = queryset.filter(ruta_id=ruta)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'LISTADO DE VENTAS'
        context['cancelar_url'] = '/Mantenimientos_Administrador'
        context['crear_url'] = '/new_Venta_adm'
        context['rol'] = 'LISTADO DE VENTAS'
        context['Inic'] = '/InicioAdministrador'
        context['query'] = self.request.GET.get("query") or ""
        context['chofer'] = Chofer.objects.all()
        context['copiloto'] = Copiloto.objects.all()
        return context

class FacturaVenta_adm(DeleteView):
    model = CabeceraVenta
    template_name = "Administrador/venta/detalle.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detalles'] = DetalleVenta.objects.all()
        context['titulo'] = 'FACTURA DEL BOLETO'
        context['rol'] = 'FACTURA DEL BOLETO'
        context['cancelar_url'] = '/list_Venta_adm'
        return context


"""------------------------------------------------USUARIO-----------------------------------------------------------"""

class List_Venta_user(ListView):
    template_name = "Usuario/venta/Listaventa.html"
    context_object_name = 'lis_venta'
    model = CabeceraVenta

    def get_queryset(self):
        queryset = super().get_queryset()
        chofer = self.request.GET.get('chofer')
        copiloto = self.request.GET.get('copiloto')
        fechafin = self.request.GET.get('fechafin')
        fechainicio = self.request.GET.get('fechainicio')
        oficinista = self.request.GET.get('oficinista')
        ruta = self.request.GET.get('ruta')
        print('ruta', ruta)
        if chofer:
            queryset = queryset.filter(chofer__nombres__contains=chofer)
        if copiloto:
            queryset = queryset.filter(copiloto__nombres__contains=copiloto)
        if fechafin:
            queryset = queryset.filter(fecha_hora__lt=fechafin)
        if fechainicio:
            queryset = queryset.filter(fecha_hora__gt=fechainicio)
        if oficinista:
            queryset = queryset.filter(oficinista__nom_user__contains=oficinista)
        if ruta:
            queryset = queryset.filter(ruta_id=ruta)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'LISTADO DE VENTAS'
        context['cancelar_url'] = '/InicioUsuario'
        context['crear_url'] = '/new_Venta_user'
        context['rol'] = 'LISTADO DE VENTAS'
        context['Inic'] = '/InicioUsuario'
        context['ruta'] = Ruta.objects.all().values("id", "nombreRuta")
        context['query'] = self.request.GET.get("query") or ""
        context['chofer'] = Chofer.objects.all()
        context['copiloto'] = Copiloto.objects.all()
        return context


class new_Venta_user(CreateView):
    template_name = 'Usuario/venta/create.html'
    model = CabeceraVenta
    form_class = VentaForm
    success_url = reverse_lazy('list_Venta_user')

    # print(Chofer.objects.all().values("id","nombres")) Aquí hacía una prueba, me debe mostrar el queryset
    # de solo los id y nombres

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_save'] = 'new_Venta_user'
        context['titulo'] = 'REGISTRAR VENTA'
        context['rol'] = 'NUEVO VENTA'
        context['Inic'] = '/InicioUsuario'
        context['cancelar_url'] = '/list_Venta_user'
        context['chofer'] = Chofer.objects.all().values("id", "nombres")
        context['copiloto'] = Copiloto.objects.all().values("id", "nombres")
        context['ruta'] = Ruta.objects.all().values("id", "nombreRuta")
        context['bus'] = Buses.objects.all().values("id", "modelo", "capacidad_pasajero")
        context['action'] = 'add'
        return context

    def post(self, request, *args, **kwargs):
        resp = {}
        data = json.loads(request.body)
        print(type(CabeceraVenta().fecha_hora))

        try:
            data = json.loads(request.body)
            if data['action'] == 'add':
                with transaction.atomic():
                    Ven = CabeceraVenta()
                    Ven.chofer_id = int(data['chofer'])
                    Ven.copiloto_id = int(data['copiloto'])
                    Ven.oficinista_id = int(data['oficinista'])
                    Ven.buses_id = int(data['bus'])
                    Ven.ruta_id = int(data['ruta'])
                    Ven.fecha_hora = datetime.strptime(data['fecha_hora'], '%d/%m/%Y %H:%M:%S')
                    Ven.total = float(data['total'])
                    items = data['boleto']
                    Ven.save()
                    for item in items:
                        detalle = DetalleVenta(
                            venta_id=Ven.id,
                            pasajero=item['pasajero'],
                            destino=item['destino'],
                            asiento=item['asiento'],
                            hora=datetime.strptime(item['hora'], '%d/%m/%Y %H:%M:%S'),
                            costo=item['costo'],
                            modo_pago=item['modoPago'])
                        detalle.save()
                        resp["grabar"] = "ok"
            else:
                print('NADA')
        except Exception as e:
            resp["grabar"] = str(e)
            print(e)

        return JsonResponse(resp, safe="false")


class FacturaVenta_user(DeleteView):
    model = CabeceraVenta
    template_name = "Usuario/venta/detalle.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detalles'] = DetalleVenta.objects.all()
        context['titulo'] = 'FACTURA'
        context['rol'] = 'FACTURA DE LA VENTA'
        context['cancelar_url'] = '/list_Venta_user'
        return context


########################################################################################################################
########################################### VISTAS DE LOS BOLETOS ######################################################
########################################################################################################################

"""------------------------------------------------ADMINISTRADOR-----------------------------------------------------"""

class list_Boletos_adm(ListView):
    template_name = "Administrador/boletos/list.html"
    model = DetalleVenta
    context_object_name = 'boletos'

    def get_queryset(self):
        queryset = super().get_queryset()
        pasajero = self.request.GET.get('pasajero')
        chofer = self.request.GET.get('chofer')
        oficinista = self.request.GET.get('oficinista')
        fechainicio = self.request.GET.get('fechainicio')
        fechafin = self.request.GET.get('fechafin')
        destino = self.request.GET.get('destino')
        print(destino)
        if pasajero:
            queryset = queryset.filter(pasajero__contains=pasajero)
        if chofer:
            queryset = queryset.filter(venta__chofer__nombres__contains=chofer)
        if fechainicio:
            queryset = queryset.filter(hora__gt=fechainicio)
        if fechafin:
            queryset = queryset.filter(hora__lt=fechafin)
        if oficinista:
            queryset = queryset.filter(venta__oficinista__nom_user__contains=oficinista)
        if destino:
            queryset = queryset.filter(destino__contains=destino)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rol'] = 'LISTADO DE BOLETOS VENDIDOS'
        context['Inic'] = '/InicioAdministrador'
        context['cancelar_url'] = '/InicioAdministrador'
        context['query'] = self.request.GET.get("query") or ""
        return context

class Facturaboletos_adm(DeleteView):
    model = DetalleVenta
    template_name = "Administrador/boletos/detalle.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detalles'] = DetalleVenta.objects.all()
        context['titulo'] = 'FACTURA DEL BOLETO'
        context['Inic'] = '/InicioAdministrador'
        context['rol'] = 'FACTURA DEL BOLETO'
        context['cancelar_url'] = '/list_boletos_adm'
        return context


"""------------------------------------------------USUARIO-----------------------------------------------------------"""

class list_Boletos_user(ListView):
    template_name = "Usuario/boletos/list.html"
    model = DetalleVenta
    context_object_name = 'boletos'

    def get_queryset(self):
        queryset = super().get_queryset()
        pasajero = self.request.GET.get('pasajero')
        chofer = self.request.GET.get('chofer')
        oficinista = self.request.GET.get('oficinista')
        fechainicio = self.request.GET.get('fechainicio')
        fechafin = self.request.GET.get('fechafin')
        destino = self.request.GET.get('destino')
        print(destino)
        if pasajero:
            queryset = queryset.filter(pasajero__contains=pasajero)
        if chofer:
            queryset = queryset.filter(venta__chofer__nombres__contains=chofer)
        if fechainicio:
            queryset = queryset.filter(hora__gt=fechainicio)
        if fechafin:
            queryset = queryset.filter(hora__lt=fechafin)
        if oficinista:
            queryset = queryset.filter(venta__oficinista__nom_user__contains=oficinista)
        if destino:
            queryset = queryset.filter(destino__contains=destino)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rol'] = 'LISTADO DE BOLETOS VENDIDOS'
        context['Inic'] = '/InicioUsuario'
        context['cancelar_url'] = '/InicioUsuario'
        context['query'] = self.request.GET.get("query") or ""
        return context


class Facturaboletos_user(DeleteView):
    model = DetalleVenta
    template_name = "Usuario/boletos/detalle.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detalles'] = DetalleVenta.objects.all()
        context['titulo'] = 'FACTURA DEL BOLETO'
        context['rol'] = 'FACTURA DEL BOLETO'
        context['cancelar_url'] = '/list_boletos_user'
        return context

