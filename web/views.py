from django.shortcuts import render, redirect
from .forms import ContactoForm, SolicitudForm, RegistroForm, LoginForm
from .models import Solicitud, UsuarioPermitido
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SolicitudSerializer


def index(request):
    mensaje_enviado = False
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            mensaje_enviado = True
            form = ContactoForm()
    else:
        form = ContactoForm()
    return render(request, 'web/index.html', {'form': form, 'mensaje_enviado': mensaje_enviado})


def servicios_view(request):
    return render(request, 'web/servicios.html')


def nosotros_view(request):
    return render(request, 'web/nosotros.html')


def contacto_view(request):
    mensaje_enviado = False
    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            mensaje = solicitud.mensaje.lower()

            if any(p in mensaje for p in ['precio', 'costo', 'tarifa', 'compra']):
                solicitud.categoria = 'Consulta Comercial'
            elif any(p in mensaje for p in ['soporte', 'error', 'problema', 'ayuda']):
                solicitud.categoria = 'Consulta Técnica'
            elif any(p in mensaje for p in ['trabajo', 'cv', 'empleo', 'linkedin']):
                solicitud.categoria = 'Consulta de RRHH'
            else:
                solicitud.categoria = 'Consulta General'

            solicitud.save()

            # Envío de confirmación por correo
            asunto = f"Formulario recibido: {solicitud.categoria}"
            cuerpo = f"""
Hola {solicitud.nombre},

Recibimos tu consulta con la siguiente información:

Nombre: {solicitud.nombre}
Email: {solicitud.email}
Teléfono: {solicitud.telefono}
Mensaje: {solicitud.mensaje}
Categoría asignada: {solicitud.categoria}

Gracias por comunicarte con nosotros.

Saludos cordiales,
Grupo Empresarial Norte
"""
            try:
                send_mail(
                    asunto,
                    cuerpo,
                    settings.DEFAULT_FROM_EMAIL,
                    [solicitud.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Error enviando correo: {e}")

            mensaje_enviado = True
            return redirect('contacto')  # Podrías usar una redirección con ?enviado=1 si querés persistencia
    else:
        form = SolicitudForm()

    return render(request, 'web/contacto.html', {
        'form': form,
        'mensaje_enviado': mensaje_enviado
    })


def registro_view(request):
    mensaje = ''
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            nombre = form.cleaned_data['nombre']
            password = form.cleaned_data['password']

            try:
                permitido = UsuarioPermitido.objects.get(email=email)
            except UsuarioPermitido.DoesNotExist:
                messages.error(request, "Acceso restringido. No está autorizado a utilizar este sistema.")
                return redirect('registro')

            request.session['registro_datos'] = {
                'nombre': nombre,
                'email': email,
                'password': password,
                'codigo': permitido.codigo_validacion
            }

            send_mail(
                'Validación de cuenta',
                f'Tu código de validación es: {permitido.codigo_validacion}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )

            mensaje = 'Le llegará un correo para validar su cuenta'
            return redirect('validar_cuenta')
    else:
        form = RegistroForm()
    return render(request, 'web/registro.html', {'form': form, 'mensaje': mensaje})


def validar_cuenta_view(request):
    if request.method == 'POST':
        codigo_ingresado = request.POST.get('codigo')
        datos = request.session.get('registro_datos')
        if datos and datos['codigo'] == codigo_ingresado:
            if not User.objects.filter(username=datos['email']).exists():
                User.objects.create_user(
                    username=datos['email'],
                    email=datos['email'],
                    password=datos['password'],
                    first_name=datos['nombre']
                )
                messages.success(request, 'Cuenta validada. Ya podés iniciar sesión.')
                return redirect('login')
            else:
                messages.info(request, 'Ya habías validado esta cuenta.')
                return redirect('login')
        else:
            messages.error(request, 'Código inválido.')
    return render(request, 'web/validar.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "Usuario no registrado.")
                return redirect('login')

            user_auth = authenticate(username=user.username, password=password)
            if user_auth:
                login(request, user_auth)
                return redirect('index')
            else:
                messages.error(request, "Credenciales incorrectas.")
    else:
        form = LoginForm()
    return render(request, 'web/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index')


def noticias_view(request):
    api_key = 'f189b42e62d7527430a9efe0e98192c8'
    url = f"http://api.mediastack.com/v1/news?access_key={api_key}&languages=es&keywords=ley%2Cjusticia%2Cjurídico"

    response = requests.get(url)
    noticias = []

    if response.status_code == 200:
        data = response.json()
        noticias = data.get('data', [])
    else:
        print("Error al acceder a la API:", response.status_code)

    return render(request, 'web/noticias.html', {'noticias': noticias})


@api_view(['GET'])
def consultas_api_view(request):
    consultas = Solicitud.objects.all()
    serializer = SolicitudSerializer(consultas, many=True)
    return Response(serializer.data)


@login_required
def dashboard_view(request):
    total = Solicitud.objects.count()
    por_categoria = Solicitud.objects.values('categoria').annotate(cantidad=Count('id'))
    solicitudes = Solicitud.objects.all().order_by('-fecha')

    return render(request, 'web/dashboard.html', {
        'total': total,
        'por_categoria': por_categoria,
        'solicitudes': solicitudes,
    })
