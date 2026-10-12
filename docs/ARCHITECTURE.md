# Arquitectura de SupportDesk

La aplicación es un monolito FastAPI pequeño. Las rutas, la lógica de creación y el almacenamiento temporal están en `app/main.py`; los contratos están en `app/schemas.py`.

```text
Cliente HTTP → FastAPI (main.py) → lista en memoria
                         ↓
                  Pydantic (schemas.py)
```

`main.py` crea la aplicación y registra endpoints. `schemas.py` define `Priority`, `TicketStatus`, `TicketCreate` y `TicketResponse`. FastAPI convierte JSON, valida, serializa y genera OpenAPI. La lista global simplifica el aprendizaje del flujo request → validación → lógica → respuesta, pero no es almacenamiento de producción.

La evolución esperada es extraer servicio y repositorio, generar identificadores, añadir persistencia, autenticación, autorización, observabilidad y pruebas. La capa de dominio deberá proteger el cierre irreversible y aplicar las invariantes descritas en `DOMAIN.md`: un ticket cerrado no puede editarse, reabrirse ni recibir soft delete. `DELETE` conservará los demás tickets, los excluirá de las consultas operativas y los dejará disponibles únicamente para histórico o análisis de la IA.
