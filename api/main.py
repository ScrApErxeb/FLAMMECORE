from fastapi import FastAPI
from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Any
from core.plugin_manager import PluginManager
from api.memoire_api import router as memoire_router

from core.executor import ActionExecutor  # à adapter selon ton import réel

app = FastAPI(title="FlammeCore API")

router = APIRouter()
plugin_manager = PluginManager()
executor = ActionExecutor(plugin_manager)


origins = ["http://localhost","http://localhost:5173", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Action(BaseModel):
    type: str

    class Config:
        extra = "allow"  # Autorise les champs supplémentaires dynamiques

class ExecuteRequest(BaseModel):
    actions: List[Dict[str, Any]]

    model_config = ConfigDict(extra="allow")


@app.post("/execute")
async def execute_actions(req: ExecuteRequest):
    results = executor.execute(req.actions)
    return {"results": results}

@router.get("/plugins")
def list_plugins():
    return {"plugins": list(plugin_manager.plugins.keys())}

app.include_router(memoire_router, prefix="/memoire", tags=["memoire"])
