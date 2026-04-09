"""Shared types, dataclasses, and exceptions for FP&A automation."""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Any, Literal, Optional

AccountType = Literal["revenue", "expense", "asset", "liability", "cogs"]
FavorabilityStatus = Literal["favorable", "unfavorable", "neutral"]
UserRole = Literal["analyst", "senior_analyst", "manager"]


@dataclass
class VarianceResult:
    """Result of a single account variance calculation."""

    account_code: str
    account_name: str
    department: str
    account_type: AccountType
    budget: Decimal
    actual: Decimal
    variance_amount: Decimal
    variance_pct: Optional[Decimal]
    favorability: FavorabilityStatus
    is_material: bool
    status: str
    commentary: str = ""


@dataclass
class MaterialityThreshold:
    """Configurable materiality thresholds for variance flagging."""

    pct_threshold: Decimal = Decimal("10")
    abs_threshold: Decimal = Decimal("50000")


@dataclass
class AuditEntry:
    """Structured audit trail entry."""

    timestamp: datetime
    user: str
    operation: str
    source_files: list[str]
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class DashboardConfig:
    """Configuration for role-based dashboard generation."""

    role: UserRole
    title: str
    period: str = ""
    filters: dict[str, Any] = field(default_factory=dict)
    materiality_only: bool = False


# --- Exception hierarchy ---


class FPAError(Exception):
    """Base exception for all FP&A errors."""


class FinancialCalculationError(FPAError):
    """Error in a financial calculation."""


class DataValidationError(FPAError):
    """Error validating input data."""


class InvalidAccountTypeError(FPAError):
    """Invalid account type provided."""


class DivisionByZeroBudgetError(FinancialCalculationError):
    """Budget is zero, cannot compute percentage variance."""
