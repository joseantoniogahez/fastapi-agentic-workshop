# Dominio de SupportDesk

## Ticket

Un ticket representa una solicitud de soporte. Tiene un `id` entero generado por la base de datos, `title` (3–100 caracteres), `description` (hasta 2000), `priority` (`low`, `medium` o `high`, por defecto `medium`) y `status`.

## Estados

| Estado | Significado |
|---|---|
| `open` | Ticket recién creado y pendiente de atención. |
| `in_progress` | Ticket que está siendo atendido. |
| `closed` | Ticket cuya atención terminó. |

Todo ticket nuevo comienza en `open`. El contrato de creación no permite enviar `status`; lo asigna el servicio. La ruta `POST /api/v1/tickets/{id}/close` cierra un ticket.

## Persistencia y reglas

Los tickets se guardan en SQLite mediante SQLAlchemy. Se pueden crear, consultar, editar, cerrar y eliminar lógicamente; no hay endpoint de listado, autenticación ni aislamiento entre usuarios. El repositorio oculta los tickets eliminados en las consultas operativas.

Un ticket existente puede analizarse con IA para obtener una categoría, una prioridad sugerida y un resumen. El análisis no modifica el ticket. La integración usa Gemini y requiere `GEMINI_API_KEY`; los fallos del proveedor o una respuesta inválida se exponen como errores de API.

1. Un ticket cerrado no se puede editar ni reabrir.
2. `DELETE` realiza soft delete, nunca borrado físico, y no permite eliminar tickets cerrados.
3. Los tickets eliminados quedan ocultos en lecturas operativas; se conservan en la base de datos para histórico.
4. Los tickets cerrados se conservan como histórico y podrían servir como fuente para una futura función de IA.
