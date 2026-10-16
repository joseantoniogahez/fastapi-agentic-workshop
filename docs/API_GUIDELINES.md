# Convenciones de la API

- Las rutas usan sustantivos plurales y minúsculas: `GET /health` y los endpoints de tickets bajo `/api/v1/tickets`.
- Los cuerpos usan JSON y nombres `snake_case`, por ejemplo `in_progress`.
- `POST /api/v1/tickets` valida el cuerpo con Pydantic, crea el ticket con estado `open`, lo guarda en SQLite y responde `201 Created` con `TicketResponse` e ID autogenerado.
- Pydantic valida longitudes, enums y campos extra; las entradas inválidas producen `422`.
- Las respuestas deben declarar `response_model` para que el contrato aparezca en OpenAPI.
- `GET /api/v1/tickets` lista los tickets almacenados en SQLite.
- `DELETE /api/v1/tickets/{id}` y las operaciones de edición/cierre no están implementadas.
- Los cambios de nombres, enums, obligatoriedad o semántica de campos son cambios de contrato y deben documentarse.
