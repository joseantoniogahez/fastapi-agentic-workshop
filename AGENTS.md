# AGENTS.md

## SupportDesk

- Read `.agents/skills/supportdesk/SKILL.md` for the repository workflow.
- Start with `docs/agent-guide.md`; open only the production reference needed for the task.
- Read `docs/APP_OVERVIEW.md` and `docs/API_GUIDELINES.md` before changing the API.
- Use Pydantic v2 conventions and keep examples small and explainable.
- Check behavior with the available tests.
- Organiza las pruebas por nivel en archivos separados: `test_ticket_service.py` para reglas del dominio con repositorios fake, `test_tickets_api.py` para HTTP y coordinación, y `test_ticket_repository.py` para persistencia real con SQLite temporal. Añade pruebas de sistema externo sólo cuando haya un adaptador cuya compatibilidad verificar.
- Revisa qué documentación queda afectada por cada cambio y actualiza sólo la estrictamente necesaria; mantén la información consistente, mí­nima y suficiente, evitando redundancias.
- La preparación para producción en este repositorio es documentación de decisiones y revisión; no presupongas que exista un despliegue real ni agregues infraestructura sin una tarea concreta.
