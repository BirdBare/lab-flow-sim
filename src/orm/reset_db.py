import os
import pathlib

for root, dirs, files in os.walk(pathlib.Path(__file__).parent):
    for file in files:
        if "migrations" in root and "__init__.py" not in file:
            (pathlib.Path(root) / file).unlink()
        if file == "db.sqlite3":
            (pathlib.Path(root) / file).unlink()
