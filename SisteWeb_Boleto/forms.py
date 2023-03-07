from django.forms import ModelForm
from django import forms
from datetime import datetime

from SisteWeb_Boleto.models import Usuario, Chofer, Buses, Copiloto, CabeceraVenta, Ruta


class Userform(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = Usuario
        fields = '__all__'
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '09...'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Los Rios - Vinces'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'nom_user': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: userName12'}),
            'contraseña': forms.TextInput(attrs={'class': 'form-control'}),
        }


class Choferform(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = Chofer
        fields = '__all__'
        widgets = {
            'telefonos': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '09...'}),
            'provincia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Los Ríos'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Vinces'}),
            'exp_licencia': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Nombres'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Apellidos'}),
            'cedula': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Cedula'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Dirección'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Edad'}),
        }


class BusesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = Buses
        fields = '__all__'
        widgets = {
            'año_fabricado': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'año_modelo': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Modelo'}),
            'placa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Placa'}),
            'motor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Numero del Motor'}),
            'chasis': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Numero del Chasís'}),
            'ejes': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Cantidad de Ejes'}),
            'ruedas': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Numero de Ruedas'}),
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Marca'}),
            'kilometraje': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el Kilomtraje '
                                                                                            'Recorrido'}),
            'capacidad_pasajero': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la '
                                                                                                   'Capacidad de '
                                                                                                   'Pasajeros'}),
            'propietario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Nombre'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Cédula'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Teléfono'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Dirección'}),
            'numerobus': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Numero de Disco'}),
        }


class CopilotoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = Copiloto
        fields = '__all__'
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Nombre'}),
            'cedula': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Cédula'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Direccién'}),
            'provincia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Provincia'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Apellidos'}),
            'telefono': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Télefono'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Ciudad'}),
        }


class VentaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = CabeceraVenta
        fields = '__all__'
        # widgets = {
        #     'fecha_hora': forms.DateInput(
        #         format=('%Y-%m-%d'),
        #         attrs={'type': 'datetime-local', 'class':'form-control'}),
        # }
class buscarventa(forms.Form):
    chofer= forms.CharField(required=False)
    copiloto= forms.CharField(required=False)
    oficinista = forms.CharField(required=False)
    buses = forms.CharField(required=False)
    fecha_hora = forms.DateField(required=False)
    ruta = forms.ModelChoiceField(queryset=Ruta.objects.all(), required=False)

