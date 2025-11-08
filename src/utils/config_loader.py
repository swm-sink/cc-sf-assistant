"""
Configuration loader for FP&A Automation Assistant.

Loads YAML configuration files with validation.
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from decimal import Decimal


class ConfigurationError(Exception):
    """Raised when configuration is invalid or missing."""
    pass


def load_yaml_config(config_path: str) -> Dict[str, Any]:
    """
    Load YAML configuration file.

    Args:
        config_path: Path to YAML configuration file

    Returns:
        Dict containing configuration

    Raises:
        FileNotFoundError: If config file doesn't exist
        ConfigurationError: If YAML is invalid

    Example:
        >>> config = load_yaml_config('config/fpa_config.yaml')
        >>> threshold = config['variance_thresholds']['percentage']
    """
    path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    try:
        with open(path, 'r') as f:
            config = yaml.safe_load(f)

        if config is None:
            raise ConfigurationError(f"Empty configuration file: {config_path}")

        return config

    except yaml.YAMLError as e:
        raise ConfigurationError(
            f"Invalid YAML in {config_path}: {e}"
        ) from e


def get_variance_thresholds(config: Dict[str, Any]) -> Dict[str, Decimal]:
    """
    Extract variance thresholds from configuration.

    Args:
        config: Configuration dict from load_yaml_config

    Returns:
        Dict with 'percentage' and 'absolute' as Decimal values

    Raises:
        ConfigurationError: If thresholds missing or invalid

    Example:
        >>> config = load_yaml_config('config/fpa_config.yaml')
        >>> thresholds = get_variance_thresholds(config)
        >>> assert thresholds['percentage'] == Decimal('0.10')
    """
    if 'variance_thresholds' not in config:
        raise ConfigurationError(
            "Missing 'variance_thresholds' in configuration"
        )

    thresholds_config = config['variance_thresholds']

    try:
        thresholds = {
            'percentage': Decimal(str(thresholds_config['percentage'])),
            'absolute': Decimal(str(thresholds_config['absolute']))
        }
    except KeyError as e:
        raise ConfigurationError(
            f"Missing threshold configuration: {e}"
        ) from e
    except Exception as e:
        raise ConfigurationError(
            f"Invalid threshold values: {e}"
        ) from e

    return thresholds


def get_favorability_rules(config: Dict[str, Any]) -> Dict[str, str]:
    """
    Extract favorability rules from configuration.

    Args:
        config: Configuration dict from load_yaml_config

    Returns:
        Dict mapping account types to favorability rules

    Raises:
        ConfigurationError: If rules missing

    Example:
        >>> config = load_yaml_config('config/fpa_config.yaml')
        >>> rules = get_favorability_rules(config)
        >>> assert rules['revenue'] == 'actual_gt_budget'
    """
    if 'favorability_rules' not in config:
        raise ConfigurationError(
            "Missing 'favorability_rules' in configuration"
        )

    return config['favorability_rules']


def load_account_mapping(mapping_path: str) -> Dict[str, str]:
    """
    Load account code mapping configuration.

    Args:
        mapping_path: Path to account mapping YAML file

    Returns:
        Dict mapping department codes to corporate codes

    Example:
        >>> mapping = load_account_mapping('config/account_mapping.yaml')
        >>> corporate_code = mapping.get('DEPT001', None)
    """
    config = load_yaml_config(mapping_path)

    if 'account_mapping' not in config:
        raise ConfigurationError(
            "Missing 'account_mapping' in mapping file"
        )

    return config['account_mapping']
