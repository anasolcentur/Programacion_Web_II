# Grupo Empresarial Norte

Este es un sitio web desarrollado con Django como parte del proyecto académico de la materia Programacion Web II, que simula un sitio institucional con funcionalidades avanzadas, como autenticación restringida, sistema de formularios, API REST y despliegue profesional.

## 🌐 URL del sitio en producción (Render)

https://grupo-empresarial-norte.onrender.com

## 🧩 Funcionalidades implementadas

- Sitio web con múltiples secciones (Inicio, Nosotros, Servicios, Contacto)
- Sistema de autenticación con:
  - Registro restringido a usuarios autorizados
  - Validación de cuenta vía email con código
  - Inicio y cierre de sesión
- Formulario de contacto con validación en frontend y backend
- Clasificación automática de mensajes por tipo de consulta
- Envío de email de confirmación con la categoría asignada
- Panel de administración personalizado (dashboard)
  - Resumen estadístico por tipo de consulta
  - Tabla editable de solicitudes recibidas
- API REST propia para exponer solicitudes:
  - Ruta: `/api/consultas/`
- Consumo de API externa sobre noticias legales:
  - Sección “Noticias del mundo jurídico”
  - Fuente: [mediastack.com](http://api.mediastack.com/v1/news)
