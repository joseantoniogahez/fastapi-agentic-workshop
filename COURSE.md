# FastAPI: ¿Cómo se construyen APIs en la industria?

**Testing + GenAI + Agentic Development**

## Descripción del workshop

Este taller muestra cómo pasar de una API que simplemente “funciona” a una API organizada, testeable y preparada para trabajar dentro de un equipo de desarrollo moderno.

El objetivo no es enseñar todo FastAPI en seis horas.

El objetivo es que los participantes entiendan cómo se toman decisiones al construir una API en un entorno profesional y cómo cambia ese proceso cuando usamos agentes de IA como parte del flujo de desarrollo.

Durante el taller construiremos progresivamente una API de soporte técnico utilizando:

- Python
- FastAPI
- Pydantic
- SQLModel
- SQLite
- pytest
- HTTPX / TestClient
- Dependency Injection
- Coding Agents
- `AGENTS.md`
- FastAPI Agent Skill
- Generative AI
- automated quality checks

---

# Información del workshop

## Duración

6 horas en total.

- Día 1: 3 horas
- Día 2: 3 horas

Pausas recomendadas:

- Día 1: 10 minutos
- Día 2: 10 minutos

---

# Audiencia objetivo

Este workshop está diseñado principalmente para:

- recién egresados de Computer Science;
- junior backend developers;
- Python developers que están empezando con FastAPI;
- developers que ya conocen programación básica pero tienen experiencia limitada en backend profesional;
- developers que empiezan a usar coding agents como Codex.

Los participantes deberían entender conceptos básicos de Python:

- funciones;
- clases;
- imports;
- excepciones;
- listas y diccionarios;
- conceptos básicos de HTTP ayudan, pero no son obligatorios.

---

# Pregunta principal

El workshop gira alrededor de una pregunta:

> ¿Cómo pasamos de una API que funciona a una API que un equipo profesional de desarrollo podría mantener?

Una pregunta secundaria acompaña todo el workshop:

> Si un agente de IA puede escribir gran parte del código, ¿de qué es responsable el developer?

---

# Objetivos de aprendizaje

Al final del workshop, los participantes deberían poder:

1. Explicar el rol de un API contract.
2. Construir endpoints REST usando FastAPI.
3. Usar modelos de Pydantic para validar requests y responses.
4. Entender las responsabilidades de routers, services y repositories.
5. Usar Dependency Injection para reducir acoplamiento.
6. Persistir información usando SQLModel.
7. Distinguir errores de negocio de errores HTTP e infraestructura.
8. Escribir automated API tests usando pytest.
9. Usar dependency overrides y fakes al testear.
10. Integrar un servicio externo de IA sin acoplarlo directamente a endpoints HTTP.
11. Testear código que depende de servicios de IA no determinísticos o de pago.
12. Entender el rol de `AGENTS.md`, la documentación del proyecto y los library skills.
13. Usar coding agents con mejor contexto de proyecto.
14. Revisar código generado por IA en lugar de confiar en él ciegamente.
15. Identificar preocupaciones básicas de production-readiness.

---

# Filosofía del workshop

Este workshop está guiado por problemas, no por features.

No introducimos un concepto porque existe en FastAPI.

Lo introducimos porque la implementación actual crea un problema.

Ejemplos:

```text
dict accepts almost anything
        ↓
Pydantic contracts

main.py becomes too large
        ↓
Architecture

Business logic appears in routers
        ↓
Service layer

Tests require a real database
        ↓
Dependency Injection

LLM requests cost money
        ↓
FakeAIService

The coding agent makes inconsistent decisions
        ↓
AGENTS.md

The coding agent uses outdated FastAPI patterns
        ↓
FastAPI Agent Skill
```

Cada lección debería empezar con un problema.

Después, el nuevo concepto se introduce como solución.

---

# Proyecto del workshop

Construiremos un pequeño sistema de tickets de soporte llamado:

# SupportDesk API

El sistema administra solicitudes de soporte enviadas por usuarios.

Un ticket contiene:

```json
{
  "title": "Unable to log in",
  "description": "I receive an error when logging in.",
  "priority": "high",
  "status": "open"
}
```

La API final soportará operaciones como:

