# Convenciones de la API

## Contrato implementado

- `GET /health` devuelve `{"status": "ok"}`.
- Los endpoints de tickets usan el prefijo `/api/v1/tickets` y cuerpos JSON con nombres `snake_case`.
- `POST /api/v1/tickets` crea un ticket y devuelve `201 Created` con `TicketResponse`: `id`, `title`, `description`, `priority` y `status`.
- En la creación, `title` debe tener entre 3 y 100 caracteres; `description` admite hasta 2000. `priority` puede ser `low`, `medium` o `high` y por defecto es `medium`. `status` no se acepta en el cuerpo: comienza como `open`.
- `GET /api/v1/tickets/{ticket_id}` devuelve `TicketResponse` con `200 OK`; si no existe el ID, devuelve `404` y `{"detail": "Ticket <id> not found"}`.
- Pydantic rechaza campos adicionales, valores de enum desconocidos y longitudes fuera de los límites; FastAPI responde `422`.
- Los modelos de respuesta se declaran con `response_model` para exponer el contrato en OpenAPI.
- Los tickets se persisten en SQLite mediante SQLAlchemy. El ID lo genera la base de datos.

## Reglas para cambios futuros

Las reglas siguientes son requisitos de dominio, no endpoints actualmente disponibles:

- Si se agrega `DELETE`, debe ser soft delete y rechazar tickets cerrados. Los tickets eliminados deben quedar ocultos en operaciones ordinarias; sólo se incluyen en operaciones explícitas de histórico o análisis.
- Las operaciones futuras de edición no deben permitir modificar ni reabrir tickets cerrados.
- Si se agrega integración con IA, una dependencia no disponible puede responder `503` y una respuesta inválida `502`; esos errores no deben confundirse con errores de dominio.
- Todo cambio en rutas, nombres, enums, obligatoriedad o semántica de campos debe actualizar esta guía y los esquemas OpenAPI generados por la aplicación.

El alcance implementado es `GET /health`, `POST /api/v1/tickets` y `GET /api/v1/tickets/{ticket_id}`. No existen endpoints de listado, edición, cierre ni borrado.
