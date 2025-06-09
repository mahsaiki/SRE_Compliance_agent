from flask import Flask, request, jsonify
from core.cicd_integration import CICDIntegration
from core.infrastructure_analysis import InfrastructureAnalysis
from core.reporting_module import ReportingModule

app = Flask(__name__)

# Initialize components
cicd = CICDIntegration('config/settings.yaml')
infra = InfrastructureAnalysis('config/settings.yaml')
reporting = ReportingModule('config/settings.yaml')

@app.route('/check_policy', methods=['POST'])
def check_policy():
    data = request.json
    policy_id = data.get('policy_id')
    result = cicd.trigger_automated_check(policy_id)
    return jsonify(result)

@app.route('/analyze_infrastructure', methods=['POST'])
def analyze_infrastructure():
    data = request.json
    service_name = data.get('service_name')
    result = infra.check_compliance(service_name)
    return jsonify(result)

@app.route('/generate_report', methods=['POST'])
def generate_report():
    data = request.json
    service_name = data.get('service_name')
    result = reporting.create_report(service_name)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True) 