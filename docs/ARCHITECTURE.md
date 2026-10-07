# Arquitectura de SupportDesk

La aplicación es un monolito FastAPI pequeño. `app/main.py` expone rutas versionadas, `app/services.py` aplica reglas de negocio, `app/repositories.py` adapta el almacenamiento temporal y `app/schemas.py` declara los contratos.

```text
Cliente HTTP → FastAPI (main.py) → servicio → repositorio en memoria
                    ↓              ↓
              Pydantic (schemas.py)
```

`main.py` crea la aplicación y registra endpoints. `schemas.py` define enums y contratos de creación, actualización y respuesta. FastAPI valida, serializa y genera OpenAPI. El adaptador en memoria simplifica el aprendizaje del flujo, pero no es almacenamiento persistente ni seguro para varios procesos.

La evolución esperada es extraer servicio y repositorio, generar identificadores, añadir persistencia, autenticación, autorización, observabilidad y pruebas. La capa de dominio deberá proteger el cierre irreversible y aplicar las invariantes descritas en `DOMAIN.md`: un ticket cerrado no puede editarse, reabrirse ni recibir soft delete. `DELETE` conservará los demás tickets, los excluirá de las consultas operativas y los dejará disponibles únicamente para histórico o análisis de la IA.
