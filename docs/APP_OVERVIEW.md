# SupportDesk

SupportDesk es una API para gestionar tickets de soporte. Permite crear, listar, consultar, editar, cerrar, eliminar lógicamente y analizar tickets con Gemini.

## Capacidades

- Los tickets se guardan en SQLite y reciben un ID generado por la base de datos.
- Los tickets nuevos comienzan abiertos; los tickets cerrados no se pueden editar ni eliminar.
- El borrado lógico conserva el registro y lo oculta de las consultas y del listado.
- El análisis con IA devuelve categoría, prioridad sugerida y resumen sin modificar el ticket.

## Ejecución y comprobación

Consulta [README.md](../README.md) para instalar y ejecutar la aplicación. El contrato HTTP está descrito en [API_GUIDELINES.md](API_GUIDELINES.md); las reglas del dominio están en [DOMAIN.md](DOMAIN.md).

Las pruebas se organizan por servicio, API y repositorio. El estado operativo y las decisiones de producción pendientes están descritos en la [guía de contexto](agent-guide.md) y sus referencias.
