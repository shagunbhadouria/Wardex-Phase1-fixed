"""Application-wide named constants (Rule R-34)."""

# Anomaly Detection & ML Defaults
ANOMALY_THRESHOLD: float = -0.1
CONFIDENCE_GATE_THRESHOLD: float = 0.82
MIN_HEALING_SUCCESSES: int = 3
MAX_RETRY_ATTEMPTS: int = 3

# Groq Model IDs
GROQ_MODEL_FAST: str = "llama-3.1-8b-instant"
GROQ_MODEL_SMART: str = "llama-3.1-70b-versatile"

# Cache TTLs (seconds)
CACHE_TTL_DEFAULT: int = 300
CACHE_TTL_HEALTH: int = 60
JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

# High Risk Actions that NEVER auto-execute (Rule R-100 / Blueprint v2 Section 2.3)
HIGH_RISK_ACTIONS: set[str] = {
    "database_restart",
    "network_config_change",
}
