# Arquitectura de SupportDesk

SupportDesk es una aplicación pequeña construida con FastAPI. `app/main.py` crea la aplicación, registra `GET /health`, incluye el router de tickets y traduce `TicketNotFound` a HTTP `404`. El router define las rutas HTTP; el servicio aplica la lógica de creación y consulta; el repositorio accede a SQLite mediante SQLAlchemy. Los esquemas Pydantic están en `app/schemas.py`.

```text
Cliente HTTP → FastAPI (main.py) → Router (/api/v1/tickets)
                                      ↓
                           Service → Repository → SQLite
                                      ↑
                             Pydantic (schemas.py)
```

`schemas.py` define `Priority`, `TicketStatus`, `TicketCreate` y `TicketResponse`. FastAPI valida el JSON de entrada, serializa las respuestas y genera OpenAPI. Al crear, el servicio asigna `open`; el repositorio inserta el ticket, confirma la transacción y actualiza el objeto con el ID generado. Al consultar por ID, el servicio lanza `TicketNotFound` cuando el repositorio no encuentra el ticket.

## Responsabilidades por capa

| Capa | Responsabilidad actual |
|---|---|
| Router | Define rutas, parámetros HTTP, códigos de estado y modelos de respuesta. |
| Service | Coordina las operaciones y asigna el estado inicial del ticket. |
| Repository | Inserta y busca tickets en la sesión SQLAlchemy. |
| Database | Configura el motor SQLite, las sesiones y la creación inicial de tablas. |
| Schemas | Define enums y modelos Pydantic para entrada y salida. |

## Errores

Pydantic/FastAPI responde `422` cuando la entrada no cumple el esquema. `TicketNotFound` se define en `app/services.py` y el manejador de `app/main.py` responde `404` con `{"detail": "Ticket <id> not found"}`. Los errores inesperados conservan el manejo predeterminado de FastAPI.

## Límites actuales

Están implementados `GET /health`, `POST /api/v1/tickets` y `GET /api/v1/tickets/{ticket_id}`. Ambas rutas de tickets abren y cierran la sesión directamente; aunque `get_session()` existe en `app/database.py`, actualmente no se inyecta en las rutas. No hay listados, edición, borrado, integración con IA, autenticación, autorización, observabilidad ni pruebas automatizadas. Las reglas previstas para el ciclo de vida están en [DOMAIN.md](DOMAIN.md).
