"""Favorability determination by account type."""

from decimal import Decimal

from scripts.utils.types import AccountType, FavorabilityStatus, InvalidAccountTypeError

# Revenue/Asset: higher actual is favorable
# Expense/Liability/COGS: lower actual is favorable
FAVORABILITY_RULES: dict[AccountType, str] = {
    "revenue": "higher_is_favorable",
    "asset": "higher_is_favorable",
    "expense": "lower_is_favorable",
    "liability": "lower_is_favorable",
    "cogs": "lower_is_favorable",
}

VALID_ACCOUNT_TYPES: set[str] = set(FAVORABILITY_RULES.keys())


def determine_favorability(
    variance_amount: Decimal, account_type: AccountType
) -> FavorabilityStatus:
    """Determine if a variance is favorable, unfavorable, or neutral.

    Rules:
        Revenue/Asset: positive variance (actual > budget) = favorable
        Expense/Liability/COGS: negative variance (actual < budget) = favorable
        Zero variance = neutral
    """
    if account_type not in VALID_ACCOUNT_TYPES:
        raise InvalidAccountTypeError(
            f"Invalid account type '{account_type}'. "
            f"Valid types: {sorted(VALID_ACCOUNT_TYPES)}"
        )

    if variance_amount == Decimal("0"):
        return "neutral"

    rule = FAVORABILITY_RULES[account_type]

    if rule == "higher_is_favorable":
        return "favorable" if variance_amount > Decimal("0") else "unfavorable"
    else:  # lower_is_favorable
        return "favorable" if variance_amount < Decimal("0") else "unfavorable"


def get_favorability_direction(account_type: AccountType) -> str:
    """Return the favorability rule description for UI labeling."""
    if account_type not in VALID_ACCOUNT_TYPES:
        raise InvalidAccountTypeError(f"Invalid account type '{account_type}'")
    return FAVORABILITY_RULES[account_type]
