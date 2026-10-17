# Dominio de SupportDesk

## Ticket

Un ticket representa una solicitud de soporte. Tiene `title` (3–100 caracteres), `description` (hasta 2000), `priority` (`low`, `medium` o `high`, por defecto `medium`), `status` e `id`.

## Estados y ciclo de vida

| Estado | Significado |
|---|---|
| `open` | Ticket recién creado y pendiente de atención. |
| `in_progress` | Ticket que está siendo atendido. |
| `closed` | Ticket cuya atención terminó. |

Todo ticket nuevo comienza en `open`. Se puede actualizar parcialmente el título, la descripción o la prioridad, y se puede cerrar explícitamente. Un ticket cerrado no se puede editar ni eliminar. El borrado es lógico: conserva la fila con `deleted_at` y oculta el ticket de consultas y listados operativos.

## Reglas

Pydantic rechaza campos adicionales y valores de prioridad fuera del enum. `PATCH` requiere al menos un campo permitido. Los IDs inexistentes o eliminados producen `404`; editar o eliminar un ticket cerrado produce `409`. `DELETE` responde `204` sin cuerpo. Los tickets se persisten en SQLite. No hay migraciones ni aislamiento entre usuarios.
