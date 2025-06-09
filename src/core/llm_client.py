import requests
import logging
from typing import Dict, List, Optional
import yaml
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self, config_path: str = "config/settings.yaml"):
        self.config = self._load_config(config_path)
        self.api_key = self.config['llm']['api_key']
        self.model = self.config['llm']['model']
        self.base_url = self.config['llm']['base_url']
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Error loading config: {str(e)}")
            raise

    def analyze_policy_violation(self, policy_id: str, violation_details: str) -> str:
        """Use LLM to analyze a policy violation and suggest remediation."""
        prompt = f"""
        Analyze the following SRE policy violation and suggest remediation steps:
        
        Policy ID: {policy_id}
        Violation Details: {violation_details}
        
        Please provide:
        1. Root cause analysis
        2. Immediate remediation steps
        3. Long-term prevention measures
        """

        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                }
            )
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            logger.error(f"Error calling LLM API: {str(e)}")
            raise

    def generate_compliance_report(self, policy_results: List[Dict]) -> str:
        """Generate a compliance report using LLM."""
        prompt = f"""
        Generate a comprehensive SRE compliance report based on the following policy check results:
        
        {policy_results}
        
        Please include:
        1. Executive summary
        2. Detailed findings
        3. Risk assessment
        4. Recommendations
        """

        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                }
            )
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            logger.error(f"Error generating compliance report: {str(e)}")
            raise

    def suggest_policy_improvements(self, policy: Dict) -> str:
        """Use LLM to suggest improvements for a policy."""
        prompt = f"""
        Review the following SRE policy and suggest improvements:
        
        {policy}
        
        Please consider:
        1. Best practices
        2. Common pitfalls
        3. Industry standards
        4. Specific recommendations
        """

        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                }
            )
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            logger.error(f"Error suggesting policy improvements: {str(e)}")
            raise 