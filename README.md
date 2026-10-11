# SupportDesk API

SupportDesk es un proyecto didáctico para construir una API de soporte con FastAPI. La aplicación ofrece health check y creación de tickets; estos se persisten en SQLite. Incluye un test de comportamiento para la creación de tickets. Todavía no hay autenticación.

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

Crea un ticket:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/tickets `
  -H "Content-Type: application/json" `
  -d '{"title":"No puedo iniciar sesión","description":"El portal rechaza mi contraseña"}'
```

La respuesta de creación tiene estado `201 Created` e incluye el `id` generado, la prioridad `medium` y el estado inicial `open`. Para otros ejemplos y las reglas del contrato, consulta [docs/API_GUIDELINES.md](docs/API_GUIDELINES.md).

Puedes consultar el ticket usando el `id` devuelto:

```bash
curl http://127.0.0.1:8000/api/v1/tickets/1
```

La consulta devuelve `200 OK`, o `404 Not Found` si el ID no existe. Los tickets permanecen en `supportdesk.db` en el directorio desde el que se inicia la aplicación.

## Estructura

```text
app/
├── main.py        # aplicación FastAPI, health check y manejador 404
├── router.py      # endpoints HTTP de tickets
├── services.py    # lógica de creación y consulta
├── repositories.py # acceso a datos
├── models.py      # modelo SQLAlchemy
├── database.py    # motor y sesiones SQLite
└── schemas.py     # enums y modelos Pydantic
docs/             # documentación de dominio, arquitectura, API y curso
```

Consulta [docs/DOMAIN.md](docs/DOMAIN.md), [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), [docs/API_GUIDELINES.md](docs/API_GUIDELINES.md) y [docs/COURSE.md](docs/COURSE.md).

Para salir del entorno virtual: `deactivate`.
