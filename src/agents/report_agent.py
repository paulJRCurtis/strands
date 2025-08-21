from .base_agent import BaseAgent
from typing import Dict, List

class ReportGeneratorAgent(BaseAgent):
    def __init__(self):
        super().__init__("ReportGeneratorAgent")

    async def generate(self, agent_results: List[List[Dict]]) -> Dict:
        all_findings = []
        for results in agent_results:
            all_findings.extend(results)
        
        # Calculate risk score
        risk_score = self._calculate_risk_score(all_findings)
        
        # Group findings by severity
        findings_by_severity = {
            'CRITICAL': [],
            'HIGH': [],
            'MEDIUM': [],
            'LOW': []
        }
        
        for finding in all_findings:
            severity = finding.get('severity', 'LOW')
            findings_by_severity[severity].append(finding)
        
        return {
            'total_findings': len(all_findings),
            'risk_score': risk_score,
            'findings_by_severity': findings_by_severity,
            'summary': self._generate_summary(findings_by_severity),
            'recommendations': self._generate_recommendations(all_findings)
        }

    def _calculate_risk_score(self, findings: List[Dict]) -> int:
        score = 0
        severity_weights = {'CRITICAL': 10, 'HIGH': 7, 'MEDIUM': 4, 'LOW': 1}
        
        for finding in findings:
            severity = finding.get('severity', 'LOW')
            score += severity_weights.get(severity, 1)
        
        return min(score, 100)

    def _generate_summary(self, findings_by_severity: Dict) -> str:
        critical = len(findings_by_severity['CRITICAL'])
        high = len(findings_by_severity['HIGH'])
        
        if critical > 0:
            return f"Critical security issues found ({critical} critical, {high} high severity)"
        elif high > 0:
            return f"High severity security issues found ({high} issues)"
        else:
            return "No critical security issues detected"

    def _generate_recommendations(self, findings: List[Dict]) -> List[str]:
        recommendations = set()
        for finding in findings:
            recommendations.add(finding.get('recommendation', ''))
        return list(recommendations)

    async def analyze(self, data: Dict) -> List[Dict]:
        # Report generator doesn't analyze, just consolidates
        return []