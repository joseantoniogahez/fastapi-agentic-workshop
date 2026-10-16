# Arquitectura de SupportDesk

La aplicación es un monolito FastAPI pequeño. La creación y el listado de tickets recorren router, servicio y repositorio en memoria. No hay una capa de acceso a base de datos conectada.

```text
Cliente HTTP → FastAPI (main.py) → router → TicketService → repositorio en memoria
                                                         ↓
                                                  Ticket de dominio
```

- **Router** (`app/routers/tickets.py`): publica `POST` y `GET` bajo `/api/v1/tickets`, recibe los contratos HTTP y delega los casos de uso.
- **Servicio** (`app/services/tickets.py`): coordina la creación y el listado; al crear, construye el ticket mediante el modelo de dominio y pide al repositorio guardarlo.
- **Dominio** (`app/domain.py`): representa el ticket y establece `open` como estado inicial.
- **Repositorio** (`app/repositories/tickets.py`): guarda y lista tickets en memoria. Sus datos se pierden al reiniciar.
- **Base de datos**: no está conectada. Aunque SQLAlchemy figura entre las dependencias del proyecto, no hay configuración, sesión ni repositorio de base de datos en uso.

`app/main.py` crea la aplicación, conserva `GET /health` y registra el router de tickets. `app/schemas.py` define los contratos Pydantic; FastAPI valida entradas, serializa respuestas y genera OpenAPI. Esta separación cubre sólo el flujo actual: no implica persistencia, asignación de IDs ni implementación de las demás reglas del dominio. La capa de dominio tampoco implementa todavía el ciclo de vida completo descrito en `DOMAIN.md`.
