from django.contrib import admin

# Register your models here.
from .models import Usuario, Administrador, CabeceraVenta, DetalleVenta, Ruta

admin.site.register(Ruta)
class TableAdmin(admin.ModelAdmin):
    list_display = ['nombre','contraseña']
    search_fields = ['nombre']
    list_per_page = 5

admin.site.register(Administrador,TableAdmin)


# class TableRuta(admin.ModelAdmin):
#     list_display = ['nombreRuta','abreviatura']
#     search_fields = ['nombreRuta']
#     list_per_page = 5
#
# admin.site.register(Ruta,TableRuta)
#
#
class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 0

@admin.register(CabeceraVenta)
class FacturaAdmin(admin.ModelAdmin):
    inlines = (DetalleVentaInline, )
    list_display = ('chofer', 'copiloto', 'oficinista', 'buses', 'ruta', 'total', )
    # list_per_page = 20
    ordering = ('-fecha_hora',)
    list_filter = ('chofer', 'ruta')