from django.urls import path
from .views import (
    index,
    contacto_view,
    servicios_view,
    nosotros_view,
    registro_view,
    validar_cuenta_view,
    login_view,
    logout_view, 
    noticias_view, 
    consultas_api_view,
    dashboard_view,
    editar_solicitud_view,
    eliminar_solicitud_view,
)

app_name = 'web'

urlpatterns = [
    path('', index, name='index'),
    path('contacto/', contacto_view, name='contacto'),
    path('servicios/', servicios_view, name='servicios'),
    path('nosotros/', nosotros_view, name='nosotros'),
    path('registro/', registro_view, name='registro'),
    path('validar/', validar_cuenta_view, name='validar_cuenta'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('noticias/', noticias_view, name='noticias'),
    path('api/consultas/', consultas_api_view, name='consultas_api'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('dashboard/editar/<int:solicitud_id>/', editar_solicitud_view, name='editar_solicitud'),
    path('dashboard/eliminar/<int:solicitud_id>/', eliminar_solicitud_view, name='eliminar_solicitud'),
]
