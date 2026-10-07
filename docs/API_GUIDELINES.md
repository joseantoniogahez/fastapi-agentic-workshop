# Convenciones de la API

- Las rutas usan sustantivos plurales y minúsculas: `GET /health` y `/api/v1/tickets` para la colección versionada.
- Los cuerpos usan JSON y nombres `snake_case`, por ejemplo `in_progress`.
- `POST /api/v1/tickets` usa `201 Created`; `DELETE /api/v1/tickets/{id}` usa `204 No Content`.
- Pydantic valida longitudes, enums y campos extra; las entradas inválidas producen `422`.
- Las respuestas deben declarar `response_model` para que el contrato aparezca en OpenAPI.
- `DELETE /tickets/{id}` implementa soft delete, nunca borrado físico, y debe rechazar tickets cuyo estado sea `closed`.
- Los tickets eliminados lógicamente deben quedar ocultos para listados, búsquedas y lecturas operativas; sólo podrán incluirse en endpoints o procesos explícitos de histórico y análisis de IA.
- `PATCH /api/v1/tickets/{id}` sólo acepta campos de `TicketUpdate`; las operaciones de edición y reapertura deben rechazar tickets cerrados. Los conflictos con invariantes de estado responden `409`.
- `GET /api/v1/tickets` admite filtros `status` y `priority`, además de `limit` (1–100) y `offset` (>= 0).
- Los cambios de nombres, enums, obligatoriedad o semántica de campos son cambios de contrato y deben documentarse.

El almacenamiento actual sigue siendo en memoria y se reinicia con el proceso; la ruta `/tickets` del checkpoint inicial se reemplazó por `/api/v1/tickets`.
