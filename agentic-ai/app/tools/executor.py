from kubernetes import client


class ToolExecutor:

    def __init__(self, kube_client):
        self.core = kube_client
        self.apps = client.AppsV1Api(kube_client.api_client)

    def execute(self, ai_response, report):

        if ai_response.action == "delete_pod":
            return self.delete_pod(
                report.namespace,
                report.pod,
            )

        if ai_response.action == "restart_deployment":

            if not ai_response.deployment:
                return {
                    "success": False,
                    "message": "Deployment name not provided by AI."
                }

            return self.restart_deployment(
                report.namespace,
                ai_response.deployment,
            )

        return {
            "success": True,
            "message": "No action required."
        }

    def delete_pod(self, namespace, pod_name):

        self.core.delete_namespaced_pod(
            name=pod_name,
            namespace=namespace,
        )

        return {
            "success": True,
            "message": f"Pod '{pod_name}' deleted."
        }

    def restart_deployment(self, namespace, deployment):

        body = {
            "spec": {
                "template": {
                    "metadata": {
                        "annotations": {
                            "kubectl.kubernetes.io/restartedAt": "agentic-ai"
                        }
                    }
                }
            }
        }

        self.apps.patch_namespaced_deployment(
            name=deployment,
            namespace=namespace,
            body=body,
        )

        return {
            "success": True,
            "message": f"Deployment '{deployment}' restarted."
        }