from typing import Dict, List, Optional
import yaml
from pydantic import BaseModel, Field
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Alert(BaseModel):
    name: str
    condition: str
    severity: str
    notify: str

class OnCall(BaseModel):
    team: str
    schedule: str
    escalation: str

class SLO(BaseModel):
    objective: str
    latency_p95: Optional[str] = None
    window: str

class SLA(BaseModel):
    objective: str
    window: str

class Policy(BaseModel):
    id: str
    description: str
    service: str
    slo: SLO
    sla: SLA
    on_call: OnCall
    alerts: List[Alert]

class PolicyEngine:
    def __init__(self, policy_file: str):
        self.policy_file = policy_file
        self.policies: Dict[str, Policy] = {}
        self.load_policies()

    def load_policies(self) -> None:
        """Load policies from YAML file."""
        try:
            with open(self.policy_file, 'r') as f:
                policy_data = yaml.safe_load(f)
                for policy_dict in policy_data.get('policies', []):
                    policy = Policy(**policy_dict)
                    self.policies[policy.id] = policy
            logger.info(f"Loaded {len(self.policies)} policies successfully")
        except Exception as e:
            logger.error(f"Error loading policies: {str(e)}")
            raise

    def get_policy(self, policy_id: str) -> Optional[Policy]:
        """Get a specific policy by ID."""
        return self.policies.get(policy_id)

    def validate_policy(self, policy_id: str) -> bool:
        """Validate if a policy meets all requirements."""
        policy = self.get_policy(policy_id)
        if not policy:
            logger.error(f"Policy {policy_id} not found")
            return False

        try:
            # Validate SLO objectives
            slo_obj = float(policy.slo.objective.strip('%'))
            if not (0 <= slo_obj <= 100):
                logger.error(f"Invalid SLO objective: {slo_obj}")
                return False

            # Validate SLA objectives
            sla_obj = float(policy.sla.objective.strip('%'))
            if not (0 <= sla_obj <= 100):
                logger.error(f"Invalid SLA objective: {sla_obj}")
                return False

            # Validate latency format if present
            if policy.slo.latency_p95:
                latency = policy.slo.latency_p95.lower()
                if not (latency.endswith('ms') or latency.endswith('s')):
                    logger.error(f"Invalid latency format: {latency}")
                    return False

            return True
        except Exception as e:
            logger.error(f"Error validating policy {policy_id}: {str(e)}")
            return False

    def get_all_policies(self) -> Dict[str, Policy]:
        """Get all loaded policies."""
        return self.policies

    def get_service_policies(self, service_name: str) -> List[Policy]:
        """Get all policies for a specific service."""
        return [p for p in self.policies.values() if p.service == service_name] 