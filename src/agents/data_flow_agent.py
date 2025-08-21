from .base_agent import BaseAgent
from typing import Dict, List

class DataFlowAgent(BaseAgent):
    def __init__(self):
        super().__init__("DataFlowAgent")

    async def analyze(self, data: Dict) -> List[Dict]:
        findings = []
        
        # Check for unencrypted data flows
        if 'data_flows' in data:
            for flow in data['data_flows']:
                if not flow.get('encrypted', False):
                    findings.append({
                        'severity': 'HIGH',
                        'category': 'Data Protection',
                        'description': f"Unencrypted data flow from {flow['source']} to {flow['destination']}",
                        'recommendation': 'Enable encryption in transit',
                        'affected_component': f"{flow['source']} -> {flow['destination']}"
                    })
        
        # Check for PII exposure
        if 'databases' in data:
            for db in data['databases']:
                if 'pii' in db.get('data_types', []) and not db.get('encrypted_at_rest'):
                    findings.append({
                        'severity': 'CRITICAL',
                        'category': 'Data Protection',
                        'description': f"Database {db['name']} contains PII but is not encrypted at rest",
                        'recommendation': 'Enable database encryption',
                        'affected_component': db['name']
                    })
        
        return findings