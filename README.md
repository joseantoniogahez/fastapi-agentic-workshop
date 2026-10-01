# FastAPI Production Ready

Workshop project for learning how modern APIs are built with FastAPI in a professional development environment.

The workshop focuses not only on creating endpoints, but on the engineering practices around them:

- API contracts with Pydantic
- application architecture
- persistence
- error handling
- automated testing
- dependency injection
- GenAI-assisted development
- `AGENTS.md`
- FastAPI Agent Skills
- testing AI-dependent features
- production-readiness concepts

## Workshop

**FastAPI: ¿Cómo se construyen APIs en la industria?**

Duration: 6 hours  
Format: 2 days  
Audience: junior developers and recent graduates

## Project

During the workshop we build a small support-ticket API called **SupportDesk API**.

The project evolves incrementally from a very simple FastAPI application into a structured and testable backend.

## Repository Structure

The `main` branch contains the completed project.

Each `step/*` branch represents a workshop checkpoint.

```text
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

Branches are cumulative and are intended to be used as teaching checkpoints.

## Course Guide

The complete workshop plan is available in:

```text
COURSE.md
```

Individual lesson guides are located in:

```text
COURSE.md (lesson details)
```

## Development

The project uses modern Python tooling and FastAPI.

Installation and development instructions will be added as the workshop implementation progresses.

## AI-Assisted Development

This repository is also designed to demonstrate how coding agents can work effectively with project-specific context.

Relevant files include:

```text
AGENTS.md
ARCHITECTURE.md
DOMAIN.md
API_GUIDELINES.md
```

The goal is to demonstrate the difference between simply prompting an AI and providing an agent with structured, reusable project context.

## License

MIT License.
