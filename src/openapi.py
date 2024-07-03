import json
import os

from app import app

os.chdir(os.path.dirname(__file__))

with open("./web/openapi.json", "w") as f:
    api_spec = app.openapi()
    f.write(json.dumps(api_spec))
