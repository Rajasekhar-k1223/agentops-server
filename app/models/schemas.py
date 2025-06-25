# agentops-server/app/models/schemas.py
from pydantic import BaseModel

class AgentRegister(BaseModel):
    agent_id: str
    os:str

class AgentCommandResult(BaseModel):
    agent_id: str
    output: str
    command: str

class CommandRequest(BaseModel):
    agent_id: str
    command: str