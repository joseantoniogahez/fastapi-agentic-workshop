# Arquitectura de SupportDesk

La aplicación es un monolito FastAPI pequeño. `app/main.py` crea la aplicación, registra `/health` e incluye el router de tickets. El router define el contrato HTTP; service y repository coordinan la creación, y SQLAlchemy persiste los tickets en SQLite. Los contratos HTTP están en `app/schemas.py`.

```text
Cliente HTTP → FastAPI (main.py) → Router (/api/v1/tickets)
                                      ↓
                           Service → Repository → SQLite
                                      ↑
                             Pydantic (schemas.py)
```

`schemas.py` define `Priority`, `TicketStatus`, `TicketCreate` y `TicketResponse`. FastAPI convierte JSON, valida, serializa y genera OpenAPI. `POST /api/v1/tickets` valida la entrada, el service asigna `open`, el repository inserta y confirma la transacción, y la base de datos devuelve el identificador generado.

## Responsabilidades por capa

Cada capa tiene una responsabilidad concreta:

| Capa | Responsabilidad | Ejemplo |
|---|---|---|
| Router | Manejar HTTP y definir contratos: body, path y status code. | Recibir `POST /api/v1/tickets` y responder con el modelo declarado. |
| Service | Aplicar reglas del negocio. | Rechazar la edición de un ticket cerrado. |
| Repository | Leer y guardar datos. | Buscar un ticket e insertar o actualizar sus datos. |
| Database | Crear y mantener la conexión y el esquema persistente. | Crear la tabla `tickets` en SQLite. |

La implementación actual cubre sólo creación de tickets: todavía no ofrece listados, lecturas por identificador, edición ni borrado. `get_session()` está disponible en `app/database.py`, pero el router abre la sesión directamente con `Session(engine)`; no usa esa función como dependencia FastAPI.

La autenticación, autorización, observabilidad y pruebas siguen pendientes. Si se agregan operaciones de edición o borrado, la capa de dominio deberá aplicar las invariantes descritas en `DOMAIN.md`.
