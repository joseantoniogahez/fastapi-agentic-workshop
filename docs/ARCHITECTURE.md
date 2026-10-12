# Arquitectura de SupportDesk

SupportDesk es una aplicación pequeña construida con FastAPI. `app/main.py` crea la aplicación, registra `GET /health`, incluye el router de tickets y traduce `TicketNotFound` a HTTP `404` y `TicketAlreadyClosed` a `409`. El lifespan de la app de producción crea las tablas al iniciar; `create_app(manage_database=False)` permite construir una app de pruebas sin ese acceso a SQLite. El router define las rutas HTTP y compone mediante `Depends` las dependencias de sesión, repositorio y servicio; el servicio aplica las reglas del ciclo de vida; el repositorio persiste y consulta tickets en SQLite mediante SQLAlchemy. Los esquemas Pydantic están en `app/schemas.py`.

```text
Cliente HTTP → FastAPI (main.py) → Router (/api/v1/tickets)
                                      ↓
                           Service → Repository → SQLite
                                      ↑
                             Pydantic (schemas.py)
```

`schemas.py` define `Priority`, `TicketStatus`, `TicketCreate`, `TicketUpdate`, `TicketResponse` y `TicketAnalysis`. FastAPI valida el JSON de entrada, serializa las respuestas y genera OpenAPI. Al crear, el servicio asigna `open`; el repositorio inserta el ticket, confirma la transacción y actualiza el objeto con el ID generado. El servicio también permite listar tickets activos, consultar, editar, cerrar y marcar como eliminado un ticket. El repositorio ordena el listado por ID y oculta los tickets eliminados. Para analizar un ticket, el servicio coordina con un servicio Gemini inyectado en el router. Si no encuentra un ticket, el servicio lanza `TicketNotFound`.

## Responsabilidades por capa

| Capa | Responsabilidad actual |
|---|---|
| Router | Define rutas, parámetros HTTP, códigos de estado y modelos de respuesta. |
| Service | Aplica reglas de creación, listado, edición, cierre y eliminación lógica. |
| Repository | Inserta, lista, consulta, actualiza y marca tickets como eliminados en SQLAlchemy. |
| AI service | Solicita a Gemini una categoría, prioridad sugerida y resumen; valida la respuesta como `TicketAnalysis`. |
| Database | Configura el motor SQLite, las sesiones y la creación inicial de tablas. |
| Schemas | Define enums y modelos Pydantic para entrada y salida. |

## Errores

Pydantic/FastAPI responde `422` cuando la entrada no cumple el esquema. `TicketNotFound` se define en `app/services.py` y el manejador de `app/main.py` responde `404` con `{"detail": "Ticket <id> not found"}`. Gemini no disponible o sin clave produce `503`; una respuesta inválida produce `502`. Los errores inesperados conservan el manejo predeterminado de FastAPI.

## Límites actuales

Están implementados `GET /health`, `POST` y `GET /api/v1/tickets`, `GET` y `PATCH /api/v1/tickets/{ticket_id}`, `POST /api/v1/tickets/{ticket_id}/close` y `/analyze`, y `DELETE /api/v1/tickets/{ticket_id}`. FastAPI inyecta la sesión por petición y reutiliza la misma instancia de servicio entre dependencias de esa petición. No hay autenticación, autorización ni observabilidad. Las pruebas están organizadas por servicio, API y repositorio. Las reglas del ciclo de vida están en [DOMAIN.md](DOMAIN.md).
