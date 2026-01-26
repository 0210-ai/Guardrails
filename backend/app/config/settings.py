"""Configuration management."""

import os
from app.models import PolicyConfig, EnforcementMode


class Config:
    """Application configuration."""

    # Server
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

    # Security
    BACKEND_SECRET = os.getenv("BACKEND_SECRET", "dev-secret-key-change-in-production")

    # Policy
    DEFAULT_ENFORCEMENT_MODE = EnforcementMode.WARNING

    @staticmethod
    def get_default_policy() -> PolicyConfig:
        """Get default policy configuration."""
        return PolicyConfig(
            enforcement_mode=EnforcementMode.WARNING,
            enable_security_checks=True,
            enable_compliance_checks=True,
            enable_quality_checks=False,
            block_on_critical=True,
            block_on_high=False,
            allowed_licenses=["MIT", "Apache-2.0", "GPL-3.0", "BSD-3-Clause"],
        )
