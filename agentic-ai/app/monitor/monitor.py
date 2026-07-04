from kubernetes.client import CoreV1Api

from models.incident import Incident


class ClusterMonitor:

    ERROR_STATES = {
        "CrashLoopBackOff",
        "ImagePullBackOff",
        "ErrImagePull",
        "CreateContainerConfigError",
        "CreateContainerError",
    }

    def __init__(self, kube_client: CoreV1Api):
        self.kube_client = kube_client

    def scan_cluster(self) -> list[Incident]:

        incidents = []

        pods = self.kube_client.list_pod_for_all_namespaces()

        for pod in pods.items:

            namespace = pod.metadata.namespace
            pod_name = pod.metadata.name

            if pod.status.phase == "Pending":
                incidents.append(
                    Incident(
                        namespace=namespace,
                        pod=pod_name,
                        issue="Pending",
                    )
                )

            if not pod.status.container_statuses:
                continue

            for container in pod.status.container_statuses:

                waiting = container.state.waiting

                if waiting and waiting.reason in self.ERROR_STATES:

                    incidents.append(
                        Incident(
                            namespace=namespace,
                            pod=pod_name,
                            issue=waiting.reason,
                        )
                    )

        return incidents