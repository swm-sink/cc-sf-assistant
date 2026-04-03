"""Configuration loading with YAML support and sensible defaults."""

from decimal import Decimal
from pathlib import Path
from typing import Any, Optional

import yaml

from scripts.utils.types import AccountType, MaterialityThreshold

DEFAULT_CONFIG: dict[str, Any] = {
    "materiality": {
        "default": {
            "pct_threshold": "10",
            "abs_threshold": "50000",
        },
        "by_category": {
            "revenue": {"pct_threshold": "5", "abs_threshold": "50000"},
        },
    },
    "account_type_prefixes": {
        "4": "revenue",
        "5": "cogs",
        "6": "expense",
        "7": "expense",
        "8": "expense",
    },
    "departments": ["Engineering", "Sales", "Marketing", "G&A", "R&D"],
    "roles": {
        "analyst": {"materiality_filter": False},
        "senior_analyst": {"materiality_filter": False},
        "manager": {"materiality_filter": True},
    },
    "output": {
        "currency_format": "$#,##0.00",
        "pct_format": "0.00%",
    },
}


def load_config(path: str = "config/fpa_config.yaml") -> dict[str, Any]:
    """Load configuration from YAML file, falling back to defaults."""
    config = dict(DEFAULT_CONFIG)
    config_path = Path(path)
    if config_path.exists():
        with open(config_path) as f:
            file_config = yaml.safe_load(f)
        if file_config:
            _deep_merge(config, file_config)
    return config


def _deep_merge(base: dict, override: dict) -> None:
    """Recursively merge override dict into base dict."""
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value


def get_materiality_thresholds(
    config: dict[str, Any], category: Optional[str] = None
) -> MaterialityThreshold:
    """Get materiality thresholds, optionally overridden by category."""
    mat_config = config.get("materiality", {})
    defaults = mat_config.get("default", {})

    pct = Decimal(str(defaults.get("pct_threshold", "10")))
    abs_val = Decimal(str(defaults.get("abs_threshold", "50000")))

    if category:
        by_cat = mat_config.get("by_category", {})
        cat_config = by_cat.get(category, {})
        if "pct_threshold" in cat_config:
            pct = Decimal(str(cat_config["pct_threshold"]))
        if "abs_threshold" in cat_config:
            abs_val = Decimal(str(cat_config["abs_threshold"]))

    return MaterialityThreshold(pct_threshold=pct, abs_threshold=abs_val)


def get_account_type_map(config: dict[str, Any]) -> dict[str, AccountType]:
    """Map account code first digit to AccountType."""
    prefixes = config.get("account_type_prefixes", DEFAULT_CONFIG["account_type_prefixes"])
    return {str(k): v for k, v in prefixes.items()}


def infer_account_type(
    account_code: str, config: dict[str, Any]
) -> AccountType:
    """Infer account type from account code prefix."""
    type_map = get_account_type_map(config)
    first_digit = str(account_code)[0] if account_code else ""
    account_type = type_map.get(first_digit)
    if account_type is None:
        return "expense"  # safe default
    return account_type
