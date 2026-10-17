# SupportDesk API

SupportDesk es un proyecto didáctico para construir una API de soporte con FastAPI. Los tickets persisten en SQLite; autenticación y migraciones todavía no están implementadas.

## Requisitos

- Python 3.11 o superior.
- `uv` (recomendado) o `pip`.

Instala [uv](https://docs.astral.sh/uv/getting-started/installation/) con Python:

```bash
python -m pip install uv
```

## Instalación

```bash
git clone https://github.com/joseantoniogahez/fastapi-agentic-workshop
cd fastapi-agentic-workshop
python -m venv .venv
```

Activa el entorno virtual:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```bash
# macOS/Linux
source .venv/bin/activate
```

Instala las dependencias con `uv`:

```bash
python -m pip install uv
uv sync
```

Como alternativa, usando `pip`:

```bash
python -m pip install -r requirements.txt
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv run fastapi dev app/main.py
```

La API queda disponible en <http://127.0.0.1:8000>. La documentación interactiva está en <http://127.0.0.1:8000/docs>, y el esquema OpenAPI en <http://127.0.0.1:8000/openapi.json>.

## Pruebas manuales

Comprueba que el servicio está vivo:

```bash
curl http://127.0.0.1:8000/health
```

Respuesta: `{\"status\":\"ok\"}`

Consulta los tickets guardados en SQLite:

```bash
curl http://127.0.0.1:8000/api/v1/tickets
```

Para crear un ticket, envía JSON a `POST /api/v1/tickets`:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/tickets \
  -H "Content-Type: application/json" \
  -d '{"title":"No puedo iniciar sesión","description":"La aplicación rechaza mi contraseña","priority":"high"}'
```

La respuesta es `201 Created`, incluye un ID autogenerado y el estado inicial `open`. SQLite usa `supportdesk.db` en el directorio de ejecución y la tabla se crea al iniciar la aplicación. No hay migraciones.

Las rutas disponibles permiten crear (`POST /api/v1/tickets`), listar (`GET /api/v1/tickets`), consultar (`GET /api/v1/tickets/{ticket_id}`), actualizar parcialmente (`PATCH /api/v1/tickets/{ticket_id}`), cerrar (`POST /api/v1/tickets/{ticket_id}/close`) y eliminar lógicamente (`DELETE /api/v1/tickets/{ticket_id}`). Actualización y cierre responden con `TicketResponse`; el borrado responde `204` sin cuerpo. IDs inexistentes o eliminados responden `404`; editar o eliminar un ticket cerrado responde `409`. Los errores de validación conservan `422`. El borrado oculta el ticket de consultas y listados, pero conserva su fila en SQLite.

Ejecuta la suite con `uv run pytest` (o instala `requirements.txt` y ejecuta `pytest`). Las pruebas separan reglas de servicio, contrato HTTP y persistencia SQLite temporal.

## Estructura

```text
app/
├── main.py       # aplicación FastAPI y registro de rutas
├── database.py   # engine SQLite y sesiones
├── models.py     # modelo ORM Ticket
├── repositories/ # acceso de tickets a SQLite
├── routers/      # endpoints HTTP
├── services/     # coordinación de casos de uso
└── schemas.py    # enums y contratos Pydantic
docs/             # documentación de dominio, arquitectura, API y curso
```

Consulta [docs/DOMAIN.md](docs/DOMAIN.md), [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), [docs/API_GUIDELINES.md](docs/API_GUIDELINES.md) y [docs/COURSE.md](docs/COURSE.md).

Para salir del entorno virtual: `deactivate`.