```text
POST   /api/v1/tickets
GET    /api/v1/tickets
GET    /api/v1/tickets/{ticket_id}
PATCH  /api/v1/tickets/{ticket_id}
DELETE /api/v1/tickets/{ticket_id}
```

El proyecto final también tendrá un endpoint asistido por IA:

```text
POST /api/v1/tickets/{ticket_id}/analyze
```

El servicio de IA puede devolver información como:

```json
{
  "category": "authentication",
  "suggested_priority": "high",
  "summary": "The user is unable to authenticate."
}
```

---

# Arquitectura final

La arquitectura final debería aproximarse a:

```text
Client
  |
  v
FastAPI
  |
  v
Router
  |
  v
Service
  |
  +----------------+
  |                |
  v                v
Repository      AI Service
  |                |
  v                v
Database           LLM
```

Componentes de soporte:

```text
Pydantic
OpenAPI
pytest
Dependency Injection
Configuration
Logging
AGENTS.md
FastAPI Agent Skill
Project documentation
```

---

# Estrategia del repositorio

El repositorio es educativo.

La rama `main` contiene la versión completa del proyecto del workshop.

Cada capítulo del workshop tiene una rama acumulativa.

Ejemplo:

```text
main

step/00-bootstrap
step/01-naive-api
step/02-api-contracts
step/03-project-context
step/04-agents-and-skills
step/05-architecture
step/06-persistence
step/07-error-handling
step/08-first-tests
step/09-testing-dependencies
step/10-ai-integration
step/11-testing-ai
step/12-production-readiness
```

Cada rama `step/*` representa un checkpoint completo de enseñanza.

Las ramas son acumulativas.

Por ejemplo:

```text
step/04
=
step/03
+
changes introduced in lesson 04
```

---

# Estrategia de commits

Las ramas representan capítulos.

Los commits representan pasos de enseñanza más pequeños.

Ejemplo:

```text
step/05-architecture

01 Move routes to APIRouter
02 Introduce TicketService
03 Introduce TicketRepository
04 Configure dependencies
05 Move business rules out of router
```

Los commits deberían ser lo suficientemente pequeños para explicarse de forma independiente.

Evita commits grandes que contengan cambios no relacionados.

---

# Documentación de lecciones

Cada lección debería tener un archivo correspondiente:

```text
docs/lessons/XX-name.md
```

Cada documento de lección debería contener:

```text
Problem
Learning objective
Starting point
Concept
Implementation steps
Demo
Exercise
Discussion questions
Common mistakes
Key takeaway
Branch
Relevant commits
```

---

# DÍA 1

# De un endpoint que funciona a una API mantenible

Duración: aproximadamente 3 horas.

La pregunta principal del Día 1 es:

> ¿Qué hace que una API sea mantenible más allá de simplemente devolver el JSON correcto?

---

# Lección 00 — Bootstrap

**Branch**

```text
step/00-bootstrap
```

**Duración aproximada**

15 minutos.

## Problema

Necesitamos la aplicación FastAPI más pequeña posible para que todos empiecen desde el mismo entorno.

## Objetivo de aprendizaje

Los participantes deberían entender los componentes mínimos necesarios para ejecutar una aplicación FastAPI.

## Conceptos

- project setup;
- dependencies;
- aplicación FastAPI;
- development server;
- health endpoint;
- Swagger UI;
- OpenAPI.

## Implementación

Crear:

```text
app/
    __init__.py
    main.py
```

Aplicación inicial:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}
```

## Demo

Ejecutar la aplicación.

Inspeccionar:

```text
/health
/docs
/openapi.json
```

## Discusión

Pregunta:

> ¿Qué generó FastAPI automáticamente para nosotros?

Respuestas esperadas:

- infraestructura de validación;
- documento OpenAPI;
- documentación Swagger;
- serialización.

## Key Takeaway

Una API no es solamente código ejecutable.

También expone un contrato legible por máquinas.

---

# Lección 01 — The Naive API

**Branch**

```text
step/01-naive-api
```

**Duración aproximada**

20 minutos.

## Problema

Queremos crear y consultar tickets lo más rápido posible.

## Implementación

Empezar con algo intencionalmente simple:

```python
tickets = []


@app.post("/tickets")
def create_ticket(ticket: dict):
    tickets.append(ticket)
    return ticket
