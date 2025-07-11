from django.contrib import admin
from .models import Solicitud, UsuarioPermitido
from django.utils.html import format_html
from django.db.models import Count

# Registro del modelo UsuarioPermitido
@admin.register(UsuarioPermitido)
class UsuarioPermitidoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'codigo_validacion')
    search_fields = ('nombre', 'email')

# Registro del modelo Solicitud con estadísticas y resumen
@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'categoria', 'mensaje_corto')
    list_filter = ('categoria',)
    search_fields = ('nombre', 'email', 'mensaje')
    ordering = ('-id',)

    def mensaje_corto(self, obj):
        return (obj.mensaje[:50] + '...') if len(obj.mensaje) > 50 else obj.mensaje
    mensaje_corto.short_description = 'Mensaje'

    def changelist_view(self, request, extra_context=None):
        total = Solicitud.objects.count()
        por_categoria = Solicitud.objects.values('categoria').annotate(cantidad=Count('id'))

        resumen = f"<p><strong>Total de solicitudes:</strong> {total}</p>"
        for item in por_categoria:
            resumen += f"<p><strong>{item['categoria']}:</strong> {item['cantidad']}</p>"

        extra_context = extra_context or {}
        extra_context['title'] = 'Panel de Solicitudes'
        extra_context['resumen_estadistico'] = format_html(resumen)

        return super().changelist_view(request, extra_context=extra_context)
