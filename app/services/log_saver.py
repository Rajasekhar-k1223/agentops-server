from app.db.mongo import logs_collection, system_info_collection
from datetime import datetime

def save_command_output(agent_id, output, command):
    logs_collection.insert_one({
        "agent_id": agent_id,
        "command": command,
        "output": output,
        "timestamp": datetime.utcnow()
    })

def save_system_info(agent_id, info: dict):
    system_info_collection.update_one(
        {"agent_id": agent_id},
        {"$set": {"info": info, "last_updated": datetime.utcnow()}},
        upsert=True
    )
