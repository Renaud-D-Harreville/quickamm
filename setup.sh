rm -rf .venv
python3.12 -m venv .venv --prompt quickamm
source .venv/bin/activate
pip install -U pip setuptools
pip install -e .[dev]