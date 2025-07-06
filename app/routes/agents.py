# # agentops-server/app/routes/agents.py
# from fastapi import APIRouter, HTTPException
# from app.models.schemas import AgentRegister, AgentCommandResult
# from app.services.agent_manager import AgentManager
# from app.services.log_saver import save_command_output

# router = APIRouter()
# agent_manager = AgentManager()

# @router.post("/register")
# def register_agent(agent: AgentRegister):
#     agent_manager.register(agent.agent_id,agent.os)
#     return {"status": "registered", "agent_id": agent.agent_id}

# @router.get("/status/{agent_id}")
# def get_status(agent_id: str):
#     return {"agent_id": agent_id, "connected": agent_manager.is_online(agent_id)}

# @router.post("/result")
# def post_result(result: AgentCommandResult):
#     print(result)
#     save_command_output(result.agent_id, result.output,result.command)  # You can track last command sent too
#     return {"status": "received"}
# agentops-server/app/routes/agents.py

from app.utils.chunking import split_text_chunks
from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from app.models import schemas
from app.services.agent_manager import AgentManager
from app.db.mongo import mongo_db
from app.db.session import get_db
from sqlalchemy.orm import Session

router = APIRouter()
agent_manager = AgentManager()

# -------------------------------------------------
# Register Agent
# -------------------------------------------------
@router.post("/register")
async def register_agent(agent: schemas.AgentRegister, db: Session = Depends(get_db)):
    """
    Registers an agent.
    """
    print(agent.agent_id)
    print(agent.os)
    print(db)
    agent_manager.register(agent.agent_id, agent.os, db)
    return {"status": "registered", "agent_id": agent.agent_id}

# -------------------------------------------------
# Check agent status
# -------------------------------------------------
@router.get("/status/{agent_id}")
async def get_status(agent_id: str, db: Session = Depends(get_db)):
    connected = agent_manager.is_online(agent_id, db)
    return {"agent_id": agent_id, "connected": connected}

# -------------------------------------------------
# Receive command result
# -------------------------------------------------
@router.post("/result")
async def post_result(result: schemas.AgentCommandResult):
    doc = {
        "agent_id": result.agent_id,
        "timestamp": datetime.utcnow(),
        "command": result.command,
        "output": result.output
    }
    mongo_db.command_results.insert_one(doc)
    return {"status": "received"}

# -------------------------------------------------
# System info
# -------------------------------------------------
@router.post("/system_info")
async def post_system_info(info: schemas.SystemInfo):
    doc = {
        "agent_id": info.agent_id,
        "timestamp": datetime.utcnow(),
        "system_info": info.system_info
    }
    mongo_db.system_info.insert_one(doc)
    return {"status": "system info saved"}

# -------------------------------------------------
# Logs
# -------------------------------------------------
@router.post("/logs")
async def post_logs(logs: schemas.AgentLogs):
    doc = {
        "agent_id": logs.agent_id,
        "timestamp": datetime.utcnow(),
        "logs": logs.logs
    }
    mongo_db.logs.insert_one(doc)
    return {"status": "logs saved"}
    # chunks = split_text_chunks(logs.logs, chunk_size=50000)
    # docs = []
    # for chunk in chunks:
    #     docs.append({
    #         "agent_id": logs.agent_id,
    #         "timestamp": datetime.utcnow(),
    #         "log_chunk": chunk
    #     })
    # if docs:
    #     mongo_db.logs.insert_many(docs)
    # return {"status": f"{len(docs)} log chunks saved"}

# -------------------------------------------------
# Errors
# -------------------------------------------------
@router.post("/errors")
async def post_errors(errors: schemas.ErrorData):
    docs = []
    for e in errors.errors:
        docs.append({
            "agent_id": errors.agent_id,
            "timestamp": datetime.utcnow(),
            "source": e.source,
            "message": e.message,
            "severity": e.severity
        })
    if docs:
        mongo_db.errors.insert_many(docs)
    return {"status": f"{len(docs)} errors saved"}

# -------------------------------------------------
# Security findings
# -------------------------------------------------
@router.post("/security")
async def post_security(findings: schemas.SecurityFinding):
    docs = []
    for f in findings.findings:
        docs.append({
            "agent_id": findings.agent_id,
            "timestamp": datetime.utcnow(),
            "type": f.type,
            "details": f.details
        })
    if docs:
        mongo_db.security_findings.insert_many(docs)
    return {"status": f"{len(docs)} security findings saved"}

# -------------------------------------------------
# Packages
# -------------------------------------------------
@router.post("/packages")
async def post_packages(packages: schemas.AgentPackages):
    doc = {
        "agent_id": packages.agent_id,
        "timestamp": datetime.utcnow(),
        "packages": [pkg.dict() for pkg in packages.packages]
    }
    try:
        result = await mongo_db.packages.insert_one(doc)
        return {"status": "packages saved", "inserted_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
# @router.post("/packages")
# async def post_packages(packages: schemas.AgentPackages):
#     doc = {
#         "agent_id": packages.agent_id,
#         "timestamp": datetime.utcnow(),
#         "packages": packages.packages
#     }
#     mongo_db.packages.insert_one(doc)
#     return {"status": "packages saved"}
# @router.post("/packages")
# async def post_packages(packages: schemas.AgentPackages):
#     package_list = []
#     print(packages.packages)
#     for pkg in packages.packages:
#         if hasattr(pkg, "dict"):
#             package_list.append(pkg.dict())
#         elif isinstance(pkg, dict):
#             package_list.append(pkg)
#         else:
#             package_list.append({"name": str(pkg), "version": ""})
#     print(package_list)
#     doc = {
#         "agent_id": packages.agent_id,
#         "timestamp": datetime.utcnow(),
#         "packages": package_list
#     }
#     print(doc)
#     mongo_db.packages.insert_one(doc)
#     return {"status": "packages saved"}
# -------------------------------------------------
# Services
# -------------------------------------------------
@router.post("/services")
async def post_services(services: schemas.AgentServices):
    doc = {
        "agent_id": services.agent_id,
        "timestamp": datetime.utcnow(),
        "services": services.services,
        "live_services": services.live_services
    }
    mongo_db.services.insert_one(doc)
    return {"status": "services saved"}

# -------------------------------------------------
# Get next command for an agent
# -------------------------------------------------
@router.get("/commands/get/{agent_id}")
async def get_command(agent_id: str, db: Session = Depends(get_db)):
    cmd = agent_manager.get_next_command(agent_id, db)
    if cmd:
        return {"command": cmd}
    else:
        return {"command": None}
