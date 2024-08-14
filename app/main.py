import importlib
import os
from fastapi import FastAPI

app = FastAPI()

def import_routes(folder, prefix):
    for filename in os.listdir(f"app/api/{folder}/endpoints"):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = f"app.api.{folder}.endpoints.{filename[:-3]}"
            module = importlib.import_module(module_name)
            if hasattr(module, 'router'):
                app.include_router(module.router, prefix=f"/api/{prefix}")

# Import v1 routes
import_routes("v1", "v1")

# Import v2 routes
import_routes("v2", "v2")

@app.get("/")
def read_root():
    return {"Hello": "World"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)