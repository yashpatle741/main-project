import time


class Verifier:

    def __init__(self, kube_client):
        self.kube_client = kube_client

    def verify(self, namespace: str, pod_name: str):

        time.sleep(10)

        pods = self.kube_client.list_namespaced_pod(namespace=namespace)

        for pod in pods.items:

            if not pod.metadata.name.startswith(pod_name.rsplit("-", 2)[0]):
                continue

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

        return {
            "phase": "NotFound",
            "ready": False,
            "healthy": False,
        }