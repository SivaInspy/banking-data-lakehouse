
import pandas as pd
import pytest

from src.transformers.silver_transformation import validate_transactions
from src.quality.validate_pipeline import (
    check_required_columns,
    check_transaction_ids,
    check_amounts,
    check_currency,
    check_status,
    check_payment_channel,
)
from src.transformers.gold_transformation import create_daily_summary


@pytest.fixture
def valid_transactions():
    """Create a small, valid transaction dataset for testing."""
    return pd.DataFrame(
        {
            "transaction_id": ["TXN001", "TXN002", "TXN003"],
            "account_id": ["ACC001", "ACC002", "ACC003"],
            "customer_id": ["CUS001", "CUS002", "CUS003"],
            "merchant_id": ["MER001", "MER002", "MER003"],
            "transaction_date": pd.to_datetime(
                ["2026-10-01", "2026-10-01", "2026-10-02"]
            ),
            "amount": [100.00, 250.00, 150.00],
            "currency": ["INR", "INR", "INR"],
            "payment_channel": ["UPI", "CARD", "NET_BANKING"],
            "transaction_status": ["SUCCESS", "FAILED", "PENDING"],
        }
    )


def test_valid_transactions_pass_silver_validation(valid_transactions):
    result = validate_transactions(valid_transactions.copy())

    assert (result["quarantine_reason"] == "").all()


def test_non_positive_amount_is_quarantined(valid_transactions):
    valid_transactions.loc[0, "amount"] = 0

    result = validate_transactions(valid_transactions)

    assert "invalid_amount;" in result.loc[0, "quarantine_reason"]


def test_missing_transaction_id_is_quarantined(valid_transactions):
    valid_transactions.loc[0, "transaction_id"] = None

    result = validate_transactions(valid_transactions)

    assert "transaction_id_missing;" in result.loc[0, "quarantine_reason"]


def test_duplicate_transaction_id_is_quarantined(valid_transactions):
    valid_transactions.loc[1, "transaction_id"] = "TXN001"

    result = validate_transactions(valid_transactions)

    assert "duplicate_transaction;" in result.loc[1, "quarantine_reason"]


def test_invalid_currency_is_quarantined(valid_transactions):
    valid_transactions.loc[0, "currency"] = "USD"

    result = validate_transactions(valid_transactions)

    assert "invalid_currency;" in result.loc[0, "quarantine_reason"]


def test_invalid_status_is_quarantined(valid_transactions):
    valid_transactions.loc[0, "transaction_status"] = "UNKNOWN"

    result = validate_transactions(valid_transactions)

    assert "invalid_transaction_status;" in result.loc[0, "quarantine_reason"]


def test_invalid_payment_channel_is_quarantined(valid_transactions):
    valid_transactions.loc[0, "payment_channel"] = "CRYPTO"

    result = validate_transactions(valid_transactions)

    assert "invalid_payment_channel;" in result.loc[0, "quarantine_reason"]


def test_required_columns_check_passes(valid_transactions):
    check_required_columns(valid_transactions)


def test_required_columns_check_fails_when_column_missing(valid_transactions):
    transactions = valid_transactions.drop(columns=["account_id"])

    with pytest.raises(ValueError, match="Missing columns"):
        check_required_columns(transactions)


def test_duplicate_transaction_ids_fail_quality_check(valid_transactions):
    valid_transactions.loc[1, "transaction_id"] = "TXN001"

    with pytest.raises(ValueError, match="Duplicate transaction_id"):
        check_transaction_ids(valid_transactions)


def test_invalid_amount_fails_quality_check(valid_transactions):
    valid_transactions.loc[0, "amount"] = -10

    with pytest.raises(ValueError, match="Non-positive transaction amount"):
        check_amounts(valid_transactions)


def test_invalid_currency_fails_quality_check(valid_transactions):
    valid_transactions.loc[0, "currency"] = "USD"

    with pytest.raises(ValueError, match="Invalid currencies"):
        check_currency(valid_transactions)


def test_invalid_status_fails_quality_check(valid_transactions):
    valid_transactions.loc[0, "transaction_status"] = "UNKNOWN"

    with pytest.raises(ValueError, match="Invalid transaction statuses"):
        check_status(valid_transactions)


def test_invalid_payment_channel_fails_quality_check(valid_transactions):
    valid_transactions.loc[0, "payment_channel"] = "CRYPTO"

    with pytest.raises(ValueError, match="Invalid payment channels"):
        check_payment_channel(valid_transactions)


def test_gold_daily_summary_calculates_totals(valid_transactions):
    summary = create_daily_summary(valid_transactions.copy())

    first_day = summary.loc[
        summary["transaction_day"] == pd.Timestamp("2026-10-01").date()
    ].iloc[0]

    second_day = summary.loc[
        summary["transaction_day"] == pd.Timestamp("2026-10-02").date()
    ].iloc[0]

    assert first_day["transaction_count"] == 2
    assert first_day["total_amount"] == pytest.approx(350.00)
    assert first_day["average_transaction_amount"] == pytest.approx(175.00)

    assert second_day["transaction_count"] == 1
    assert second_day["total_amount"] == pytest.approx(150.00)
    assert second_day["average_transaction_amount"] == pytest.approx(150.00)
