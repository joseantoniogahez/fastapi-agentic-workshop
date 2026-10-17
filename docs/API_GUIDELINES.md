# Convenciones de la API

- Las rutas usan sustantivos plurales y minúsculas: `GET /health` y los endpoints de tickets bajo `/api/v1/tickets`.
- Los cuerpos usan JSON y nombres `snake_case`, por ejemplo `in_progress`.
- `POST /api/v1/tickets` valida el cuerpo con Pydantic, crea el ticket con estado `open`, lo guarda en SQLite y responde `201 Created` con `TicketResponse` e ID autogenerado.
- Pydantic valida longitudes, enums y campos extra; las entradas inválidas producen `422`.
- Las respuestas deben declarar `response_model` para que el contrato aparezca en OpenAPI.
- `GET /api/v1/tickets` lista los tickets almacenados en SQLite.
- `GET /api/v1/tickets/{ticket_id}` devuelve el ticket almacenado con ese ID usando `TicketResponse`; si no existe, responde `404` con `{"detail":{"code":"ticket_not_found","ticket_id":<id>}}`.
- `PATCH /api/v1/tickets/{ticket_id}` acepta `TicketUpdate` con uno o más de `title`, `description` y `priority`, y responde `TicketResponse`; un ticket cerrado produce `409`.
- `POST /api/v1/tickets/{ticket_id}/close` cierra el ticket y responde `TicketResponse`.
- `DELETE /api/v1/tickets/{ticket_id}` marca el ticket como eliminado, lo oculta de consultas/listados y responde `204` sin cuerpo. No se pueden eliminar tickets cerrados (`409`).
- Los conflictos usan `{"detail":{"code":"ticket_conflict","ticket_id":<id>,"operation":"<operation>"}}`.
- Los errores de validación de FastAPI conservan su respuesta `422`.
- Una ruta o ID inexistente, incluido un ticket eliminado, responde `404`.
- Los cambios de nombres, enums, obligatoriedad o semántica de campos son cambios de contrato y deben documentarse.
