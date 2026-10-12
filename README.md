# SupportDesk API

SupportDesk es un proyecto didáctico para construir una API de soporte con FastAPI. El repositorio se encuentra en una etapa temprana: los tickets viven en memoria y todavía no hay persistencia, autenticación ni suite de pruebas automatizadas.

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

Consulta los tickets:

```bash
curl http://127.0.0.1:8000/tickets
```

La creación de tickets está definida con validación de entrada. En el estado actual, `POST /tickets` aún no genera el campo `id` que exige `TicketResponse`; ese flujo puede producir un error de validación hasta que se implemente la asignación de identificadores.

## Estructura

```text
app/
├── main.py       # aplicación FastAPI y endpoints
└── schemas.py    # enums y modelos Pydantic
docs/             # documentación de dominio, arquitectura, API y curso
```

Consulta [docs/DOMAIN.md](docs/DOMAIN.md), [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), [docs/API_GUIDELINES.md](docs/API_GUIDELINES.md) y [docs/COURSE.md](docs/COURSE.md).

Para salir del entorno virtual: `deactivate`.
