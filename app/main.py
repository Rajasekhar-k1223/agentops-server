# agentops-server/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import agents, commands
from app.middleware.auth import TokenAuthMiddleware

app = FastAPI(title="AgentOps Server")
# app.add_middleware(TokenAuthMiddleware)

# CORS (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agents.router, prefix="/agents", tags=["Agents"])
app.include_router(commands.router, prefix="/commands", tags=["Commands"])

@app.get("/")
def root():
    return {"message": "AgentOps Server is Running!"}
