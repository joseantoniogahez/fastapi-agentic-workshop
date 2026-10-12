# Configuración y secretos

## Lo que existe

`app/main.py` carga `.env` con `python-dotenv`. `app/router.py` lee `GEMINI_API_KEY` al atender `/api/v1/tickets/{ticket_id}/analyze`. Si falta, el endpoint responde `503`. `.env` está excluido de Git y `.env.example` contiene un valor de muestra.

## Guía para cambios

- Mantén secretos fuera del código, de los logs, de ejemplos reales y del control de versiones. Usa valores ficticios en `.env.example`.
- Para desarrollo local, conserva `.env` ignorado por Git. Para producción, el mecanismo de inyección depende del entorno de ejecución y aún no está elegido; no agregues un gestor de secretos específico por suposición.
- Valida configuración requerida al iniciar cuando una variable sea necesaria para arrancar la aplicación. Si una integración opcional puede estar deshabilitada, define y documenta claramente el comportamiento sin credencial.
- Agrupa configuración tipada en un punto único sólo cuando el cambio lo requiera; documenta nombre, propósito, obligatoriedad y comportamiento por defecto.
- No muestres valores de credenciales en errores ni diagnóstico.

## Revisión

Confirma que `.env` sigue ignorado, que la plantilla no contiene credenciales y que el comportamiento ante variable ausente coincide con el contrato documentado. No supongas rotación automática ni almacenamiento seguro en producción: no están configurados aquí.
