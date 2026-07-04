from kubernetes.client import CoreV1Api
from kubernetes.client.rest import ApiException

from models.analysis import AnalysisReport
from models.incident import Incident


class IncidentAnalyzer:

    def __init__(self, kube_client: CoreV1Api):
        self.kube_client = kube_client

    def analyze(self, incident: Incident) -> AnalysisReport:

        report = AnalysisReport(
            namespace=incident.namespace,
            pod=incident.pod,
            issue=incident.issue,
        )

        try:
            report.logs = self.kube_client.read_namespaced_pod_log(
                name=incident.pod,
                namespace=incident.namespace,
                tail_lines=100,
            )
        except ApiException as e:
            report.logs = f"Unable to fetch logs: {e.reason}"

        try:
            events = self.kube_client.list_namespaced_event(
                namespace=incident.namespace
            )

            for event in events.items:
                if (
                    event.involved_object.kind == "Pod"
                    and event.involved_object.name == incident.pod
                ):
                    report.events.append(
                        {
                            "reason": event.reason,
                            "message": event.message,
                        }
                    )

        except ApiException:
            pass

        return report