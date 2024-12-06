from datetime import datetime
from subprocess import run

import typer
import uvicorn

app = typer.Typer()


@app.command()
def runserver(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    uvicorn.run("src.main:app", host=host, port=port, reload=reload)


@app.command()
def makemigrations():
    run(
        [
            "alembic",
            "revision",
            "--autogenerate",
            "-m",
            f"""Migration {datetime.now().strftime("%d_%m_%Y")}""",
        ],
        check=True,
    )


@app.command()
def migrate():
    run(["alembic", "upgrade", "head"], check=True)


@app.command()
def format(path: str):
    run(
        ["ruff", "check", "--select", "I", "--fix", path],
        check=True,
    )
    run(
        ["ruff", "format", path],
        check=True,
    )


if __name__ == "__main__":
    app()
