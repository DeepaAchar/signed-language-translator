import yaml
from pathlib import Path
import shutil

# === CONFIGURATION ===
swagger_file = "signed-language-translation-api.yml"
package_name = "signedlang_api"
app_name = "main.py"
root = Path(package_name)

# === 1. Load Swagger YAML ===
with open(swagger_file, "r") as f:
    spec = yaml.safe_load(f)

# === 2. Create Folder Structure ===
(root / package_name).mkdir(parents=True, exist_ok=True)
(root / "tests").mkdir(exist_ok=True)
(root / "README.md").write_text("# Signed Language Translation API\n\nGenerated from OpenAPI YAML.")
(root / package_name / "__init__.py").touch()
shutil.copy(swagger_file, root / swagger_file)

# === 3. Generate FastAPI Routes ===
def format_func_name(path, method):
    return f"{method.lower()}_" + path.strip("/").replace("/", "_").replace("-", "_").replace("{", "").replace("}", "") or "root"

routes = []
for path, methods in spec.get("paths", {}).items():
    for method in methods:
        func = f"""
@app.{method.lower()}("{path}")
async def {format_func_name(path, method)}():
    return {{ "message": "Placeholder for {method.upper()} {path}" }}
""".strip()
        routes.append(func)

main_code = f"""
from fastapi import FastAPI

app = FastAPI(title="{spec['info']['title']}", version="{spec['info']['version']}")

{chr(10).join(routes)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
""".strip()

(root / package_name / app_name).write_text(main_code)

# === 4. Create pyproject.toml ===
pyproject = f"""
[project]
name = "{package_name}"
version = "0.1.0"
description = "{spec['info'].get('description', 'FastAPI app from Swagger')}"
authors = [{{ name = "Deepa Veerabhadrachar", email = "deepav2008@gmail.com" }}]
readme = "README.md"
requires-python = ">=3.9"
dependencies = ["fastapi", "uvicorn", "pyyaml"]

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
""".strip()

(root / "pyproject.toml").write_text(pyproject)

print(f"✅ FastAPI package created at: ./{package_name}")