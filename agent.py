from compte import Compte


class Agent():
    def __init__(self, name: str, agent_type: str, compte: Compte):
        assert agent_type in ["human", "bot"]
        self.name = name
        self.agent_type = agent_type
        self.compte = compte
        self.age = 0



