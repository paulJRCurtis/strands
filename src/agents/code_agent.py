from .base_agent import BaseAgent
from typing import Dict, List

class CodeSecurityAgent(BaseAgent):
    def __init__(self):
        super().__init__("CodeSecurityAgent")

    async def analyze(self, data: Dict) -> List[Dict]:
        findings = []
        
        # Check for hardcoded secrets
        if 'code_files' in data:
            for file_data in data['code_files']:
                content = file_data.get('content', '')
                if 'password' in content.lower() or 'api_key' in content.lower():
                    findings.append({
                        'severity': 'CRITICAL',
                        'category': 'Application Security',
                        'description': f"Potential hardcoded credentials in {file_data['name']}",
                        'recommendation': 'Use environment variables or secret management',
                        'affected_component': file_data['name']
                    })
        
        # Check authentication mechanisms
        if 'authentication' in data:
            auth = data['authentication']
            if not auth.get('multi_factor', False):
                findings.append({
                    'severity': 'MEDIUM',
                    'category': 'Application Security',
                    'description': 'Multi-factor authentication not implemented',
                    'recommendation': 'Enable MFA for enhanced security',
                    'affected_component': 'Authentication System'
                })
        
        return findings