```

Agregar:

```text
POST /tickets
GET /tickets
GET /tickets/{id}
```

## Discusión

Pregunta:

> ¿Esto funciona?

Sí.

Después pregunta:

> ¿Lo desplegarías?

Explorar:

- no hay validación;
- no hay persistencia real;
- no hay arquitectura;
- contracts poco claros;
- errores poco claros;
- estado global mutable;
- no hay tests.

## Ejercicio

Pide a los participantes identificar tantos problemas como sea posible.

## Key Takeaway

Software que funciona y software production-ready no son lo mismo.

---

# Lección 02 — API Contracts

**Branch**

```text
step/02-api-contracts
```

**Duración aproximada**

25 minutos.

## Problema

Usar `dict` significa que la API acepta input mal definido.

Ejemplo:

```json
{
  "title": 123,
  "priority": "SUPER_IMPORTANT"
}
```

## Objetivo de aprendizaje

Entender que una API es un contrato entre sistemas.

## Conceptos

- Pydantic;
- request schemas;
- response schemas;
- enums;
- status codes;
- validation;
- OpenAPI.

## Implementación

Introducir modelos como:

```text
TicketCreate
TicketUpdate
TicketResponse
Priority
TicketStatus
```

Ejemplo:

```python
class TicketCreate(BaseModel):
    title: str
    description: str
    priority: Priority
```

Introducir restricciones de validación.

Ejemplo:

```text
title:
3–100 characters

description:
maximum 2000 characters
```

## Demo

Enviar payloads inválidos.

Observar las respuestas de validación de FastAPI.

Inspeccionar `/docs` otra vez.

## Discusión

Pregunta:

> ¿Quién decide qué JSON puede enviar el frontend?

## Key Takeaway

El contrato debería ser explícito y verificable por máquinas.

---

# Lección 03 — Project Context and Documentation

**Branch**

```text
step/03-project-context
```

**Duración aproximada**

20 minutos.

## Problema

La aplicación ya tiene reglas, pero el conocimiento existe solamente en la cabeza del developer.

## Objetivo de aprendizaje

Entender la documentación como parte de la arquitectura de software.

## Introducir

```text
README.md
docs/DOMAIN.md
docs/ARCHITECTURE.md
docs/API_GUIDELINES.md
```

## Explicar responsabilidades

### README

Onboarding humano.

Preguntas que responde:

```text
What is this project?
How do I install it?
How do I run it?
How do I test it?
```

### DOMAIN.md

Conocimiento de negocio.

Ejemplo:

```text
A new ticket starts OPEN.

A CLOSED ticket cannot be edited.

Priority can be:
LOW
MEDIUM
HIGH
```

### ARCHITECTURE.md

Decisiones técnicas y flujo de dependencias.

### API_GUIDELINES.md

Convenciones como:

```text
POST creation -> 201
DELETE success -> 204
Missing resource -> 404
```

## Discusión

Pregunta:

> ¿Qué pasa cuando un nuevo developer se une al proyecto seis meses después?

Después:

> ¿Qué pasa cuando el nuevo developer es un agente de IA?

## Key Takeaway

La buena documentación reduce la cantidad de contexto que debe explicarse repetidamente.

---

# Lección 04 — AGENTS.md and FastAPI Skills

**Branch**

```text
step/04-agents-and-skills
```

**Duración aproximada**

30 minutos.

## Problema

Un coding agent conoce Python y FastAPI, pero no sabe automáticamente cómo este equipo particular construye software.

## Objetivo de aprendizaje

Entender la diferencia entre:

```text
Prompt
Project instructions
Project documentation
Library skills
Source code
Tests
```

## Introducir

```text
AGENTS.md
```

Discutir:

```text
Skill
=
how to use the technology

AGENTS.md
=
how this project uses the technology

Project documentation
=
why the project works this way
```

## Demostración

Ejecutar la misma solicitud con distintas cantidades de contexto.

### Intento 1

```text
Create an endpoint for creating tickets.
```

### Intento 2

Prompt grande que contiene arquitectura y convenciones.

### Intento 3

Repositorio configurado con:

```text
AGENTS.md
FastAPI Skill
DOMAIN.md
ARCHITECTURE.md
tests
```

Usar una solicitud mínima:

```text
Implement ticket creation according to the project guidelines.
```

Comparar resultados.

## Introducir Context Engineering

```text
Prompt Engineering
=
How should I ask?

