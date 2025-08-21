from .base_agent import BaseAgent
from typing import Dict, List

class InfrastructureAgent(BaseAgent):
    def __init__(self):
        super().__init__("InfrastructureAgent")

    async def analyze(self, data: Dict) -> List[Dict]:
        findings = []
        
        # Check IAM policies
        if 'iam_policies' in data:
            for policy in data['iam_policies']:
                if '*' in policy.get('actions', []):
                    findings.append({
                        'severity': 'HIGH',
                        'category': 'Infrastructure Security',
                        'description': f"IAM policy {policy['name']} grants wildcard permissions",
                        'recommendation': 'Apply principle of least privilege',
                        'affected_component': policy['name']
                    })
        
        # Check S3 bucket configurations
        if 'storage' in data:
            for bucket in data['storage']:
                if bucket.get('public_read', False):
                    findings.append({
                        'severity': 'CRITICAL',
                        'category': 'Infrastructure Security',
                        'description': f"Storage bucket {bucket['name']} allows public read access",
                        'recommendation': 'Restrict bucket access and enable access logging',
                        'affected_component': bucket['name']
                    })
        
        return findings