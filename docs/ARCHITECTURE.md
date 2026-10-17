# Arquitectura de SupportDesk

La aplicación es un monolito FastAPI pequeño. Las operaciones de tickets recorren router, servicio y repositorio SQLAlchemy.

```text
POST /api/v1/tickets → router → TicketService → TicketRepository → SQLite
GET /api/v1/tickets/{ticket_id} → router → TicketService → TicketRepository → SQLite
PATCH /api/v1/tickets/{ticket_id} → router → TicketService → TicketRepository → SQLite
POST /api/v1/tickets/{ticket_id}/close → router → TicketService → TicketRepository → SQLite
DELETE /api/v1/tickets/{ticket_id} → router → TicketService → TicketRepository → SQLite
                                  ↓                    ↑
                         Ticket SQLAlchemy ────────────┘
```

- **Router** (`app/routers/tickets.py`): recibe los contratos HTTP y obtiene una sesión por solicitud.
- **Servicio** (`app/services/tickets.py`): coordina creación, consultas, actualización, cierre y borrado; aplica el conflicto para tickets cerrados y lanza `TicketNotFound` para IDs ausentes.
- **Dominio** (`app/domain.py`): construye los datos del ticket con estado inicial `open` antes de persistirlos.
- **Modelo** (`app/models.py`): define `Ticket` con ID autogenerado, título, descripción, prioridad y estado.
- **Repositorio** (`app/repositories/tickets.py`): persiste creación, cambios, cierre y `deleted_at`; las lecturas omiten tickets eliminados.
- **Base de datos** (`app/database.py`): configura SQLite en `supportdesk.db`, una sesión SQLAlchemy y crea las tablas al iniciar la aplicación.
- **Contratos** (`app/schemas.py`): Pydantic valida los datos de entrada y `TicketResponse` serializa el modelo de base de datos.

La API expone `POST` y `GET /api/v1/tickets`, `GET` y `PATCH /api/v1/tickets/{ticket_id}`, `POST /api/v1/tickets/{ticket_id}/close` y `DELETE /api/v1/tickets/{ticket_id}`. El manejador global traduce `TicketNotFound` a `404` y `TicketConflict` a `409`; FastAPI conserva el `422` de validación. El borrado es lógico y responde `204`. No hay migraciones ni gestión específica de errores de base de datos. La ruta de SQLite es relativa al directorio desde el que se inicia la aplicación.
