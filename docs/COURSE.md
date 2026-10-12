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
| A (`step/04-agents-and-skills-attempt-a`) | El prompt enumera seis capacidades, pero deja rutas y semántica abiertas. El resultado conserva el contrato existente de `/tickets` y añade lectura, PATCH, soft delete y análisis; es la mayor cobertura directa de la petición funcional. | Ventaja: implementa creación, listado, consulta, edición, eliminación y análisis con historial. Desventajas: toma decisiones no especificadas sobre campos editables, conflictos con tickets cerrados y análisis; no lee ni alinea explícitamente el contrato documentado. | El prompt no pide checks y la rama no contiene tests. No hay evidencia registrada de ejecución. |
| B (`step/04-agents-and-skills-attempt-b`) | El prompt propone `/api/v1/tickets` y el resultado lo respeta. Añade filtros, paginación y códigos HTTP probados en el código. | Ventaja: resultado más estructurado, separa repositorio/servicio y aporta cinco pruebas útiles. Desventaja: el prompt es muy ambicioso y el resultado sólo cubre una parte: faltan autenticación, autorización, observabilidad, caché, eventos, integración de IA, migraciones, Docker y CI; además, no implementa análisis. | El prompt pide tests y validaciones. La rama contiene cinco pruebas en `tests/test_tickets.py`, pero no hay reporte que confirme su ejecución; tampoco hay configuración de Ruff. |
| C (`step/04-agents-and-skills-attempt-c`) | El prompt especifica contexto, `PATCH /api/v1/tickets/{id}`, `TicketUpdate`, reglas para cerrados, soft delete y errores. El resultado sigue el prefijo y protege tickets cerrados, pero `TicketUpdate` omite `status`, por lo que no permite cerrar ni reabrir mediante PATCH; esto hace redundante la mención explícita a reapertura. | Ventaja: el cambio queda concentrado en `app/main.py` y `app/schemas.py`, sin capas ni dependencias añadidas, y mantiene creación, listado y borrado lógico. Desventaja: pese al alcance estrecho no añade pruebas, y la omisión de `status` impide cambiar el estado por la ruta solicitada. | El prompt define tests relevantes, Ruff y revisión del diff como salida. La rama no contiene tests ni configuración de Ruff, y no hay reporte de ejecución; los checks pedidos no quedan demostrados. |

La columna de checks distingue lo que cada prompt pidió de lo que puede comprobarse en la rama. B es el único resultado que aporta pruebas automatizadas, aunque no hay evidencia guardada de que se ejecutaran. Ninguna rama contiene un reporte de ejecución de checks. Las diferencias se compararon contra el checkpoint común `step/04-agents-and-skills` (`656b7f9`).

En conjunto, A gana en amplitud funcional frente a su prompt breve; B gana en estructura y cobertura de pruebas, pero deja muchas de sus propias ambiciones sin implementar; C gana en delimitación del alcance y evita trabajo extra, pero incumple un detalle importante de su contrato (`TicketUpdate` no permite cambiar el estado) y no demuestra sus checks de salida. C ofrece el mejor punto de partida para una tarea de implementación verificable, mientras que B deja más evidencia automatizada para evaluar comportamiento.

La comparación muestra por qué CODE pide objetivos verificables: una buena petición identifica el contexto necesario, limita el cambio y permite comprobar el resultado.
