import time


class Verifier:

    def __init__(self, kube_client):
        self.kube_client = kube_client

    def verify(self, namespace: str, pod_name: str):

        time.sleep(10)

        pod = self.kube_client.read_namespaced_pod(
            name=pod_name,
            namespace=namespace,
        )

        phase = pod.status.phase

        ready = False

        if pod.status.container_statuses:
            ready = all(
                container.ready
                for container in pod.status.container_statuses
            )

        return {
            "phase": phase,
            "ready": ready,
            "healthy": phase == "Running" and ready,
        }