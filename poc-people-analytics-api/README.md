uv init <project-name>

uv add <package-name>

uv add --dev python-dotenv[cli]

uv tool install ruff poethepoet

uv pip compile pyproject.toml --universal --output-file requirements.txt

uv venv

uv pip sync requirements.txt

uv sync --no-dev