Context Engineering
=
What information should the agent have available?
```

## Modelo mental sugerido

# CODE

```text
C — Context
O — Objective
D — Definition of Done
E — Evaluation
```

## Key Takeaway

El mejor desarrollo con GenAI normalmente se logra mejorando el contexto y los feedback loops, no escribiendo prompts cada vez más gigantes.

---

# Pausa

Duración recomendada:

10 minutos.

---

# Lección 05 — Architecture

**Branch**

```text
step/05-architecture
```

**Duración aproximada**

30 minutos.

## Problema

Nuestro `main.py` se está volviendo responsable de todo.

Actualmente contiene:

- lógica HTTP;
- reglas de negocio;
- persistencia;
- validación;
- manejo de errores.

## Objetivo de aprendizaje

Entender la separación de responsabilidades.

## Arquitectura objetivo

```text
Router
  |
  v
Service
  |
  v
Repository
```

## Responsabilidades

### Router

Preocupaciones HTTP.

Ejemplos:

```text
parameters
request models
response models
status codes
```

### Service

Comportamiento de negocio.

Ejemplos:

```text
Can this ticket be closed?
Can this status transition happen?
What happens when a ticket is created?
```

### Repository

Persistencia.

Ejemplos:

```text
get
create
update
delete
```

## Regla importante

No presentes esta arquitectura como la única arquitectura válida.

Explica:

> Architecture is a set of trade-offs and responsibility boundaries.

## Ejercicio

Da a los participantes piezas de lógica y pregunta:

> Router, Service or Repository?

## Key Takeaway

La organización del código debería seguir responsabilidades, no solo tipos de archivo.

---

# Lección 06 — Persistence

**Branch**

```text
step/06-persistence
```

**Duración aproximada**

30 minutos.

## Problema

Nuestros datos desaparecen cuando el proceso se reinicia.

## Objetivo de aprendizaje

Entender la persistencia como una responsabilidad separada.

## Conceptos

- SQLModel;
- SQLite;
- database session;
- repository implementation;
- constraints;
- IDs.

## Implementación

Reemplazar la lista en memoria con SQLite.

Mantener el acceso a base de datos dentro de repositories.

## Discusión

Pregunta:

> ¿Por qué el router no debería ejecutar SQL directamente?

Introducir brevemente las database constraints.

Ejemplos:

```text
NOT NULL
UNIQUE
foreign keys
```

## Momento de industria

Discutir:

```text
if not exists:
    insert()
```

Pregunta:

> ¿Qué pasa si dos requests ejecutan esto simultáneamente?

No profundizar en transaction isolation.

El objetivo es simplemente ilustrar que las validaciones de aplicación no reemplazan las constraints de base de datos.

## Key Takeaway

Las reglas de persistencia existen en múltiples capas.

---

# CIERRE DEL DÍA 1

Mostrar la evolución:

```text
@app.post(...)
def create(ticket: dict):
    tickets.append(ticket)
```

se convirtió en:

```text
Request
  |
Pydantic
  |
Router
  |
Service
  |
Repository
  |
Database
```

Y el repositorio ahora también contiene:

```text
README
DOMAIN
ARCHITECTURE
API_GUIDELINES
AGENTS.md
FastAPI Skill
```

Pregunta final del Día 1:

> El código se ve mejor. ¿Cómo sabemos que realmente funciona?

Eso se convierte en el punto de partida del Día 2.

---

# DÍA 2

# Testing, integración con IA y pensamiento de producción

Duración: aproximadamente 3 horas.

La pregunta principal del Día 2 es:

> ¿Cómo verificamos software escrito por humanos y agentes de IA?

---

# Lección 07 — Error Handling

**Branch**

```text
step/07-error-handling
```

**Duración aproximada**

20 minutos.

## Problema

Actualmente los errores se manejan de forma inconsistente.

Las reglas de negocio pueden lanzar excepciones HTTP directamente.

## Objetivo de aprendizaje

Entender distintas categorías de errores.

## Introducir

```text
Domain errors
HTTP errors
Infrastructure errors
```

Ejemplos:

```text
TicketNotFound
TicketAlreadyClosed
DatabaseUnavailable
AIProviderUnavailable
```

Después mapearlos a comportamiento HTTP.

Ejemplo:

```text
TicketNotFound
        ↓
