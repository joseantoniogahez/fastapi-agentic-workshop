# Arquitectura de SupportDesk

La aplicación es un monolito FastAPI pequeño. La creación, el listado y la consulta de tickets recorren router, servicio y repositorio SQLAlchemy.

```text
POST /api/v1/tickets → router → TicketService → TicketRepository → SQLite
GET /api/v1/tickets/{ticket_id} → router → TicketService → TicketRepository → SQLite
                                  ↓                    ↑
                         Ticket SQLAlchemy ────────────┘
```

- **Router** (`app/routers/tickets.py`): recibe los contratos HTTP y obtiene una sesión por solicitud.
- **Servicio** (`app/services/tickets.py`): delega creación y consultas; lanza `TicketNotFound` cuando no existe el ID solicitado.
- **Dominio** (`app/domain.py`): construye los datos del ticket con estado inicial `open` antes de persistirlos.
- **Modelo** (`app/models.py`): define `Ticket` con ID autogenerado, título, descripción, prioridad y estado.
- **Repositorio** (`app/repositories/tickets.py`): crea el ticket con estado `open`, lo inserta, confirma la transacción y recarga el ID; también lista y busca por ID.
- **Base de datos** (`app/database.py`): configura SQLite en `supportdesk.db`, una sesión SQLAlchemy y crea las tablas al iniciar la aplicación.
- **Contratos** (`app/schemas.py`): Pydantic valida los datos de entrada y `TicketResponse` serializa el modelo de base de datos.

`GET /api/v1/tickets` consulta los registros guardados en SQLite. `GET /api/v1/tickets/{ticket_id}` responde con `TicketResponse` o, si no existe, el manejador global convierte `TicketNotFound` en HTTP `404` con `detail.code` igual a `ticket_not_found` y `detail.ticket_id`. FastAPI conserva sus respuestas `422` de validación. No hay migraciones, edición, cierre, borrado ni gestión de errores de base de datos específica. La ruta de SQLite es relativa al directorio desde el que se inicia la aplicación.
