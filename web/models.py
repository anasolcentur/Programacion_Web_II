from django.db import models

class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.email}"

class Solicitud(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20, null=True, blank=True)
    mensaje = models.TextField()
    categoria = models.CharField(max_length=100, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.nombre} - {self.email}"

class UsuarioPermitido(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    codigo_validacion = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nombre} - {self.email}"  # Corregido
