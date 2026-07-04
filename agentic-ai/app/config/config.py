import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    KUBECONFIG: str = os.path.expanduser(
        os.getenv("KUBECONFIG", "~/.kube/config")
    )

    POLL_INTERVAL: int = int(
        os.getenv("POLL_INTERVAL", "30")
    )

    ALLOWED_NAMESPACES: tuple[str, ...] = tuple(
        namespace.strip()
        for namespace in os.getenv(
            "ALLOWED_NAMESPACES",
            "default"
        ).split(",")
    )


settings = Settings()