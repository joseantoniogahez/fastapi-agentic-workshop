# Recorrido del curso

El historial funciona como una secuencia de checkpoints:

| Checkpoint | Rama | Qué enseña |
|---|---|---|
| 0. Bootstrap | `step/00-bootstrap` | Crear FastAPI y publicar `GET /health`. |
| 1. API ingenua | `step/01-api-ingenua` | Crear y listar tickets en memoria. |
| 2. Contratos | `step/02-contratos` | Modelos, enums, valores por defecto, límites y campos extra con Pydantic. |
| 3. Documentación | `step/03-documentation` | Documentar dominio, arquitectura, convenciones de API y recorrido del curso. |
| 4. Agentes y skills | `step/04-agents-and-skills` | Definir instrucciones persistentes con `AGENTS.md` y crear una skill para el workflow de FastAPI. |

Para estudiar cada etapa, cambia a la rama correspondiente y revisa sus diferencias:

```bash
git switch <rama>
git diff <rama-anterior> <rama>
```

Ejecuta la aplicación y prueba cada endpoint desde `/docs` o con `curl`. El checkpoint de contratos y los siguientes dejan como ejercicios la asignación de IDs, persistencia, actualización, cierre, protección de tickets cerrados, soft delete, histórico para sugerencias de IA y pruebas automatizadas.

## CODE para definir la tarea

CODE es una regla mnemotécnica propuesta en este taller, no un estándar oficial. Sirve para convertir una petición vaga en un objetivo verificable:

| Letra | Pregunta | Ejemplo |
|---|---|---|
| C · Context | ¿Qué debe leer? | `DOMAIN.md` y `API_GUIDELINES.md` |
| O · Objective | ¿Qué cambia? | Implementar `DELETE` de tickets |
| D · Done | ¿Cuándo termina? | Respuestas `204` y `404`, con la documentación actualizada |
| E · Evaluation | ¿Cómo lo comprobamos? | Tests, Ruff y revisión del diff |

Una descripción vaga como “dejarlo production ready” no basta: la tarea debe definir resultados comprobables. La revisión del diff también debe detectar cambios fuera de alcance y dependencias innecesarias.

## Ejemplos de peticiones con CODE

### Intento A: petición breve sin contexto del repositorio

> Implementa los endpoints de tickets con FastAPI: crear, listar, consultar, editar, eliminar y analizar con IA.

Es breve, pero no indica qué documentos leer, qué significa eliminar, qué campos son editables, qué rutas forman el contrato ni cómo comprobar el resultado. Puede producir cambios fuera de alcance o incompatibles con las reglas del dominio.

### Intento B: convenciones dentro de un prompt largo

> Implementa una API completa y production ready para gestionar tickets con FastAPI y Pydantic v2. Debe usar arquitectura limpia, repositorios, servicios, autenticación, autorización, observabilidad, paginación, filtros, caché, eventos, integración con un proveedor de IA, migraciones, Docker, CI, documentación exhaustiva y cobertura total. Usa `/api/v1/tickets`, respuestas RESTful y buenas prácticas. Añade tests y validaciones.

Incluye muchas convenciones y deseos, pero no delimita una tarea concreta. “Production ready” no define cuándo termina el trabajo; además, puede introducir dependencias y componentes que el repositorio todavía no necesita.

### Intento C: petición breve con documentos e instrucciones

> Lee `docs/DOMAIN.md`, `docs/API_GUIDELINES.md` y los contratos objetivo de `docs/COURSE.md`. Implementa `PATCH /api/v1/tickets/{id}` usando `TicketUpdate`. Sólo permite cambiar los campos definidos por ese modelo; un ticket `closed` no puede editarse ni reabrirse. Conserva el soft delete y devuelve los errores definidos por las convenciones existentes. Termina cuando pasen los tests relevantes, Ruff y la revisión del diff no muestre cambios fuera de alcance.

Es breve, pero proporciona contexto, objetivo, definición de terminado y evaluación. También hace explícitas las reglas de dominio que podrían perderse en una petición genérica.

### Comparación: contrato, alcance y checks ejecutados

| Intento | Contrato | Alcance | Checks ejecutados |
|---|---|---|---|
| A | Implícito y ambiguo | Demasiado amplio | No definidos |
| B | Menciona convenciones, pero no recursos concretos | Excesivo: puede generar arquitectura y dependencias innecesarias | “Tests y validaciones” sin criterios de salida |
| C | Ruta, modelo y reglas explícitas | Limitado a `PATCH` y sus efectos necesarios | Tests relevantes, Ruff y revisión del diff |

La comparación muestra por qué CODE pide objetivos verificables: una buena petición no es la más larga, sino la que identifica el contexto necesario, limita el cambio y permite comprobar el resultado.
