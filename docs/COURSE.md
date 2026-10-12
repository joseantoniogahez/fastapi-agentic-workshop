# Recorrido del curso

El historial funciona como una secuencia de checkpoints:

| Checkpoint | Rama | Qué enseña |
|---|---|---|
| 0. Bootstrap | `step/00-bootstrap` | Crear FastAPI y publicar `GET /health`. |
| 1. API ingenua | `step/01-api-ingenua` | Crear y listar tickets en memoria. |
| 2. Contratos | `step/02-contratos` | Modelos, enums, valores por defecto, límites y campos extra con Pydantic. |
| 3. Documentación | `step/03-documentation` | Documentar dominio, arquitectura, convenciones de API y recorrido del curso. |

Para estudiar cada etapa, cambia a la rama correspondiente y revisa sus diferencias:

```bash
git switch <rama>
git diff <rama-anterior> <rama>
```

Ejecuta la aplicación y prueba cada endpoint desde `/docs` o con `curl`. El checkpoint de contratos y los siguientes dejan como ejercicios la asignación de IDs, persistencia, actualización, cierre, protección de tickets cerrados, soft delete, histórico para sugerencias de IA y pruebas automatizadas.
