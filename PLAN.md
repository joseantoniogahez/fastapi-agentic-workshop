# Plan del curso

Guía para impartir el workshop **FastAPI: Testing + GenAI + Agentic Development** en dos sesiones de tres horas. Úsala como agenda; [COURSE.md](COURSE.md) conserva el contenido y los detalles de cada lección.

## Antes del curso

- [ ] Confirmar que todos tienen Python, Git y un coding agent configurados.
- [ ] Clonar el repositorio y comprobar que la aplicación de `step/00-bootstrap` arranca.
- [ ] Tener listo el acceso a las ramas `step/*` y una forma de mostrar diffs.
- [ ] Preparar una pizarra para anotar problemas, decisiones y preguntas abiertas.
- [ ] Aclarar que no se necesita una API key de un proveedor de IA: durante las pruebas se usará un fake.

## Día 1 — De un endpoint que funciona a una API mantenible

**Meta:** reconocer los límites de una API improvisada y construir contratos, contexto y arquitectura inicial.

| Tiempo | Bloque | Qué hacemos | Checkpoint |
|---|---|---|---|
| 00:00–00:10 | Apertura | Presentar SupportDesk, objetivos y la pregunta guía: ¿qué hace mantenible a una API? | El grupo entiende el problema que resolverá el taller. |
| 00:10–00:25 | 00 · Bootstrap (15 min) | Ejecutar `/health`; revisar `/docs` y `/openapi.json`. | Aplicación mínima funcionando. |
| 00:25–00:45 | 01 · The Naive API (20 min) | Crear y consultar tickets en memoria; listar riesgos antes de avanzar. | El grupo identifica qué funciona y qué falta para desplegar. |
| 00:45–01:10 | 02 · API Contracts (25 min) | Añadir esquemas Pydantic, enums, validación y códigos de estado; probar payloads inválidos. | Contrato visible y validación comprobada en OpenAPI. |
| 01:10–01:30 | 03 · Project Context (20 min) | Revisar README, reglas de dominio, arquitectura y convenciones de API. | Las decisiones importantes dejan de vivir solo en la cabeza del developer. |
| 01:30–02:00 | 04 · Agents and Skills (30 min) | Comparar prompt, instrucciones del repo y documentación; usar el agente en una tarea acotada y revisar el resultado. | El grupo puede dar contexto verificable y evaluar el cambio generado. |
| 02:00–02:10 | Pausa (10 min) | Descanso. | — |
| 02:10–02:40 | 05 · Architecture (30 min) | Separar router, service y repository; seguir el flujo de una petición. | Cada capa tiene una responsabilidad clara. |
| 02:40–03:00 | 06 · Persistence (20 min) | Conectar SQLModel y SQLite; mostrar cómo el repository encapsula el acceso a datos. | Los tickets sobreviven al reinicio de la aplicación. |
| 03:00–03:00 | Cierre | Preguntar: “El código se ve mejor. ¿Cómo sabemos que realmente funciona?” Recoger respuestas para abrir el Día 2. | Queda planteada la necesidad de manejo de errores y pruebas. |

> **Ajuste de agenda:** las lecciones 00–06 suman 160 minutos; con apertura, pausa y cierre se excedían las tres horas. Para mantener el Día 1 en 180 minutos, se asignan 20 minutos a persistencia y se integran apertura y cierre en los bloques indicados. Si la demostración de SQLModel requiere más tiempo, recorta la discusión de la lección 01 o deja la persistencia preparada en el checkpoint.

## Día 2 — Testing, IA y pensamiento de producción

**Meta:** demostrar cómo se verifica el comportamiento, se aíslan dependencias y se evalúa si el sistema está listo para operar.

| Tiempo | Bloque | Qué hacemos | Checkpoint |
|---|---|---|---|
| 00:00–00:10 | Reentrada | Reconstruir el flujo router → service → repository y retomar la pregunta del cierre. | El grupo conecta arquitectura con testeabilidad. |
| 00:10–00:30 | 07 · Error Handling (20 min) | Distinguir errores de dominio, HTTP e infraestructura; observar respuestas esperadas. | Los errores tienen una traducción clara hacia el cliente. |
| 00:30–01:00 | 08 · First Automated Tests (30 min) | Escribir pruebas de API para caso exitoso, error y límite con pytest y TestClient. | La conducta básica se comprueba automáticamente. |
| 01:00–01:30 | 09 · Testing Dependencies (30 min) | Usar dependency overrides y FakeRepository para aislar la prueba. | Las pruebas no requieren una base de datos real. |
| 01:30–01:40 | Pausa (10 min) | Descanso. | — |
| 01:40–02:05 | 10 · AI Integration (25 min) | Diseñar `AIService` e incorporar `POST /api/v1/tickets/{ticket_id}/analyze`; discutir fallas del proveedor. | La ruta no depende directamente de un proveedor concreto. |
| 02:05–02:35 | 11 · Testing AI (30 min) | Sustituir el servicio por un fake determinístico; generar o revisar pruebas y buscar casos faltantes. | La función se prueba sin red, costo ni resultados variables. |
| 02:35–03:00 | 12 · Production Readiness (25 min) | Revisar configuración, secretos, seguridad, fiabilidad, observabilidad y Definition of Done. | El grupo distingue pruebas verdes de preparación para producción. |
| 03:00–03:00 | Cierre y ejercicio | Presentar el requerimiento de comentarios en tickets; pedir contrato, reglas, contexto para el agente y pruebas. | El grupo aplica el proceso completo a un cambio nuevo. |

> **Ajuste de agenda:** las lecciones 07–12 suman 160 minutos; al añadir reentrada, pausa y ejercicio final se excedían las tres horas. Para cerrar a tiempo, combina la reentrada con la lección 07 y usa el ejercicio de comentarios como actividad de cierre dentro de los 25 minutos de producción readiness. Si quieres un ejercicio práctico completo, reserva 15 minutos y reduce la demo de integración de IA a 15 minutos.

## Ritmo de cada lección

Repite este ciclo y adapta el tiempo según las preguntas del grupo:

1. Explica el problema que aparece en el checkpoint actual.
2. Muestra el código y pregunta qué riesgos observan.
3. Introduce el concepto que resuelve ese problema.
4. Revisa el diff incremental de la rama o commit siguiente.
5. Ejecuta la aplicación o las pruebas para comprobar el cambio.
6. Cierra con una pregunta: ¿qué decisión tomarían distinto en un sistema real?

## Reglas para mantener el ritmo

- Usa las ramas `step/*` como checkpoints restaurables y los commits como pasos pequeños de enseñanza.
- Evita escribir toda la aplicación en vivo; dedica el tiempo a decisiones, diffs y verificación.
- Cada bloque debe responder: **¿qué problema resuelve este concepto?**
- Al pedir trabajo a un coding agent, incluye objetivo, restricciones y una forma observable de verificarlo.
- Trata el resultado del agente como una propuesta: ejecutar pruebas y revisar el cambio sigue siendo responsabilidad del equipo.
- Si un bloque se alarga, conserva la idea central y deja la implementación extendida como ejercicio posterior.

## Cierre del workshop

Vuelve al endpoint inicial con `dict` y estado en memoria. Pide al grupo que describa qué cambió: contrato, límites entre capas, persistencia, manejo de errores, pruebas y dependencias reemplazables. Termina con el ejercicio de comentarios y pregunta qué aclararían con Product antes de delegar código.

La idea que debe quedar es el flujo de trabajo:

```text
Entender el requisito → definir el contrato → diseñar límites → implementar → verificar → revisar → operar y mantener
```
