# agentops-server/app/models/schemas.py

from typing import List, Optional, Dict, Any,Union
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
    output: Union[str,List[Dict[str,str]]]

class PackageInfo(BaseModel):
    name: str
    version: str
    
class AgentPackages(BaseModel):
    agent_id: str
    packages: List[PackageInfo]

class AgentServices(BaseModel):
    agent_id: str
    services: List[dict]
    live_services: List[dict]


class LogData(BaseModel):
    agent_id: str
    logs: str

class SingleError(BaseModel):
    source: str
    message: str
    severity: str

class ErrorData(BaseModel):
    agent_id: str
    errors: List[SingleError]

class Finding(BaseModel):
    type: str
    details: str

class SecurityFinding(BaseModel):
    agent_id: str
    findings: List[Finding]

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