# Timeouts, logs y diagnóstico

## Estado

La aplicación ofrece `GET /health` con `{"status":"ok"}`. No se configura logging operativo ni timeouts explícitos en el cliente Gemini. No se documenta una comprobación de salud de la base de datos ni métricas.

## Guía para cambios

- Asigna timeouts explícitos a llamadas de red y define qué error observable devuelve el servicio cuando vencen. Mantén separado el timeout de conexión del de respuesta si el cliente lo permite.
- Añade logs estructurados con nivel, evento y contexto útil (por ejemplo, identificador de petición); excluye claves, tokens y contenido sensible de tickets. Evita capturar y ocultar excepciones indiscriminadamente.
- Conserva respuestas HTTP estables y mensajes públicos sin detalles internos; registra detalles técnicos con redacción segura.
- Aclara qué verifica cada endpoint de salud. No hagas que el readiness dependa de un servicio opcional salvo que ésa sea una decisión operativa explícita.
- Prueba timeouts y errores de proveedor usando el adaptador falso; reserva pruebas externas para verificar compatibilidad real del adaptador.

No declares observabilidad ni diagnóstico de producción existentes basándote sólo en el endpoint `/health`.
