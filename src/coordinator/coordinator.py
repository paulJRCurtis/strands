import asyncio
import uuid
from typing import Dict, List
from ..agents.network_agent import NetworkSecurityAgent
from ..agents.data_flow_agent import DataFlowAgent
from ..agents.infrastructure_agent import InfrastructureAgent
from ..agents.code_agent import CodeSecurityAgent
from ..agents.parser_agent import ArchitectureParserAgent
from ..agents.report_agent import ReportGeneratorAgent

class CoordinatorAgent:
    def __init__(self):
        self.parser = ArchitectureParserAgent()
        self.agents = {
            'network': NetworkSecurityAgent(),
            'data_flow': DataFlowAgent(),
            'infrastructure': InfrastructureAgent(),
            'code': CodeSecurityAgent()
        }
        self.report_generator = ReportGeneratorAgent()
        self.jobs = {}

    async def process_analysis(self, file):
        job_id = str(uuid.uuid4())
        self.jobs[job_id] = {'status': 'processing', 'results': None}
        
        # Parse architecture
        parsed_data = await self.parser.parse(file)
        
        # Run agents in parallel
        tasks = [agent.analyze(parsed_data) for agent in self.agents.values()]
        results = await asyncio.gather(*tasks)
        
        # Generate report
        report = await self.report_generator.generate(results)
        
        # Convert findings to the expected format
        all_findings = []
        for severity_findings in report['findings_by_severity'].values():
            all_findings.extend(severity_findings)
        
        self.jobs[job_id] = {'status': 'completed', 'results': report}
        return {
            'job_id': job_id, 
            'status': 'completed', 
            'findings': all_findings,
            'risk_score': report['risk_score'],
            'report': report
        }

    async def get_job_status(self, job_id: str):
        return self.jobs.get(job_id, {'status': 'not_found'})