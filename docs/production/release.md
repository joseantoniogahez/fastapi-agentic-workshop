# CI, despliegue y rollback

## Estado

El repositorio declara pytest y Ruff como herramientas de desarrollo/dependencias en `pyproject.toml`, pero no contiene configuración de CI, contenedor, manifiestos de despliegue ni procedimiento de rollback. No hay configuración de Ruff más allá de la dependencia. El comando local documentado es `uv run fastapi dev app/main.py`; no es una receta de producción.

## Guía para cambios

- Define una tarea concreta y el entorno destino antes de introducir pipeline, imagen o manifiesto. No elijas plataforma ni servicio de hosting por suposición.
- Como mínimo, un pipeline acordado debería instalar dependencias reproducibles, ejecutar las comprobaciones del proyecto y construir el artefacto que se desplegará. No describas checks como automatizados hasta que un workflow los ejecute.
- Separa configuración y secretos del artefacto. Despliega una versión identificable y conserva la referencia a la versión anterior.
- Documenta promoción, verificación posterior al despliegue y señal que activa rollback. El rollback debe considerar compatibilidad entre versión de aplicación y esquema; revertir código no revierte datos.
- Si existen migraciones, planifica cambios compatibles por etapas y establece cómo detener una migración fallida y recuperar datos.

CI, despliegue y rollback son temas pendientes, no capacidades configuradas en este proyecto.
