from abc import ABC, abstractmethod
from typing import Dict, List

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.knowledge_base = {}

    @abstractmethod
    async def analyze(self, data: Dict) -> List[Dict]:
        """Analyze the provided data and return findings"""
        pass

    def load_rules(self, rules_file: str):
        """Load security rules from file"""
        pass