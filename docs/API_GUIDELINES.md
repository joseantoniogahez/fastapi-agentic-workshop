# Convenciones de la API

- Las rutas usan sustantivos plurales y minúsculas: `GET /health`, `POST /tickets` y `GET /tickets`.
- Los cuerpos usan JSON y nombres `snake_case`, por ejemplo `in_progress`.
- `POST /tickets` usa `201 Created` cuando es válido.
- Pydantic valida longitudes, enums y campos extra; las entradas inválidas producen `422`.
- Las respuestas deben declarar `response_model` para que el contrato aparezca en OpenAPI.
- `DELETE /tickets/{id}` implementa soft delete, nunca borrado físico, y debe rechazar tickets cuyo estado sea `closed`.
- Los tickets eliminados lógicamente deben quedar ocultos para listados, búsquedas y lecturas operativas; sólo podrán incluirse en endpoints o procesos explícitos de histórico y análisis de IA.
- Las operaciones de edición y reapertura deben rechazar tickets cerrados.
- Los cambios de nombres, enums, obligatoriedad o semántica de campos son cambios de contrato y deben documentarse.

Deuda conocida del checkpoint: `POST /tickets` declara `TicketResponse`, pero todavía no genera el `id` requerido.
