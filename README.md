# FastAPI Agentic Workshop

Proyecto base para experimentar con APIs construidas con [FastAPI](https://fastapi.tiangolo.com/).

## Requisitos

- Python 3.11 o superior.
- `uv` (recomendado) o `pip`.

Instala [uv](https://docs.astral.sh/uv/getting-started/installation/) con Python:

```bash
python -m pip install uv
```

## Instalación

1. Clona el repositorio y entra en la carpeta del proyecto:

   ```bash
   git clone https://github.com/joseantoniogahez/fastapi-agentic-workshop
   cd fastapi-agentic-workshop
   ```

2. Crea un entorno virtual:

   **Windows (PowerShell):**

   ```powershell
   python -m venv .venv
   .\\.venv\\Scripts\\Activate.ps1
   ```

   **macOS/Linux:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Sincroniza las dependencias con `uv`:

   ```shell
   uv sync
   ```

## Ejecutar la aplicación

Inicia el servidor de desarrollo desde la raíz del proyecto:

```shell
uv run fastapi dev app/main.py
```

La API estará disponible en <http://127.0.0.1:8000>.

## Endpoint disponible

### `GET /health`

Comprueba el estado de la aplicación.

```bash
curl http://127.0.0.1:8000/health
```

Respuesta esperada:

```json
{
  "status": "ok"
}
```

## Documentación interactiva

Con el servidor ejecutándose, visita:

- Swagger UI: <http://127.0.0.1:8000/docs>
- OpenAPI JSON: <http://127.0.0.1:8000/openapi.json>
- ReDoc: <http://127.0.0.1:8000/redoc>

## Estructura del proyecto

```text
.
├── app/
│   └── main.py          # Aplicación y rutas de FastAPI
├── pyproject.toml       # Configuración y dependencias para uv
├── uv.lock              # Versiones exactas (se genera con uv sync)
├── requirements.txt     # Dependencias para instalaciones con pip
├── LICENSE
└── README.md
```

## Desarrollo

Para salir del entorno virtual cuando termines:

```bash
deactivate
```
