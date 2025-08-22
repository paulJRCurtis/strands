from .base_agent import BaseAgent
import json
import yaml
import re
from typing import Dict, List

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
            elif filename.endswith('.md'):
                return self._parse_markdown(content.decode('utf-8'))
            else:
                # Basic text parsing for other formats
                return {'raw_content': content.decode('utf-8')}
        except Exception as e:
            return {'error': f'Failed to parse file: {str(e)}'}

    def _parse_markdown(self, content: str) -> Dict:
        """Parse markdown tables into structured data"""
        result = {}
        
        # Parse Services table
        services = self._parse_table(content, "Services")
        if services:
            result['services'] = [{
                'name': row.get('Name', ''),
                'public': row.get('Public', '').lower() in ['yes', '✅'],
                'authentication': row.get('Authentication', '').lower() in ['yes', '✅'],
                'port': int(row.get('Port', 0)) if row.get('Port', '').isdigit() else 0
            } for row in services]
        
        # Parse Firewall Rules table
        firewall_rules = self._parse_table(content, "Firewall Rules")
        if firewall_rules:
            result['firewall_rules'] = [{
                'source': row.get('Source', ''),
                'port': int(row.get('Port', 0)) if row.get('Port', '').isdigit() else 0,
                'protocol': row.get('Protocol', '')
            } for row in firewall_rules]
        
        # Parse Data Flows table
        data_flows = self._parse_table(content, "Data Flows")
        if data_flows:
            result['data_flows'] = [{
                'source': row.get('Source', ''),
                'destination': row.get('Destination', ''),
                'encrypted': row.get('Encrypted', '').lower() in ['yes', '✅']
            } for row in data_flows]
        
        # Parse Databases table
        databases = self._parse_table(content, "Databases")
        if databases:
            result['databases'] = [{
                'name': row.get('Name', ''),
                'data_types': [dt.strip() for dt in row.get('Data Types', '').split(',')],
                'encrypted_at_rest': row.get('Encrypted at Rest', '').lower() in ['yes', '✅']
            } for row in databases]
        
        # Parse IAM Policies table
        iam_policies = self._parse_table(content, "IAM Policies")
        if iam_policies:
            result['iam_policies'] = [{
                'name': row.get('Name', ''),
                'actions': [row.get('Actions', '')],
                'resources': [row.get('Resources', '')]
            } for row in iam_policies]
        
        # Parse Storage table
        storage = self._parse_table(content, "Storage")
        if storage:
            result['storage'] = [{
                'name': row.get('Name', ''),
                'public_read': row.get('Public Read', '').lower() in ['yes', '✅'],
                'encryption': row.get('Encryption', '').lower() in ['yes', '✅']
            } for row in storage]
        
        return result
    
    def _parse_table(self, content: str, section_name: str) -> List[Dict]:
        """Extract table data from markdown section"""
        # Find the section
        section_pattern = rf"## {section_name}\s*\n\n(.*?)(?=\n## |\Z)"
        section_match = re.search(section_pattern, content, re.DOTALL)
        
        if not section_match:
            return []
        
        section_content = section_match.group(1).strip()
        lines = section_content.split('\n')
        
        if len(lines) < 3:  # Need header, separator, and at least one data row
            return []
        
        # Parse header
        headers = [h.strip() for h in lines[0].split('|')[1:-1]]  # Remove empty first/last
        
        # Parse data rows (skip separator line)
        rows = []
        for line in lines[2:]:
            if '|' in line:
                cells = [c.strip() for c in line.split('|')[1:-1]]  # Remove empty first/last
                if len(cells) == len(headers):
                    rows.append(dict(zip(headers, cells)))
        
        return rows

    async def analyze(self, data: Dict) -> Dict:
        # Parser doesn't generate findings, just processes input
        return data