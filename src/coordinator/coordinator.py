import asyncio
import uuid
import json
from typing import Dict, List
from ..agents.network_agent import NetworkSecurityAgent
from ..agents.data_flow_agent import DataFlowAgent
from ..agents.infrastructure_agent import InfrastructureAgent
from ..agents.code_agent import CodeSecurityAgent

class CoordinatorAgent:
    def __init__(self):
        self.agents = {
            'network': NetworkSecurityAgent(),
            'data_flow': DataFlowAgent(),
            'infrastructure': InfrastructureAgent(),
            'code': CodeSecurityAgent()
        }
        self.jobs = {}

    async def parse_file(self, file):
        """Enhanced file parser"""
        content = await file.read()
        content_str = content.decode('utf-8')
        
        # Try to parse as JSON first
        try:
            return json.loads(content_str)
        except:
            # Parse markdown tables and extract detailed info
            data = {'raw_content': content_str}
            lines = content_str.split('\n')
            
            # Parse services table
            services = []
            in_services = False
            for line in lines:
                if '| Name |' in line and 'Public' in line:
                    in_services = True
                    continue
                if in_services and line.startswith('|') and '---' not in line:
                    parts = [p.strip() for p in line.split('|')[1:-1]]
                    if len(parts) >= 4:
                        services.append({
                            'name': parts[0],
                            'public': parts[1].lower() == 'yes',
                            'authentication': parts[2].lower() == 'yes',
                            'port': int(parts[3]) if parts[3].isdigit() else 80
                        })
                elif in_services and not line.startswith('|'):
                    in_services = False
            
            # Parse firewall rules
            firewall_rules = []
            in_firewall = False
            for line in lines:
                if '| Source |' in line and 'Port' in line:
                    in_firewall = True
                    continue
                if in_firewall and line.startswith('|') and '---' not in line:
                    parts = [p.strip() for p in line.split('|')[1:-1]]
                    if len(parts) >= 3:
                        firewall_rules.append({
                            'source': parts[0],
                            'port': int(parts[1]) if parts[1].isdigit() else 80,
                            'protocol': parts[2]
                        })
                elif in_firewall and not line.startswith('|'):
                    in_firewall = False
            
            # Parse data flows
            data_flows = []
            in_flows = False
            for line in lines:
                if '| Source |' in line and 'Destination' in line and 'Encrypted' in line:
                    in_flows = True
                    continue
                if in_flows and line.startswith('|') and '---' not in line:
                    parts = [p.strip() for p in line.split('|')[1:-1]]
                    if len(parts) >= 3:
                        data_flows.append({
                            'source': parts[0],
                            'destination': parts[1],
                            'encrypted': parts[2].lower() == 'yes'
                        })
                elif in_flows and not line.startswith('|'):
                    in_flows = False
            
            # Parse databases
            databases = []
            in_db = False
            for line in lines:
                if '| Name |' in line and 'Data Types' in line:
                    in_db = True
                    continue
                if in_db and line.startswith('|') and '---' not in line:
                    parts = [p.strip() for p in line.split('|')[1:-1]]
                    if len(parts) >= 3:
                        databases.append({
                            'name': parts[0],
                            'data_types': parts[1].split(','),
                            'encrypted_at_rest': parts[2].lower() == 'yes'
                        })
                elif in_db and not line.startswith('|'):
                    in_db = False
            
            # Parse IAM policies
            iam_policies = []
            in_iam = False
            for line in lines:
                if '| Name |' in line and 'Actions' in line and 'Resources' in line:
                    in_iam = True
                    continue
                if in_iam and line.startswith('|') and '---' not in line:
                    parts = [p.strip() for p in line.split('|')[1:-1]]
                    if len(parts) >= 3:
                        iam_policies.append({
                            'name': parts[0],
                            'actions': parts[1].split(','),
                            'resources': parts[2].split(',')
                        })
                elif in_iam and not line.startswith('|'):
                    in_iam = False
            
            # Parse storage
            storage = []
            in_storage = False
            for line in lines:
                if '| Name |' in line and 'Public Read' in line and 'Encryption' in line:
                    in_storage = True
                    continue
                if in_storage and line.startswith('|') and '---' not in line:
                    parts = [p.strip() for p in line.split('|')[1:-1]]
                    if len(parts) >= 3:
                        storage.append({
                            'name': parts[0],
                            'public_read': parts[1].lower() == 'yes',
                            'encryption': parts[2].lower() == 'yes'
                        })
                elif in_storage and not line.startswith('|'):
                    in_storage = False
            
            # Populate data structure
            if services:
                data['services'] = services
            if firewall_rules:
                data['firewall_rules'] = firewall_rules
            if data_flows:
                data['data_flows'] = data_flows
            if databases:
                data['databases'] = databases
            if iam_policies:
                data['iam_policies'] = iam_policies
            if storage:
                data['storage'] = storage
            
            return data

    async def process_analysis(self, file):
        job_id = str(uuid.uuid4())
        
        # Parse file
        parsed_data = await self.parse_file(file)
        
        # Run agents in parallel
        tasks = [agent.analyze(parsed_data) for agent in self.agents.values()]
        results = await asyncio.gather(*tasks)
        
        # Flatten findings
        all_findings = []
        for agent_findings in results:
            all_findings.extend(agent_findings)
        
        # Group by severity
        findings_by_severity = {
            'CRITICAL': [f for f in all_findings if f['severity'] == 'CRITICAL'],
            'HIGH': [f for f in all_findings if f['severity'] == 'HIGH'],
            'MEDIUM': [f for f in all_findings if f['severity'] == 'MEDIUM'],
            'LOW': [f for f in all_findings if f['severity'] == 'LOW']
        }
        
        # Calculate risk score
        risk_score = min(100, len(all_findings) * 15)
        
        report = {
            'summary': f'Analysis completed for {file.filename}. Found {len(all_findings)} issues.',
            'total_findings': len(all_findings),
            'risk_score': risk_score,
            'findings_by_severity': findings_by_severity
        }
        
        self.jobs[job_id] = {'status': 'completed', 'results': report}
        
        return {
            'job_id': job_id,
            'status': 'completed',
            'findings': all_findings,
            'risk_score': risk_score,
            'report': report
        }

    async def get_job_status(self, job_id: str):
        return self.jobs.get(job_id, {'status': 'not_found'})