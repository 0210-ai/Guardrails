"""Data models for guardrails violations and scan results."""

from enum import Enum
from typing import Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime


class SeverityLevel(str, Enum):
    """Severity levels for violations."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class RuleCategory(str, Enum):
    """Rule categories."""
    SECURITY = "security"
    COMPLIANCE = "compliance"
    CODE_QUALITY = "code_quality"
    PERFORMANCE = "performance"
    LICENSE = "license"


class EnforcementMode(str, Enum):
    """Enforcement modes."""
    ADVISORY = "advisory"
    WARNING = "warning"
    BLOCKING = "blocking"


@dataclass
class Violation:
    """Represents a code violation."""
    rule_id: str
    rule_name: str
    category: RuleCategory
    severity: SeverityLevel
    message: str
    file_path: str
    line_number: int
    line_content: str
    suggested_fix: Optional[str] = None
    cwe_id: Optional[str] = None
    owasp_category: Optional[str] = None
    is_copilot_generated: bool = False

    def to_dict(self):
        """Convert violation to dictionary."""
        return {
            "rule_id": self.rule_id,
            "rule_name": self.rule_name,
            "category": self.category.value,
            "severity": self.severity.value,
            "message": self.message,
            "file_path": self.file_path,
            "line_number": self.line_number,
            "line_content": self.line_content,
            "suggested_fix": self.suggested_fix,
            "cwe_id": self.cwe_id,
            "owasp_category": self.owasp_category,
            "is_copilot_generated": self.is_copilot_generated,
        }


@dataclass
class ScanResult:
    """Result of scanning code for violations."""
    scan_id: str
    repo_name: str
    pr_number: int
    commit_hash: str
    violations: List[Violation]
    timestamp: datetime
    scan_status: str = "completed"

    def to_dict(self):
        """Convert scan result to dictionary."""
        return {
            "scan_id": self.scan_id,
            "repo_name": self.repo_name,
            "pr_number": self.pr_number,
            "commit_hash": self.commit_hash,
            "violations": [v.to_dict() for v in self.violations],
            "timestamp": self.timestamp.isoformat(),
            "scan_status": self.scan_status,
            "violation_count": len(self.violations),
        }


@dataclass
class AnalysisRequest:
    """Request to analyze code."""
    repo_name: str
    pr_number: int
    commit_hash: str
    files: dict  # {filename: diff_content}
    copilot_generated_files: Optional[List[str]] = None


@dataclass
class PolicyConfig:
    """Policy configuration."""
    enforcement_mode: EnforcementMode
    enable_security_checks: bool = True
    enable_compliance_checks: bool = True
    enable_quality_checks: bool = False
    block_on_critical: bool = True
    block_on_high: bool = False
    allowed_licenses: List[str] = None
    custom_rules: dict = None

    def __post_init__(self):
        if self.allowed_licenses is None:
            self.allowed_licenses = ["MIT", "Apache-2.0", "GPL-3.0", "BSD-3-Clause"]
        if self.custom_rules is None:
            self.custom_rules = {}
