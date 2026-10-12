# Convenciones de la API

- El health check está en `GET /health`. Las rutas de tickets usan el prefijo de versión `/api/v1/tickets`; la creación actual está disponible en `POST /api/v1/tickets`.
- Los cuerpos usan JSON y nombres `snake_case`, por ejemplo `in_progress`.
- `POST /api/v1/tickets` usa `201 Created` cuando es válido y devuelve `TicketResponse`, con `id` entero generado por la base de datos, `title`, `description`, `priority` y `status`.
- Pydantic valida longitudes, enums y campos extra; las entradas inválidas producen `422`.
- Las respuestas deben declarar `response_model` para que el contrato aparezca en OpenAPI.
- `DELETE /tickets/{id}` implementa soft delete, nunca borrado físico, y debe rechazar tickets cuyo estado sea `closed`.
- Los tickets eliminados lógicamente deben quedar ocultos para listados, búsquedas y lecturas operativas; sólo podrán incluirse en endpoints o procesos explícitos de histórico y análisis de IA.
- Al crear, `status` no se recibe en el body: el service asigna `open`. `priority` es opcional y por defecto `medium`.
- La creación persiste el ticket en SQLite mediante SQLAlchemy. El modelo de base de datos limita `title` a 100, `description` a 2000 y almacena `priority` y `status` como cadenas de hasta 20 caracteres; los enums y longitudes del contrato HTTP se validan en Pydantic.
- Las operaciones de edición y reapertura deben rechazar tickets cerrados.
- Los cambios de nombres, enums, obligatoriedad o semántica de campos son cambios de contrato y deben documentarse.

Alcance actual: sólo está implementado `POST /api/v1/tickets` además de `GET /health`. No hay actualmente endpoints de listado, lectura, edición o borrado de tickets; las reglas para esas operaciones documentadas aquí son requisitos de dominio para cuando se implementen.