404 Not Found
```

## Discusión

Pregunta:

> ¿TicketService debería saber qué significa HTTP 404?

## Key Takeaway

La lógica de negocio no debería depender innecesariamente de la capa de transporte.

---

# Lección 08 — First Automated Tests

**Branch**

```text
step/08-first-tests
```

**Duración aproximada**

30 minutos.

## Problema

El testing manual con Swagger solo prueba los ejemplos que ejecutamos manualmente.

## Objetivo de aprendizaje

Entender los automated tests como expectativas ejecutables.

## Introducir

- pytest;
- TestClient;
- assertions;
- happy path;
- error path;
- boundary cases.

## Tests iniciales

Ejemplos:

```text
create ticket
retrieve ticket
ticket not found
invalid priority
invalid title
```

## Mensaje importante de enseñanza

No digas:

> Estamos testeando FastAPI.

Di:

> Estamos testeando el comportamiento de nuestra aplicación.

## Ejercicio

Da a la clase una feature y pregunta:

> ¿Qué tests faltan?

## Key Takeaway

Los tests deberían derivarse del comportamiento esperado, no de la implementación actual.

---

# Lección 09 — Dependency Injection and Test Isolation

**Branch**

```text
step/09-testing-dependencies
```

**Duración aproximada**

30 minutos.

## Problema

Nuestros tests dependen de infraestructura real.

## Objetivo de aprendizaje

Entender cómo los límites de dependencia mejoran la testeabilidad.

## Conceptos

- Dependency Injection;
- FastAPI dependencies;
- fixtures;
- fakes;
- dependency overrides;
- isolation.

## Demostración

Reemplazar:

```text
SQLTicketRepository
```

por:

```text
FakeTicketRepository
```

durante tests seleccionados.

## Discutir

Diferencia entre:

```text
Fake
Mock
Stub
```

No profundizar demasiado en terminología.

Enfocarse en la intención.

## Pregunta importante

Pregunta:

> ¿Por qué ayer invertimos tiempo diseñando límites de dependencia?

La respuesta ahora debería ser obvia:

```text
replaceability
testability
separation
```

## Key Takeaway

La testeabilidad suele ser una propiedad arquitectónica.

---

# Pausa

Duración recomendada:

10 minutos.

---

# Lección 10 — AI as an External Dependency

**Branch**

```text
step/10-ai-integration
```

**Duración aproximada**

25 minutos.

## Problema

Product pregunta:

> ¿Puede la IA categorizar y resumir automáticamente los tickets de soporte?

## Objetivo de aprendizaje

Integrar IA sin acoplar la API directamente a un provider.

## Agregar endpoint

```text
POST /api/v1/tickets/{ticket_id}/analyze
```

## Arquitectura

No hacer:

```text
Router
  |
  v
OpenAI / Gemini / Anthropic directly
```

Preferir:

```text
Router
  |
Service
  |
AIService
  |
Provider
```

## AIService Contract

Conceptualmente:

```python
analyze_ticket(ticket) -> TicketAnalysis
```

## Discutir

Posibles fallas:

```text
timeout
rate limit
invalid JSON
provider unavailable
unexpected output
```

## Key Takeaway

Un LLM es una dependencia externa, no un componente mágico.

---

# Lección 11 — Testing AI-Dependent Features

**Branch**

```text
step/11-testing-ai
```

**Duración aproximada**

30 minutos.

## Problema

Llamar al LLM real durante cada test crea problemas.

Ejemplos:

```text
money
latency
network dependency
rate limits
nondeterminism
flaky tests
```

## Objetivo de aprendizaje

Entender cómo testear comportamiento de aplicación alrededor de IA sin requerir un modelo real.

## Introducir

```text
FakeAIService
```

Resultado determinístico de ejemplo:

```json
{
  "category": "authentication",
  "suggested_priority": "high",
  "summary": "Fake deterministic summary"
}
```

## Test

Verificar:

```text
HTTP behavior
data transformation
error handling
service coordination
```

sin requerir un LLM real.

## Discusión importante

Pide al coding agent que genere tests.

Después revísalos manualmente.

Buscar:

- tests duplicados;
- assertions sin sentido;
- mocking excesivo;
- solo happy paths;
- tests de detalles de implementación;
- boundary cases faltantes.

## Lección crítica

Mostrar este flujo:

```text
Requirement
   |
   +----------------+
   |                |
   v                v
