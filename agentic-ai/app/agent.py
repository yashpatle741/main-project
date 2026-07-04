import time

from analyzer.analyzer import IncidentAnalyzer
from config.config import settings
from llm.gemini import GeminiClient
from monitor.monitor import ClusterMonitor
from tools.executor import ToolExecutor
from tools.verifier import Verifier
from utils.kube_client import get_kubernetes_client


class Agent:

    def __init__(self):

        kube_client = get_kubernetes_client()

        self.monitor = ClusterMonitor(kube_client)
        self.analyzer = IncidentAnalyzer(kube_client)
        self.gemini = GeminiClient()
        self.executor = ToolExecutor(kube_client)
        self.verifier = Verifier(kube_client)

        self.processed_incidents = set()

    def run(self):

        print("🤖 Agentic AI Kubernetes SRE Started...\n")

        while True:

            try:

                incidents = self.monitor.scan_cluster()

                if not incidents:
                    print("✅ Cluster Healthy")
                    self.processed_incidents.clear()

                for incident in incidents:

                    incident_id = (
                        incident.namespace,
                        incident.pod,
                        incident.issue,
                    )

                    if incident_id in self.processed_incidents:
                        continue

                    self.processed_incidents.add(incident_id)

                    self.handle_incident(incident)

                time.sleep(settings.POLL_INTERVAL)

            except KeyboardInterrupt:
                print("\nAgent stopped.")
                break

            except Exception as e:
                print(f"\nError: {e}")
                time.sleep(settings.POLL_INTERVAL)

    def handle_incident(self, incident):

        report = self.analyzer.analyze(incident)

        ai = self.gemini.analyze(report)

        print("\n===================================")
        print("🚨 INCIDENT DETECTED")
        print("===================================")
        print(f"Namespace : {report.namespace}")
        print(f"Pod       : {report.pod}")
        print(f"Issue     : {report.issue}")
        print(f"Action    : {ai.action}")
        print(f"Reason    : {ai.reason}")

        result = self.executor.execute(ai, report)

        print(f"\nExecution : {result['message']}")

        verification = self.verifier.verify(
            report.namespace,
            report.pod,
        )

        print(f"Healthy : {verification['healthy']}")
        print("===================================\n")