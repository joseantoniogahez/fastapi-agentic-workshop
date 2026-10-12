# Migraciones, backups y recuperación

## Estado

La persistencia usa SQLite en `supportdesk.db`. El lifespan ejecuta `Base.metadata.create_all(engine)` al iniciar. No hay herramienta de migraciones, política de backup ni procedimiento de recuperación en el repositorio. `create_all` crea tablas ausentes; no representa un historial de cambios de esquema.

## Guía para cambios

- Si el esquema necesita evolución reproducible, define primero la base de datos objetivo y adopta una herramienta de migración antes de depender de cambios destructivos o renombrados. Las migraciones deben revisarse y probarse desde una base vacía y desde la versión anterior.
- Diseña backup según el almacenamiento real y sus garantías. Para SQLite activa, evita copiar el archivo en un momento que pueda producir una copia inconsistente; el mecanismo concreto debe corresponder al modo de operación elegido.
- Documenta propietario, frecuencia, retención, ubicación protegida, cifrado y acceso a copias cuando el proyecto tome esas decisiones.
- Un backup no está validado hasta que se restaura en un entorno aislado y se verifica la aplicación. Registra el procedimiento y el resultado de restauración.
- Define objetivos de pérdida de datos y tiempo de recuperación (RPO/RTO) antes de prometer recuperación.

No afirmes que existe backup, migración o recuperación automática sin configuración y evidencia verificables.