Implementation     Tests
   ^                ^
   |                |
   +---- Human -----+
```

Explicar:

> Si tanto la implementación como los tests se generan solo desde la implementación misma, el mismo malentendido puede aparecer en ambos.

## Key Takeaway

La IA puede aumentar la cantidad de tests mucho más rápido que su calidad.

---

# Lección 12 — Production Readiness

**Branch**

```text
step/12-production-readiness
```

**Duración aproximada**

25 minutos.

## Problema

Todos los tests pasan.

¿Podemos desplegar?

## Objetivo de aprendizaje

Entender que pasar tests es necesario, pero no suficiente.

## Reto de production readiness

Pide a los participantes identificar preocupaciones faltantes.

Posibles respuestas:

### Configuration

```text
environment variables
settings
dev vs production
```

### Secrets

```text
API keys
database passwords
credentials
```

### Security

```text
authentication
authorization
input handling
```

### Database

```text
migrations
backups
connection management
```

### Reliability

```text
timeouts
retries
external services
```

### Observability

```text
logs
request IDs
metrics
traces
```

### Operations

```text
health checks
deployment
rollback
```

### Quality

```text
CI
linting
tests
type checking
```

## Introducir Definition of Done

Ejemplo:

```text
A task is complete when:

1. Required behavior is implemented.
2. Existing architecture is respected.
3. Tests cover new behavior.
4. Existing tests still pass.
5. Static quality checks pass.
6. No unnecessary dependency is introduced.
7. Public API changes are documented.
```

## Key Takeaway

“Works on my machine” es solo un checkpoint.

---

# REVIEW FINAL DEL WORKSHOP

Volver a la implementación original:

```python
@app.post("/tickets")
def create_ticket(ticket: dict):
    tickets.append(ticket)
    return ticket
```

Compararla con la arquitectura final.

```text
                        Client
                          |
                          v
                       FastAPI
                          |
                          v
                        Router
                          |
                          v
                        Service
                      /         \
                     v           v
              Repository      AIService
                  |               |
                  v               v
              Database           LLM
```

Soportada por:

```text
Pydantic contracts
OpenAPI
Automated tests
Dependency Injection
Error handling
Configuration
Documentation
AGENTS.md
FastAPI Skill
Quality checks
Human review
```

---

# Discusión final

Pregunta:

> ¿Qué hace un backend engineer si la IA puede generar el endpoint?

Discusión esperada:

```text
understand requirements
identify ambiguity
design contracts
choose boundaries
evaluate trade-offs
review generated code
design tests
debug failures
manage risk
protect compatibility
understand the business
take ownership
```

Mensaje final:

> Generative AI cambia qué tan rápido se puede producir código.
>
> No elimina la necesidad de engineering judgment.

---

# Ejercicio final sugerido

Dar a los participantes un nuevo requerimiento:

```text
Users want to add comments to support tickets.
```

No proporcionar instrucciones de implementación.

Pedir a los equipos determinar:

1. ¿Qué preguntas le harían a Product?
2. ¿Qué API contract propondrían?
3. ¿Qué reglas de negocio faltan?
4. ¿Qué documentación necesita actualizarse?
5. ¿Qué contexto debería recibir Codex?
6. ¿Qué código debería implementar el agente?
7. ¿Qué tests deberían existir?
8. ¿Qué podría romper a consumidores existentes?
9. ¿Qué preocupaciones de producción aparecerían?

El ejercicio no trata principalmente de escribir código.

El objetivo es practicar pensar como engineer antes de delegar la implementación a un agente.

---

# Guías para el instructor

## Evitar programar todo en vivo

El sistema de ramas debería permitir que el instructor se enfoque en conceptos.

Patrón recomendado:

```text
Explain problem
        ↓
Show current code
        ↓
Ask class what is wrong
        ↓
Introduce concept
        ↓
Show incremental diff
        ↓
Run application/tests
        ↓
