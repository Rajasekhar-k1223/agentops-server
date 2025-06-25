# agentops-server/app/routes/agents.py
from fastapi import APIRouter, HTTPException
from app.models.schemas import AgentRegister, AgentCommandResult
from app.services.agent_manager import AgentManager
from app.services.log_saver import save_command_output

router = APIRouter()
agent_manager = AgentManager()

@router.post("/register")
def register_agent(agent: AgentRegister):
    agent_manager.register(agent.agent_id,agent.os)
    return {"status": "registered", "agent_id": agent.agent_id}

@router.get("/status/{agent_id}")
def get_status(agent_id: str):
    return {"agent_id": agent_id, "connected": agent_manager.is_online(agent_id)}

@router.post("/result")
def post_result(result: AgentCommandResult):
    print(result)
    save_command_output(result.agent_id, result.output,result.command)  # You can track last command sent too
    return {"status": "received"}
