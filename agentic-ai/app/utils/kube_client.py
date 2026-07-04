from kubernetes import client, config

from config.config import settings


def get_kubernetes_client():
    config.load_kube_config(config_file=settings.KUBECONFIG)
    return client.CoreV1Api()