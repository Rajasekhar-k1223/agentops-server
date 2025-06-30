from app.db.session import SessionLocal
from app.db.postgres import Agent
from sqlalchemy.exc import IntegrityError

class AgentManager:
    def __init__(self):
        self.db = SessionLocal()

    def register(self, agent_id: str, os: str, db):
        agent = db.query(Agent).filter_by(agent_id=agent_id).first()
        if not agent:
            new_agent = Agent(agent_id=agent_id, os=os)
            self.db.add(new_agent)
            try:
                self.db.commit()
            except IntegrityError:
                self.db.rollback()
        return True

