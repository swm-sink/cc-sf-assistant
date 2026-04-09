"""Tests for multi-department consolidation."""

from decimal import Decimal

from scripts.core.consolidation import (
    consolidate_records,
    detect_duplicate_accounts,
    reconcile_to_total,
)


class TestConsolidateRecords:
    def test_consolidate_two_departments(self):
        dept_records = {
            "Sales": [
                {"account_code": "4000", "budget": Decimal("100000"), "actual": Decimal("110000")},
            ],
            "Engineering": [
                {"account_code": "6000", "budget": Decimal("200000"), "actual": Decimal("205000")},
            ],
        }
        consolidated, metadata = consolidate_records(dept_records)
        assert len(consolidated) == 2
        assert metadata["total_records"] == 2
        assert "Sales" in metadata["departments"]
        assert "Engineering" in metadata["departments"]

    def test_department_tag_added(self):
        dept_records = {
            "Marketing": [
                {"account_code": "7040", "budget": Decimal("50000")},
            ],
        }
        consolidated, _ = consolidate_records(dept_records)
        assert consolidated[0]["department"] == "Marketing"

    def test_empty_department(self):
        dept_records = {"Empty": []}
        consolidated, metadata = consolidate_records(dept_records)
        assert len(consolidated) == 0
        assert metadata["department_counts"]["Empty"] == 0


class TestDetectDuplicates:
    def test_no_duplicates(self):
        dept_records = {
            "Sales": [{"account_code": "4000"}],
            "Engineering": [{"account_code": "6000"}],
        }
        dupes = detect_duplicate_accounts(dept_records)
        assert len(dupes) == 0

    def test_duplicate_detected(self):
        dept_records = {
            "Sales": [{"account_code": "4000"}],
            "Marketing": [{"account_code": "4000"}],
        }
        dupes = detect_duplicate_accounts(dept_records)
        assert len(dupes) == 1
        assert dupes[0][0] == "4000"
        assert set(dupes[0][1]) == {"Sales", "Marketing"}


class TestReconcileToTotal:
    def test_matches(self):
        dept_totals = {"Sales": Decimal("100"), "Engineering": Decimal("200")}
        matches, diff = reconcile_to_total(dept_totals, Decimal("300"))
        assert matches is True
        assert diff == Decimal("0")

    def test_mismatch(self):
        dept_totals = {"Sales": Decimal("100"), "Engineering": Decimal("200")}
        matches, diff = reconcile_to_total(dept_totals, Decimal("290"))
        assert matches is False
        assert diff == Decimal("10")
