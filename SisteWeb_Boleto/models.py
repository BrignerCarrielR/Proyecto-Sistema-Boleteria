from django.db import models
from principal.constantes import Opciones

motivos = Opciones()
GENERO = motivos.genero()
TIPO_LICENCIA = motivos.tipo_licencia()
GRUPO_SANGUINEO = motivos.grupo_sanguineo()
RUTA = motivos.ruta()


# Create your models here.
class Administrador(models.Model):
    nombre = models.CharField(max_length=100, blank=False, null=True, unique=True)
    contraseña = models.CharField(max_length=20, blank=False, null=False, unique=True)

    class Meta:
        verbose_name = "Administrador"
        verbose_name_plural = "Administrador"
        ordering = ['id']

    def __str__(self):
        return "{}".format(self.nombre)


class Usuario(models.Model):
    nombres = models.CharField(max_length=100, blank=False, null=True, )
    telefono = models.CharField(max_length=10, blank=False, null=True, unique=True)
    ciudad = models.CharField(max_length=100, blank=False, null=True)
    edad = models.IntegerField()
    genero = models.CharField(max_length=1, choices=GENERO, default=GENERO[0][0], blank=True, null=True)
    nom_user = models.CharField(max_length=15, blank=False, null=True, unique=True)
    contraseña = models.CharField(max_length=20, blank=False, null=False, unique=True)

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['id']

    def __str__(self):
        return "{}".format(self.nombres)


class Chofer(models.Model):
    nombres = models.CharField(max_length=200, unique=True, blank=False, null=True)
    apellidos = models.CharField(max_length=200, unique=True, blank=False, null=True)
    cedula = models.CharField(max_length=10, unique=True, blank=False, null=True)
    telefonos = models.CharField(max_length=10, blank=False, null=True)
    tipo_licencia = models.CharField(max_length=2, choices=TIPO_LICENCIA, default=TIPO_LICENCIA[0][0], blank=False,
                                     null=True)
    exp_licencia = models.DateField(blank=False, null=True)
    direccion = models.CharField(max_length=50, blank=False, null=True)
    edad = models.IntegerField(blank=False, null=True)
    provincia = models.CharField(max_length=50, blank=False, null=True)
    ciudad = models.CharField(max_length=50, blank=False, null=True)
    grupo_sanguineo = models.CharField(max_length=3, choices=GRUPO_SANGUINEO, default=GRUPO_SANGUINEO[0][0],
                                       blank=False, null=True)

    def __str__(self):
        return "{}".format(self.nombres)

    # .split(" ")[0], self.apellidos.split(" ")[0] + ".",
    # self.apellidos.split(" ")[1][0] + "."

    class Meta:
        verbose_name = "Chofer"
        verbose_name_plural = "Choferes"
        ordering = ['id']


class Buses(models.Model):
    modelo = models.CharField(max_length=200, blank=False, null=True)
    marca = models.CharField(max_length=200, blank=False, null=True)
    placa = models.CharField(max_length=200, unique=True, blank=False, null=True)
    año_fabricado = models.DateField(blank=False, null=True)
    motor = models.CharField(max_length=200, blank=False, null=True)
    año_modelo = models.DateField(blank=False, null=True)
    chasis = models.CharField(max_length=200, blank=False, null=True)
    kilometraje = models.CharField(max_length=10, blank=False, null=True)
    capacidad_pasajero = models.CharField(max_length=2, blank=False, null=True)
    ruedas = models.CharField(max_length=2, blank=False, null=True)
    ejes = models.CharField(max_length=1, blank=False, null=True)
    propietario = models.CharField(max_length=100, blank=False, null=True)
    cedula = models.CharField(max_length=10, unique=True, blank=False, null=True)
    telefono = models.CharField(max_length=10, blank=False, null=True)
    direccion = models.CharField(max_length=100, blank=False, null=True)
    numerobus = models.CharField(max_length=2, blank=False, null=True)

    class Meta:
        verbose_name = "Bus"
        verbose_name_plural = "Buses"
        ordering = ['id']

    def __str__(self):
        return "{}".format(self.modelo)


class Copiloto(models.Model):
    nombres = models.CharField(max_length=50, blank=False, null=True)
    apellidos = models.CharField(max_length=50, blank=False, null=True)
    cedula = models.CharField(max_length=10, blank=False, null=True, unique=True)
    telefono = models.CharField(max_length=10, blank=False, null=True, unique=True)
    direccion = models.CharField(max_length=50, blank=False, null=True)
    edad = models.IntegerField(blank=True, null=True)
    provincia = models.CharField(max_length=20, blank=False, null=True)
    ciudad = models.CharField(max_length=20, blank=False, null=True)
    grupo_sanguineo = models.CharField(max_length=3, choices=GRUPO_SANGUINEO, default=GRUPO_SANGUINEO[0][0],
                                       blank=False, null=True)

    class Meta:
        verbose_name = "Copiloto"
        verbose_name_plural = "Copilotos"
        ordering = ['id']

    def __str__(self):
        return "{} {} {}".format(self.nombres.split(" ")[0], self.apellidos.split(" ")[0] + ".",
                                 self.apellidos.split(" ")[1][0] + ".")


class Ruta(models.Model):
    nombreRuta = models.CharField(max_length=50)
    abreviatura = models.CharField(max_length=10)

    class Meta:
        verbose_name = "Ruta"
        verbose_name_plural = "Rutas"
        ordering = ['id']

    def __str__(self):
        return "{}".format(self.nombreRuta)


class CabeceraVenta(models.Model):
    chofer = models.ForeignKey(Chofer, on_delete=models.CASCADE)
    copiloto = models.ForeignKey(Copiloto, on_delete=models.CASCADE)
    oficinista = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    buses = models.ForeignKey(Buses, on_delete=models.CASCADE)
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(blank=False, null=True)
    total = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ['id']

    def __str__(self):
        return "{}".format(self.chofer)


class DetalleVenta(models.Model):
    venta = models.ForeignKey(CabeceraVenta, on_delete=models.CASCADE)
    pasajero = models.CharField(max_length=50, blank=False, null=True)
    destino = models.CharField(max_length=50, blank=False, null=True)
    asiento = models.IntegerField(blank=True, null=True)
    hora = models.TimeField(blank=True, null=True)
    costo = models.FloatField(blank=True, null=True)
    modo_pago = models.CharField(max_length=50, blank=False, null=True)

    class Meta:
        verbose_name = "Detalle Venta"
        verbose_name_plural = "Detalles de Ventas"
        ordering = ['id']

    def __str__(self):
        return "{}".format(self.pasajero)