Discuss result
```

---

# Regla para el instructor

Cada concepto técnico debería responder:

> ¿Qué problema resuelve esto?

Si esa pregunta no puede responderse claramente, considera quitar el tema del workshop de seis horas.

---

# Uso de agentes durante el workshop

Codex debería tratarse como otro participante en el proceso de desarrollo.

Úsalo para:

```text
implementation
refactoring
test generation
documentation
code review
debugging
```

Pero demuestra repetidamente que el output generado debe verificarse.

Workflow recomendado:

```text
Requirement
     |
     v
Coding Agent
     |
     v
Generated Change
     |
     +----------+
     |          |
     v          v
Tests       Human Review
     |          |
     +----+-----+
          |
          v
        Merge
```

---

# Guías de GenAI

Los participantes deberían aprender los siguientes principios.

## 1. Dar contexto antes que más prompt

Preferir:

```text
AGENTS.md
DOMAIN.md
ARCHITECTURE.md
FastAPI Skill
tests
```

en lugar de escribir prompts gigantes repetidamente.

---

## 2. Dar a los agentes objetivos verificables

Mal:

```text
Make this code production ready.
```

Mejor:

```text
Implement DELETE /tickets/{id}.

Requirements:

- Return 204 when successfully deleted.
- Return 404 when the ticket does not exist.
- Preserve the existing architecture.
- Add automated tests.
- Run the project quality checks before finishing.
```

---

## 3. No delegar ownership

El agente puede producir el código.

El developer es dueño del resultado.

---

## 4. Preferir feedback ejecutable

Preferir:

```text
pytest
ruff
type checker
integration tests
```

en lugar de:

```text
Make sure everything looks correct.
```

---

## 5. Proteger información sensible

Nunca exponer innecesariamente:

```text
production credentials
API keys
private customer information
database dumps
personal data
```

a sistemas de IA o prompts.

---

# Documentación del repositorio

Estructura final recomendada:

```text
.
├── README.md
├── AGENTS.md
├── pyproject.toml
├── .env.example
│
├── docs/
│   ├── COURSE.md
│   ├── DOMAIN.md
│   ├── ARCHITECTURE.md
│   ├── API_GUIDELINES.md
│   ├── GENAI_GUIDELINES.md
│   ├── PRODUCTION_CHECKLIST.md
│   │
│   └── lessons/
│       ├── 00-bootstrap.md
│       ├── 01-naive-api.md
│       ├── 02-api-contracts.md
│       ├── 03-project-context.md
│       ├── 04-agents-and-skills.md
│       ├── 05-architecture.md
│       ├── 06-persistence.md
│       ├── 07-error-handling.md
│       ├── 08-first-tests.md
│       ├── 09-testing-dependencies.md
│       ├── 10-ai-integration.md
│       ├── 11-testing-ai.md
│       └── 12-production-readiness.md
│
├── app/
│   ├── main.py
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   └── services/
│
└── tests/
```

---

# Checklist de ramas

Cada branch de lección debería cumplir:

```text
[ ] Runs successfully.
[ ] Introduces only concepts required by the lesson.
[ ] Is cumulative from the previous checkpoint.
[ ] Has understandable commits.
[ ] Has corresponding lesson documentation.
[ ] Does not prematurely implement later lessons.
[ ] Demonstrates a clear problem and solution.
```

---

# Checklist de main branch

La rama final `main` debería cumplir:

```text
[ ] Application starts successfully.
[ ] All endpoints work.
[ ] Database persistence works.
[ ] API contracts are documented.
[ ] Automated tests pass.
[ ] AI dependency can be replaced during tests.
[ ] Configuration comes from settings/environment.
[ ] Secrets are not committed.
[ ] Documentation reflects actual behavior.
[ ] AGENTS.md reflects project conventions.
[ ] FastAPI Skill can be used by supported agents.
[ ] Quality checks pass.
```

---

# Criterios de éxito

El workshop es exitoso si los participantes salen entendiendo que el desarrollo backend profesional no es:

```text
Write endpoint
     ↓
Done
```

sino:

```text
Understand requirement
        ↓
Define contract
        ↓
Design boundaries
        ↓
Implement
        ↓
Verify
        ↓
Review
        ↓
Observe
        ↓
Maintain
```

y que GenAI encaja dentro de este proceso como acelerador, no como reemplazo de la responsabilidad de ingeniería.
