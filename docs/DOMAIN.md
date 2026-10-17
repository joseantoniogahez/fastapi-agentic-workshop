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

Los estados describen el ciclo de vida previsto; no hay operaciones implementadas para editar, cerrar ni eliminar tickets.

## Reglas

El contrato rechaza campos adicionales (`extra="forbid"`) y valores de prioridad o estado fuera de los enums. Los tickets se persisten en SQLite. La API permite crear, listar y consultar por ID; una consulta inexistente produce `TicketNotFound`, que se representa como HTTP `404`. No hay migraciones, actualización, cierre, borrado ni aislamiento entre usuarios.
