#!/bin/bash
# python3 -m venv sandbox.venv

PYTHON_VERSION=$(cat .python-version)

# if this is the first run,
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    uv python install ${PYTHON_VERSION}
    uv venv
    uv lock
    uv sync
    uv pip compile pyproject.toml -o requirements.txt
    uv pip install -r requirements.txt
    pre-commit install -f
    # uv init --python ${PYTHON_VERSION}
    # uv add ruff
    # uv add black
    # uv add pylint
    # uv add isort

    # pyenv local ${PYTHON_VERSION}

    source .venv/bin/activate
fi

# uv run ruff check
# uv run black .
# uv run isort .
# uv run pylint --disable=all --enable=fixme --max-line-length=120 --output-format=json --reports=n --msg-template="{path}:{line}: [{category}({symbol}), {obj}] {msg}" --rcfile=.pylintrc .
