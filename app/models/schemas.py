# agentops-server/app/models/schemas.py

from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class AgentRegister(BaseModel):
    agent_id: str
    os: str

class CommandRequest(BaseModel):
    agent_id: str
    command: str

class AgentCommandResult(BaseModel):
    agent_id: str
    command: str
    output: Any
    
class AgentPackages(BaseModel):
    agent_id: str
    packages: List[str]


class AgentServices(BaseModel):
    agent_id: str
    services: List[dict]
    live_services: List[dict]


class LogData(BaseModel):
    agent_id: str
    logs: str

class ErrorData(BaseModel):
    agent_id: str
    errors: List[Dict[str, Any]]

class SecurityFinding(BaseModel):
    agent_id: str
    findings: List[Dict[str, Any]]

class PackagesData(BaseModel):
    agent_id: str
    packages: List[str]

class ServicesData(BaseModel):
    agent_id: str
    services: List[Dict[str, Any]]
    live_services: List[Dict[str, Any]]

class SystemInfo(BaseModel):
    agent_id: str
    system_info: Dict[str, Any]

class AgentLogs(BaseModel):
    agent_id: str
    logs: str