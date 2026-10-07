# Dominio de SupportDesk

## Ticket

Un ticket representa una solicitud de soporte. Tiene `title` (3–100 caracteres), `description` (hasta 2000), `priority` (`low`, `medium` o `high`, por defecto `medium`), `status` e `id`.

## Estados

| Estado | Significado |
|---|---|
| `open` | Ticket recién creado y pendiente de atención. |
| `in_progress` | Ticket que está siendo atendido. |
| `closed` | Ticket cuya atención terminó. |

Todo ticket nuevo comienza en `open`. Las siguientes invariantes gobiernan su ciclo de vida:

1. Un ticket cerrado no se puede editar ni volver a abrir.
2. `DELETE` sólo realiza soft delete; nunca borra físicamente.
3. Un ticket cerrado no se puede soft-delete.
4. Un ticket eliminado queda oculto para búsquedas y listados operativos. Sólo puede consultarse para operaciones históricas o análisis de la IA.
5. Los tickets cerrados se conservan como histórico y, en el futuro, servirán como fuente de sugerencias para la IA.

## Reglas

El contrato rechaza campos adicionales (`extra="forbid"`) y valores de prioridad o estado fuera de los enums. `PATCH` permite actualizar campos explícitos; un ticket cerrado no se puede editar, reabrir ni eliminar. El borrado es lógico y lo excluye de consultas operativas. Los tickets se almacenan en memoria y se pierden al reiniciar; no hay todavía persistencia ni aislamiento entre usuarios.
