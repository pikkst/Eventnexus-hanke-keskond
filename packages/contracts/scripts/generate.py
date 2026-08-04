from __future__ import annotations

import json
import os
import sys
from pathlib import Path

os.environ["DEBUG"] = "false"

repo_root = Path(__file__).resolve().parent.parent.parent.parent
api_dir = repo_root / "apps" / "api"
sys.path.insert(0, str(api_dir))

from app.config import AppEnvironment, Settings
from app.main import create_app


def main() -> None:
    settings = Settings(
        app_env=AppEnvironment.TESTING,
        debug=False,
        secret_key="test-secret-key-for-contract-generation",
        log_level="WARNING",
        log_format="json",
    )
    app = create_app(settings=settings)
    schema = app.openapi()

    output_dir = repo_root / "packages" / "contracts" / "dist"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "openapi.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2, ensure_ascii=False, sort_keys=True)
        f.write("\n")

    print(f"Generated OpenAPI schema to {output_file}")


if __name__ == "__main__":
    main()