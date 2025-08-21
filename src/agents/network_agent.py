from .base_agent import BaseAgent
from typing import Dict, List

class NetworkSecurityAgent(BaseAgent):
    def __init__(self):
        super().__init__("NetworkSecurityAgent")

    async def analyze(self, data: Dict) -> List[Dict]:
        findings = []
        
        # Check for exposed services
        if 'services' in data:
            for service in data['services']:
                if service.get('public', False) and not service.get('authentication'):
                    findings.append({
                        'severity': 'HIGH',
                        'category': 'Network Security',
                        'description': f"Service {service['name']} is publicly exposed without authentication",
                        'recommendation': 'Implement authentication or restrict access',
                        'affected_component': service['name']
                    })
        
        # Check firewall rules
        if 'firewall_rules' in data:
            for rule in data['firewall_rules']:
                if rule.get('source') == '0.0.0.0/0' and rule.get('port') != 443:
                    findings.append({
                        'severity': 'MEDIUM',
                        'category': 'Network Security',
                        'description': f"Overly permissive firewall rule on port {rule['port']}",
                        'recommendation': 'Restrict source IP ranges',
                        'affected_component': f"Port {rule['port']}"
                    })
        
        return findings