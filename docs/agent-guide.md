# Guía de contexto para agentes

Empieza aquí. Abre sólo la referencia que corresponda al cambio solicitado; no cargues toda la documentación de producción para una tarea que no la necesita.

## Ruta de lectura

| Si la tarea trata de… | Lee… |
|---|---|
| Comportamiento, estado o reglas de tickets | [DOMAIN.md](DOMAIN.md) |
| Rutas, validación o respuestas HTTP | [API_GUIDELINES.md](API_GUIDELINES.md) |
| Capas, dependencias o persistencia actual | [ARCHITECTURE.md](ARCHITECTURE.md) |
| Variables de entorno o credenciales | [production/configuration-and-secrets.md](production/configuration-and-secrets.md) |
| Autenticación, permisos o entrada no confiable | [production/security-and-input.md](production/security-and-input.md) |
| Esquema, migraciones, backup o recuperación | [production/data-operations.md](production/data-operations.md) |
| Timeouts, logs o diagnóstico | [production/operations.md](production/operations.md) |
| CI, despliegue o rollback | [production/release.md](production/release.md) |

## Estado del proyecto

SupportDesk es un taller, no un despliegue de producción configurado. La aplicación usa SQLite en `supportdesk.db`, crea tablas con `Base.metadata.create_all` al arrancar, carga `.env` y lee `GEMINI_API_KEY` cuando se solicita análisis. Actualmente no hay autenticación, autorización, migraciones, política de backup, logs operativos, CI ni configuración de despliegue/rollback declaradas en el repositorio.

Trata las referencias de producción como criterios para planear y revisar trabajo. No presentes recomendaciones como capacidades ya implementadas. Antes de elegir proveedor, formato de secretos, política de retención, RPO/RTO, identidad de usuarios o estrategia de despliegue, busca una decisión del proyecto; si falta, documenta la pregunta y limita el cambio a lo que puede resolverse sin inventarla.

Para cambios de código, sigue además la lección vigente, `docs/API_GUIDELINES.md` si cambia la API, las pruebas separadas por capa indicadas en `AGENTS.md`, y la skill del taller. Mantén documentación mínima: actualiza sólo la referencia cuyo comportamiento o decisión haya cambiado.
