"""Configuration and environment settings validation (Rule R-19, R-36)."""

from functools import lru_cache

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Placeholder values that are fine in dev/test (nothing reads them yet —
# auth, Groq, and the GitHub webhook aren't wired up until later phases)
# but must never be present in a production start. Keeping them as
# defaults instead of required fields avoids forcing every contributor
# to hold real Google OAuth / JWT / Groq credentials just to run Phase 1.
_DEV_ONLY_PLACEHOLDERS = {
    "GROQ_API_KEY": "mock_key_for_dev",
    "GOOGLE_CLIENT_ID": "",
    "GOOGLE_CLIENT_SECRET": "",
    "JWT_PRIVATE_KEY": "",
    "JWT_PUBLIC_KEY": "",
    "GITHUB_WEBHOOK_SECRET": "",
}


class Settings(BaseSettings):
    """Application Settings validated from environment variables."""

    # Environment
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    FRONTEND_URL: str = "http://localhost:3000"

    # Datastores
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/sentinelai"
    REDIS_URL: str = "redis://localhost:6379/0"

    # LLM & AI Providers
    GROQ_API_KEY: str = "mock_key_for_dev"
    GROQ_MODEL_FAST: str = "llama-3.1-8b-instant"
    GROQ_MODEL_SMART: str = "llama-3.1-70b-versatile"
    OLLAMA_BASE_URL: str = "http://localhost:11434"

    # Auth & Security
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    JWT_PRIVATE_KEY: str = ""
    JWT_PUBLIC_KEY: str = ""
    GITHUB_WEBHOOK_SECRET: str = ""

    # ML & Detection Settings
    ANOMALY_THRESHOLD: float = -0.1

    # Safety Gates (Rule R-100)
    CONFIDENCE_GATE_THRESHOLD: float = 0.82
    MIN_HEALING_SUCCESSES: int = 3

    # Alerts
    SLACK_WEBHOOK_URL: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @model_validator(mode="after")
    def fail_fast_on_production_placeholders(self) -> "Settings":
        """Refuses to start in production with dev-only placeholder secrets (R-36).

        Dev and test may run with empty/mock secrets since nothing reads
        them yet. Production must not: this is the actual "app refuses
        to start with missing values" behavior Blueprint v2 Section 2.5
        promises but the previous version of this file never enforced.
        """
        if self.ENVIRONMENT != "production":
            return self

        unset = [
            field
            for field, placeholder in _DEV_ONLY_PLACEHOLDERS.items()
            if getattr(self, field) == placeholder
        ]
        if unset:
            raise ValueError(
                "Missing required env var(s) for production: "
                f"{', '.join(unset)}. Set real values in the production "
                "environment — see .env.example for the expected shape."
            )
        return self


@lru_cache()
def get_settings() -> Settings:
    """Returns cached singleton application settings."""
    return Settings()


settings = get_settings()
