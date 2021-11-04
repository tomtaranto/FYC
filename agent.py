from compte import Compte


class Agent():
    def __init__(self, name: str, agent_type: str, start_credit: float):
        assert agent_type in ["human", "bot"]
        self.name = name
        self.agent_type = agent_type
        self.compte = Compte(start_credit, 0)
        self.age = 0
