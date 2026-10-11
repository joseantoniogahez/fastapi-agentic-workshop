# Arquitectura de SupportDesk

SupportDesk es una aplicación pequeña construida con FastAPI. `app/main.py` crea la aplicación, registra `GET /health`, incluye el router de tickets y traduce `TicketNotFound` a HTTP `404` y `TicketAlreadyClosed` a `409`. El router define las rutas HTTP; el servicio aplica las reglas del ciclo de vida; el repositorio persiste y consulta tickets en SQLite mediante SQLAlchemy. Los esquemas Pydantic están en `app/schemas.py`.

```text
Cliente HTTP → FastAPI (main.py) → Router (/api/v1/tickets)
                                      ↓
                           Service → Repository → SQLite
                                      ↑
                             Pydantic (schemas.py)
```

`schemas.py` define `Priority`, `TicketStatus`, `TicketCreate`, `TicketUpdate` y `TicketResponse`. FastAPI valida el JSON de entrada, serializa las respuestas y genera OpenAPI. Al crear, el servicio asigna `open`; el repositorio inserta el ticket, confirma la transacción y actualiza el objeto con el ID generado. El servicio también permite consultar, editar, cerrar y marcar como eliminado un ticket. El repositorio oculta los tickets eliminados en las consultas. Si no encuentra un ticket, el servicio lanza `TicketNotFound`.

## Responsabilidades por capa

| Capa | Responsabilidad actual |
|---|---|
| Router | Define rutas, parámetros HTTP, códigos de estado y modelos de respuesta. |
| Service | Aplica reglas de creación, edición, cierre y eliminación lógica. |
| Repository | Inserta, consulta, actualiza y marca tickets como eliminados en SQLAlchemy. |
| Database | Configura el motor SQLite, las sesiones y la creación inicial de tablas. |
| Schemas | Define enums y modelos Pydantic para entrada y salida. |

## Errores

Pydantic/FastAPI responde `422` cuando la entrada no cumple el esquema. `TicketNotFound` se define en `app/services.py` y el manejador de `app/main.py` responde `404` con `{"detail": "Ticket <id> not found"}`. Los errores inesperados conservan el manejo predeterminado de FastAPI.

## Límites actuales

Están implementados `GET /health`, `POST /api/v1/tickets`, `GET` y `PATCH /api/v1/tickets/{ticket_id}`, `POST /api/v1/tickets/{ticket_id}/close` y `DELETE /api/v1/tickets/{ticket_id}`. Las rutas abren y cierran la sesión directamente; aunque `get_session()` existe en `app/database.py`, actualmente no se inyecta en ellas. No hay endpoint de listado, integración con IA, autenticación, autorización ni observabilidad. Las pruebas están organizadas por servicio, API y repositorio. Las reglas del ciclo de vida están en [DOMAIN.md](DOMAIN.md).
