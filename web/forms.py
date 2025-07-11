from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import MensajeContacto, Solicitud, UsuarioPermitido

class ContactoForm(forms.ModelForm):
    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'email', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Tu nombre'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Tu email'}),
            'mensaje': forms.Textarea(attrs={'placeholder': 'Tu mensaje'}),
        }

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['nombre', 'email', 'telefono', 'mensaje']  # <--- Agregalo acá
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Tu nombre'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Tu correo'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Tu teléfono'}),  # <---
            'mensaje': forms.Textarea(attrs={'placeholder': 'Escribí tu mensaje'}),
        }


class RegistroForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not UsuarioPermitido.objects.filter(email=email).exists():
            raise ValidationError("Acceso restringido. No está autorizado a utilizar este sistema.")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este email ya fue registrado.")
        return email

class CodigoValidacionForm(forms.Form):
    codigo = forms.CharField(max_length=10)

class LoginForm(forms.Form):
    email = forms.EmailField(label="Correo electrónico")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
