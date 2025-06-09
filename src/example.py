from core.policy_engine import PolicyEngine
from core.llm_client import LLMClient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Initialize the policy engine
    policy_engine = PolicyEngine("config/policies/user_service_policy.yaml")
    
    # Initialize the LLM client
    llm_client = LLMClient()
    
    # Get all policies
    policies = policy_engine.get_all_policies()
    
    # Example: Validate a policy
    policy_id = "availability-slo"
    if policy_engine.validate_policy(policy_id):
        logger.info(f"Policy {policy_id} is valid")
        
        # Get the policy
        policy = policy_engine.get_policy(policy_id)
        
        # Example: Get LLM suggestions for policy improvements
        improvements = llm_client.suggest_policy_improvements(policy.model_dump())
        logger.info("Policy improvement suggestions:")
        logger.info(improvements)
        
        # Example: Simulate a policy violation
        violation_details = """
        Service: user-service
        Current Error Rate: 1.2%
        Current P95 Latency: 450ms
        Time Window: Last 24 hours
        """
        
        # Get LLM analysis of the violation
        analysis = llm_client.analyze_policy_violation(policy_id, violation_details)
        logger.info("Violation analysis:")
        logger.info(analysis)
        
        # Generate a compliance report
        policy_results = [
            {
                "policy_id": policy_id,
                "status": "violated",
                "details": violation_details
            }
        ]
        report = llm_client.generate_compliance_report(policy_results)
        logger.info("Compliance report:")
        logger.info(report)
    else:
        logger.error(f"Policy {policy_id} is invalid")

if __name__ == "__main__":
    main() 