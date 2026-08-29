"""Renders datasources.yml from datasources.yml.template + .env.

Why this exists: Grafana's stock provisioning loader has no officially
documented ${VAR} expansion for arbitrary fields in datasources.yml
(only certain env-prefixed images/entrypoints support it, and none of
those apply to the plain `grafana/grafana` image used here — verified
by search, not assumed). `envsubst` was considered and rejected: it
isn't installed by default everywhere this repo might run, so a
Makefile target depending on it silently breaks portability. Python is
already a hard dependency of this project, so this script is the one
substitution mechanism guaranteed to work everywhere `make` does.

Usage: python grafana/render_datasources.py
Reads: grafana/provisioning/datasources/datasources.yml.template, .env
Writes: grafana/provisioning/datasources/datasources.yml (gitignored —
        contains real credentials once rendered, never commit it)
"""

import re
import sys
from pathlib import Path

TEMPLATE = Path("grafana/provisioning/datasources/datasources.yml.template")
OUTPUT = Path("grafana/provisioning/datasources/datasources.yml")
ENV_FILE = Path(".env")
VAR_PATTERN = re.compile(r"\$\{([A-Z_][A-Z0-9_]*)\}")


def load_env(path: Path) -> dict:
    if not path.exists():
        print(f"::error::{path} not found. Copy .env.example to .env first.")
        sys.exit(1)
    values = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def render(template_text: str, env: dict) -> str:
    missing = []

    def replace(match: "re.Match[str]") -> str:
        var = match.group(1)
        if var not in env:
            missing.append(var)
            return match.group(0)
        return env[var]

    result = VAR_PATTERN.sub(replace, template_text)
    if missing:
        print(f"::error::Missing required vars in .env: {', '.join(sorted(set(missing)))}")
        sys.exit(1)
    return result


def main() -> None:
    if not TEMPLATE.exists():
        print(f"::error::{TEMPLATE} not found. Run this from the repo root.")
        sys.exit(1)
    env = load_env(ENV_FILE)
    rendered = render(TEMPLATE.read_text(), env)
    OUTPUT.write_text(rendered)
    print(f"Rendered {OUTPUT} from {TEMPLATE} + {ENV_FILE}")


if __name__ == "__main__":
    main()
