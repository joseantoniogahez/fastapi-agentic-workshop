# SupportDesk API

SupportDesk es un proyecto didáctico para construir una API de soporte con FastAPI. La creación de tickets persiste en SQLite; autenticación y una suite de pruebas automatizadas todavía no están implementadas.

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

## Estructura

```text
app/
├── main.py       # aplicación FastAPI y registro de rutas
├── database.py   # engine SQLite y sesiones
├── models.py     # modelo ORM Ticket
├── repositories/ # acceso de creación a SQLite
├── routers/      # endpoints HTTP
├── services/     # coordinación de casos de uso
└── schemas.py    # enums y contratos Pydantic
docs/             # documentación de dominio, arquitectura, API y curso
```

Consulta [docs/DOMAIN.md](docs/DOMAIN.md), [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), [docs/API_GUIDELINES.md](docs/API_GUIDELINES.md) y [docs/COURSE.md](docs/COURSE.md).

Para salir del entorno virtual: `deactivate`.
