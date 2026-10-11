# Dominio de SupportDesk

## Ticket

Un ticket representa una solicitud de soporte. Tiene un `id` entero generado por la base de datos, `title` (3–100 caracteres), `description` (hasta 2000), `priority` (`low`, `medium` o `high`, por defecto `medium`) y `status`.

## Estados

| Estado | Significado |
|---|---|
| `open` | Ticket recién creado y pendiente de atención. |
| `in_progress` | Ticket que está siendo atendido. |
| `closed` | Ticket cuya atención terminó. |

Todo ticket nuevo comienza en `open`. El contrato de creación no permite enviar `status`; lo asigna el servicio.

## Persistencia y alcance actual

Los tickets se guardan en la tabla `tickets` de SQLite mediante SQLAlchemy. La base de datos se configura en `app/database.py` como `supportdesk.db` en el directorio de ejecución. Actualmente se puede crear un ticket y consultarlo por ID. No hay listados, edición, cierre, borrado, autenticación, aislamiento entre usuarios.

## Reglas para futuras operaciones

Estas reglas describen el comportamiento esperado cuando se implementen las operaciones correspondientes; no implican que esos endpoints existan hoy:

1. Un ticket cerrado no se puede editar ni volver a abrir.
2. `DELETE` realiza soft delete, nunca borrado físico, y no permite eliminar tickets cerrados.
3. Los tickets eliminados quedan ocultos para búsquedas y lecturas operativas. Sólo se incluyen en operaciones explícitas de histórico o análisis.
4. Los tickets cerrados se conservan como histórico y podrían servir como fuente de sugerencias para una futura función de IA.
