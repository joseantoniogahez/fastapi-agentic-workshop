# Convenciones de la API

## Contrato implementado

- `GET /health` devuelve `{"status": "ok"}`.
- Los endpoints de tickets usan el prefijo `/api/v1/tickets` y cuerpos JSON con nombres `snake_case`.
- `POST /api/v1/tickets` crea un ticket y devuelve `201 Created` con `TicketResponse`: `id`, `title`, `description`, `priority` y `status`.
- En la creación, `title` debe tener entre 3 y 100 caracteres; `description` admite hasta 2000. `priority` puede ser `low`, `medium` o `high` y por defecto es `medium`. `status` no se acepta en el cuerpo: comienza como `open`.
- `GET /api/v1/tickets/{ticket_id}` devuelve `TicketResponse` con `200 OK`; si no existe o está eliminado, devuelve `404` y `{"detail": "Ticket <id> not found"}`.
- `PATCH /api/v1/tickets/{ticket_id}` permite actualizar `title`, `description` y `priority`; rechaza campos extra con `422`. Un ticket cerrado responde `409` y conserva sus datos.
- `POST /api/v1/tickets/{ticket_id}/close` cierra un ticket y devuelve `TicketResponse`; un ticket ya cerrado responde `409`.
- `DELETE /api/v1/tickets/{ticket_id}` realiza soft delete y devuelve `204` sin cuerpo. Los cerrados no se pueden eliminar (`409`); un ID inexistente devuelve `404`.
- `POST /api/v1/tickets/{ticket_id}/analyze` analiza un ticket existente y devuelve `TicketAnalysis` con `category`, `suggested_priority` (`low`, `medium` o `high`) y `summary` de hasta 500 caracteres. Un ID inexistente devuelve `404`.
- Pydantic rechaza campos adicionales, valores de enum desconocidos y longitudes fuera de los límites; FastAPI responde `422`.
- Los modelos de respuesta se declaran con `response_model` para exponer el contrato en OpenAPI.
- Los tickets se persisten en SQLite mediante SQLAlchemy. El ID lo genera la base de datos.

## Errores y futuras integraciones

- `TicketNotFound` devuelve `404`; `TicketAlreadyClosed` devuelve `409`.
- El análisis usa Gemini mediante `GEMINI_API_KEY`, leída del entorno al atender la petición. Si falta la clave o el proveedor no está disponible, devuelve `503`; una respuesta inválida devuelve `502`.

Todo cambio en rutas, nombres, enums, obligatoriedad o semántica de campos debe actualizar esta guía y los esquemas OpenAPI generados por la aplicación. No hay endpoint de listado.
