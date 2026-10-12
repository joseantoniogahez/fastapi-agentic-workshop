# Autenticación, permisos y entradas

## Estado

La API no autentica usuarios ni aplica autorización por propietario o rol. FastAPI/Pydantic valida los esquemas declarados y rechaza campos extra según los modelos actuales; esto no sustituye controles de acceso ni validación contextual.

## Guía para cambios

- Antes de implementar autenticación, define identidad, emisor de credenciales, rutas protegidas y flujo de pruebas. Antes de autorización, define quién puede leer, editar, cerrar, analizar y eliminar cada ticket.
- Aplica autorización en el límite de servicio o en una dependencia compartida que proteja todas las rutas pertinentes; evita proteger sólo la interfaz o una ruta.
- Mantén los modelos de entrada explícitos, límites de tamaño razonables y campos extra rechazados. Valida además reglas contextuales en la capa de dominio.
- Trata texto de tickets como entrada no confiable, especialmente al construir prompts para Gemini. No registres el contenido completo ni incluyas secretos en el prompt.
- Añade pruebas de denegación y acceso permitido junto con las pruebas HTTP y de servicio correspondientes.

No elijas proveedor de identidad, formato de token ni política multiusuario sin una decisión del proyecto.
