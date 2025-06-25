# agentops-server/app/routes/commands.py
from fastapi import APIRouter, HTTPException
from app.models.schemas import CommandRequest
from app.services.command_queue import CommandQueue

router = APIRouter()
command_queue = CommandQueue()

@router.post("/send")
def send_command(cmd: CommandRequest):
    command_queue.enqueue(cmd.agent_id, cmd.command)
    return {"status": "command sent", "agent_id": cmd.agent_id}

@router.get("/get/{agent_id}")
def get_command(agent_id: str):
    command = command_queue.dequeue(agent_id)
    if command:
        return {"command": command}
    else:
        return {"command": None}
