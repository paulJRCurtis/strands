from .base_agent import BaseAgent
import json
import yaml
from typing import Dict

class ArchitectureParserAgent(BaseAgent):
    def __init__(self):
        super().__init__("ArchitectureParserAgent")

    async def parse(self, file) -> Dict:
        content = await file.read()
        filename = file.filename.lower()
        
        try:
            if filename.endswith('.json'):
                return json.loads(content)
            elif filename.endswith(('.yml', '.yaml')):
                return yaml.safe_load(content)
            else:
                # Basic text parsing for other formats
                return {'raw_content': content.decode('utf-8')}
        except Exception as e:
            return {'error': f'Failed to parse file: {str(e)}'}

    async def analyze(self, data: Dict) -> Dict:
        # Parser doesn't generate findings, just processes input
        return data