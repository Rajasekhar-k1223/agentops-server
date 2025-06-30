# # agentops-server/app/routes/commands.py
# from fastapi import APIRouter, HTTPException
# from app.models.schemas import CommandRequest
# from app.services.command_queue import CommandQueue

# router = APIRouter()
# command_queue = CommandQueue()

# @router.post("/send")
# def send_command(cmd: CommandRequest):
#     command_queue.enqueue(cmd.agent_id, cmd.command)
#     return {"status": "command sent", "agent_id": cmd.agent_id}

# @router.get("/get/{agent_id}")
# def get_command(agent_id: str):
#     command = command_queue.dequeue(agent_id)
#     if command:
#         return {"command": command}
#     else:
#         return {"command": None}
# agentops-server/app/routes/commands.py

from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.models.schemas import CommandRequest
from app.db.mongo import mongo_db

router = APIRouter()

# --------------------------------------------------------
# Send command to an agent
# --------------------------------------------------------
@router.post("/send")
async def send_command(cmd: CommandRequest):
    """
    Enqueue a command for an agent. Stored in MongoDB.
    """
    doc = {
        "agent_id": cmd.agent_id,
        "command": cmd.command,
        "timestamp": datetime.utcnow(),
        "executed": False,
    }
    await mongo.commands.insert_one(doc)
    return {
        "status": "command sent",
        "agent_id": cmd.agent_id,
        "command": cmd.command,
    }

# --------------------------------------------------------
# Agent fetches next pending command
# --------------------------------------------------------
@router.get("/get/{agent_id}")
async def get_command(agent_id: str):
    """
    Agent polls for next pending command.
    We return the first queued, unexecuted command and mark it as executed.
    """
    command_doc = await mongo.commands.find_one_and_update(
        {
            "agent_id": agent_id,
            "executed": False,
        },
        {
            "$set": {"executed": True, "executed_at": datetime.utcnow()}
        },
        sort=[("timestamp", 1)],
    )

    if command_doc:
        return {"command": command_doc["command"]}
    else:
        return {"command": None}
